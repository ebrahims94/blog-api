from django.db import models
from .post import Post


class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(null=False, max_length=150, default='title')
    email = models.EmailField(max_length=250, null=False, default='user@blog.com')
    body = models.TextField(null=False, default='body')
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.name
