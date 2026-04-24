from django.contrib import admin
from .models import Lesson, Task, ChapterProgress, UserProfile, Submission


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'slug', 'chapter')
    list_display_links = ('title',)
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TaskInline]


@admin.register(ChapterProgress)
class ChapterProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'is_completed', 'best_score', 'completed_at')
    list_filter = ('is_completed',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_points', 'completed_percent', 'certificate_code', 'certificate_issued_at')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'is_success', 'created_at')
    list_filter = ('is_success', 'created_at')
