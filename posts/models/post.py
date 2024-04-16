from django.db import models


class Post(models.Model):
    # add default value with the user_id specified from task description
    user_id = models.IntegerField(null=False, default=99999942)
    title = models.CharField(max_length=250, null=False)
    body = models.CharField(max_length=500, null=False)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.title
