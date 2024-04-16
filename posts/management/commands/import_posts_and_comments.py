import os
from django.core.management.base import BaseCommand, CommandError
from posts.services import importer as import_service


class Command(BaseCommand):
    help = 'This command is used to import posts and comments from the fake api and store it in postgres local database.'

    # this one only to limit the number of imports and mainly for test purposes
    def add_arguments(self, parser):
        parser.add_argument('limit', nargs='?', type=int)

    def handle(self, *args, **kwargs):
        print("Start importing posts and comments into local database...")
        limit = kwargs.get('limit')
        try:
            import_service.import_data(limit=limit)
            print('Finished importing posts and comments.')
        except Exception as e:
            raise CommandError(e)
