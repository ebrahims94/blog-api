from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from posts.models import Post

class ImportPostsAndCommandsTest(TestCase):
    def test_valid_command(self):
        " Test import posts and comments command."

        call_command('import_posts_and_comments', 1)

        data = Post.objects.all()
        self.assertIsNotNone(data)
    