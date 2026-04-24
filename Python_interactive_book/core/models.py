from django.db import models
from django.contrib.auth.models import User

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)
    chapter = models.CharField(max_length=100, default='ООП')
    theory_html = models.TextField(blank=True, default='')
    starter_code = models.TextField(blank=True, default='')
    tests_inline = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'

class Task(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='tasks')
    prompt = models.TextField()
    points = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f'Task for {self.lesson.title} ({self.points} pts)'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    total_points = models.PositiveIntegerField(default=0)
    completed_percent = models.FloatField(default=0.0)
    certificate_code = models.CharField(max_length=64, blank=True, default='')
    certificate_issued_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Profile({self.user.username})'

class ChapterProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_items')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_items')
    is_completed = models.BooleanField(default=False)
    best_score = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        state = 'done' if self.is_completed else 'pending'
        return f'{self.user.username} -> {self.lesson.slug}: {state}'

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='submissions')
    code = models.TextField()
    is_success = models.BooleanField(default=False)
    output = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        state = 'ok' if self.is_success else 'fail'
        return f'Submission({self.user.username} - {self.lesson.slug} - {state})'