from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.utils import timezone
import hashlib
import json
import os


def _lesson_has_gradable_tests(lesson):
    raw = (lesson.tests_inline or '').strip()
    if not raw:
        return False
    try:
        spec = json.loads(raw)
    except json.JSONDecodeError:
        return False
    if not isinstance(spec, dict):
        return False
    if 'expectedStdout' in spec and spec.get('expectedStdout') is not None:
        return True
    for ft in spec.get('functionTests') or []:
        if ft.get('function') and ft.get('cases'):
            return True
    for et in spec.get('expressionTests') or []:
        if et.get('expr'):
            return True
    return False


def cover(request):
    if request.user.is_authenticated:
        return redirect('toc')
    return render(request, 'core/cover.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('toc')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('toc')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})


@login_required
def toc(request):
    from .models import Lesson, ChapterProgress
    lessons = list(Lesson.objects.all())
    progresses = {p.lesson_id: p for p in ChapterProgress.objects.filter(user=request.user, lesson__in=lessons)}
    data = []
    for l in lessons:
        prog = progresses.get(l.id)
        data.append({
            'lesson': l,
            'is_completed': bool(prog and prog.is_completed),
            'best_score': prog.best_score if prog else 0,
        })
    return render(request, 'core/toc.html', {'items': data})


@login_required
def lesson_detail(request, slug):
    from .models import Lesson, ChapterProgress
    lesson = Lesson.objects.filter(slug=slug).first()
    if not lesson:
        return redirect('toc')
    lessons = list(Lesson.objects.order_by('order'))
    idx = next((i for i, l in enumerate(lessons) if l.id == lesson.id), -1)
    prev_lesson = lessons[idx - 1] if idx > 0 else None
    next_lesson = lessons[idx + 1] if idx >= 0 and idx < len(lessons) - 1 else None
    done_count = ChapterProgress.objects.filter(user=request.user, is_completed=True).count()
    total_count = len(lessons) or 1
    progress_percent = round(done_count * 100 / total_count, 1)
    return render(request, 'core/lesson_detail.html', {
        'lesson': lesson,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'progress_percent': progress_percent,
        'done_count': done_count,
        'total_count': total_count,
    })


@login_required
def profile(request):
    from .models import UserProfile, ChapterProgress
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    completed = ChapterProgress.objects.filter(user=request.user, is_completed=True).select_related('lesson')
    can_download_certificate = profile.completed_percent >= 100.0
    return render(request, 'core/profile.html', {
        'profile_obj': profile,
        'completed': completed,
        'can_download_certificate': can_download_certificate,
    })


def logout_view(request):
    logout(request)
    return redirect('cover')


@login_required
def submit(request, slug):
    if request.method != 'POST':
        return HttpResponseBadRequest('POST only')
    from .models import Lesson, Submission, ChapterProgress, UserProfile
    lesson = Lesson.objects.filter(slug=slug).first()
    if not lesson:
        return HttpResponseBadRequest('Lesson not found')
    is_success = request.POST.get('is_success') == '1'
    if is_success and not _lesson_has_gradable_tests(lesson):
        is_success = False
    output = request.POST.get('output', '')
    points = 0
    awarded = 0
    if is_success:
        points = sum(t.points for t in lesson.tasks.all()) or 10
    Submission.objects.create(
        user=request.user, lesson=lesson, code=request.POST.get('code', ''),
        is_success=is_success, output=output
    )
    prog, _ = ChapterProgress.objects.get_or_create(user=request.user, lesson=lesson)
    if is_success:
        previous_best = prog.best_score
        prog.is_completed = True
        prog.best_score = max(prog.best_score, points)
        awarded = max(0, prog.best_score - previous_best)
        prog.completed_at = prog.completed_at or timezone.now()
    prog.save()
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.total_points = sum(
        p.best_score for p in ChapterProgress.objects.filter(user=request.user, is_completed=True))
    from .models import Lesson as L
    total = L.objects.count() or 1
    done = ChapterProgress.objects.filter(user=request.user, is_completed=True).count()
    profile.completed_percent = round(100.0 * done / total, 2)
    profile.save()
    return JsonResponse({
        'ok': True,
        'success': is_success,
        'awarded': awarded,
        'completed_percent': profile.completed_percent,
    })


@login_required
def certificate(request):
    from .models import Lesson, ChapterProgress, UserProfile
    total = Lesson.objects.count()
    done = ChapterProgress.objects.filter(user=request.user, is_completed=True).count()
    if total == 0 or done < total:
        return redirect('profile')
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if not profile.certificate_code:
        base = f"{request.user.id}:{request.user.username}:{timezone.now().isoformat()}"
        profile.certificate_code = hashlib.sha256(base.encode('utf-8')).hexdigest()[:16].upper()
    if not profile.certificate_issued_at:
        profile.certificate_issued_at = timezone.now()
    profile.save(update_fields=['certificate_code', 'certificate_issued_at'])
    verify_url = request.build_absolute_uri(f"/certificate/verify/{profile.certificate_code}/")
    from io import BytesIO
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.graphics.barcode.qr import QrCodeWidget
    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics import renderPDF
    def _pick_font():
        import platform
        system = platform.system()
        if system == 'Windows':
            candidates = [os.path.join(os.environ.get('WINDIR', r'C:\Windows'), 'Fonts', 'arial.ttf')]
        elif system == 'Darwin':
            candidates = ['/System/Library/Fonts/Helvetica.ttc']
        else:
            candidates = ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
        for path in candidates:
            if os.path.exists(path):
                try:
                    pdfmetrics.registerFont(TTFont('CertFont', path))
                    return 'CertFont'
                except:
                    continue
        return 'Helvetica'

    cert_font = _pick_font()
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    p.setFillColor(colors.HexColor('#F4FBF7'))
    p.rect(0, 0, width, height, stroke=0, fill=1)
    p.setStrokeColor(colors.HexColor('#2F8852'))
    p.setLineWidth(3)
    p.rect(28, 28, width - 56, height - 56, stroke=1, fill=0)
    p.setLineWidth(1)
    p.rect(38, 38, width - 76, height - 76, stroke=1, fill=0)
    p.setFillColor(colors.HexColor('#1F5837'))
    p.setFont(cert_font, 30)
    p.drawCentredString(width / 2, height - 130, "СЕРТИФИКАТ")
    p.setFont(cert_font, 16)
    p.drawCentredString(width / 2, height - 165, "о прохождении курса Dino Python Book")
    p.setFont(cert_font, 14)
    p.setFillColor(colors.black)
    p.drawCentredString(width / 2, height - 220, "Настоящим подтверждается, что")
    p.setFont(cert_font, 22)
    p.setFillColor(colors.HexColor('#276E43'))
    p.drawCentredString(width / 2, height - 255, request.user.get_username())
    p.setFont(cert_font, 13)
    p.setFillColor(colors.black)
    p.drawCentredString(width / 2, height - 290, "успешно завершил(а) все уроки курса по ООП.")
    p.drawCentredString(width / 2, height - 320, f"Итоговые очки: {profile.total_points}")
    issued = profile.certificate_issued_at.strftime('%d.%m.%Y')
    p.drawString(70, 130, f"Дата выдачи: {issued}")
    p.drawString(70, 108, f"№ сертификата: {profile.certificate_code}")
    p.setFont(cert_font, 11)
    p.drawString(70, 86, "Подпись наставника: ____________________")
    p.setStrokeColor(colors.HexColor('#2F8852'))
    p.circle(width - 120, 120, 42, stroke=1, fill=0)
    p.setFont(cert_font, 9)
    p.drawCentredString(width - 120, 128, "DINO PYTHON BOOK")
    p.drawCentredString(width - 120, 112, "CERTIFIED")
    qr = QrCodeWidget(verify_url)
    b = qr.getBounds()
    w = b[2] - b[0]
    h = b[3] - b[1]
    d = Drawing(90, 90, transform=[90.0 / w, 0, 0, 90.0 / h, 0, 0])
    d.add(qr)
    renderPDF.draw(d, p, width - 165, 45)
    p.setFont(cert_font, 9)
    p.drawString(width - 190, 35, "Проверка подлинности по QR")
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    resp = HttpResponse(pdf, content_type='application/pdf')
    resp['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    return resp


def verify_certificate(request, code):
    from .models import UserProfile
    profile = UserProfile.objects.filter(certificate_code=code).select_related('user').first()
    if not profile:
        return render(request, 'core/certificate_verify.html', {'is_valid': False, 'code': code})
    return render(request, 'core/certificate_verify.html', {
        'is_valid': True,
        'code': code,
        'username': profile.user.username,
        'issued_at': profile.certificate_issued_at,
        'points': profile.total_points,
    })
