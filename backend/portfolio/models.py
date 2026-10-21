from django.db import models


class Project(models.Model):
    DEMO_CHOICES = [
        ('', 'None'),
        ('weather', 'Live weather demo'),
        ('rag', 'RAG chatbot demo'),
    ]

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=120)
    tagline = models.CharField(max_length=200)
    role = models.CharField(max_length=60, default='Solo project')
    summary = models.TextField()
    highlights = models.JSONField(default=list, blank=True, help_text='List of strings')
    stack = models.JSONField(default=list, blank=True, help_text='List of strings')
    steps = models.JSONField(default=list, blank=True, help_text='List of strings (how it works)')
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    demo_kind = models.CharField(max_length=20, choices=DEMO_CHOICES, blank=True, default='')
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} <{self.email}>'
