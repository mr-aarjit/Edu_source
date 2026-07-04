import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Group, Sub_group


@override_settings(
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    MEDIA_ROOT=tempfile.mkdtemp(),
    MIGRATION_MODULES={"App": None},
    ALLOWED_HOSTS=["*"],
)
class DownloadFileViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='secret')
        self.group = Group.objects.create(
            user=self.user,
            heading='Math Notes',
            description='A sample group',
        )
        self.file = SimpleUploadedFile(
            'sample.jpg',
            b'fake-image-bytes',
            content_type='image/jpeg',
        )
        self.sub_group = Sub_group.objects.create(
            user=self.user,
            heading='Photo',
            description='A sample file',
            group=self.group,
            file=self.file,
        )

    def test_download_view_returns_attachment_response(self):
        response = self.client.get(reverse('download_file', args=[self.sub_group.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/jpeg')
        self.assertIn('attachment; filename="sample.jpg"', response['Content-Disposition'])
        self.assertEqual(response.content, b'fake-image-bytes')
