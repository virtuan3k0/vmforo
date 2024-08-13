from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
import base64  # Add this import
import os
import uuid
from Crypto.Cipher import AES
from django.utils.text import slugify  # Add this import at the top of the file


User = get_user_model()

class Section(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:section_detail', kwargs={'slug': self.slug})

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    section = models.ForeignKey(Section, related_name='categories', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:category_detail', kwargs={'slug': self.slug})

class Thread(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.TextField()
    category = models.ForeignKey(Category, related_name='threads', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='threads', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1
            while Thread.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{uuid.uuid4().hex[:6]}'
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:thread_detail', kwargs={'slug': self.slug})

class Post(models.Model):
    thread = models.ForeignKey(Thread, related_name='posts', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Post by {self.author} in {self.thread}'

    def get_absolute_url(self):
        return reverse('forum:thread_detail', kwargs={'slug': self.thread.slug})

    def is_root(self):
        return self.parent is None

    def get_replies(self):
        return self.replies.all()

    def mark_as_edited(self):
        self.updated_at = timezone.now()
        self.save()

class PostLike(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='liked_posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

class PrivateMessage(models.Model):
    title = models.CharField(max_length=255)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipients = models.ManyToManyField(User, related_name='received_messages')
    encrypted_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.encrypted_content.startswith('ENC:'):
            self.encrypted_content = self.encrypt(self.encrypted_content)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Message from {self.sender} to {", ".join([user.username for user in self.recipients.all()])}'

    def encrypt(self, raw):
        raw = raw.ljust(16 * ((len(raw) + 15) // 16))
        key = os.environ.get('MESSAGE_ENCRYPTION_KEY')
        if not key:
            raise ValueError("Encryption key not set. Please set the MESSAGE_ENCRYPTION_KEY environment variable.")
        
        key_bytes = bytes.fromhex(key)
        iv = os.urandom(16)
        cipher = AES.new(key_bytes, AES.MODE_CFB, iv)
        encrypted = iv + cipher.encrypt(raw.encode('utf-8'))
        return 'ENC:' + base64.b64encode(encrypted).decode('utf-8')

    def decrypt(self):
        key_hex = os.environ.get('MESSAGE_ENCRYPTION_KEY')
        if not key_hex:
            raise ValueError("Encryption key not set. Please set the MESSAGE_ENCRYPTION_KEY environment variable.")
        
        key = bytes.fromhex(key_hex)

        try:
            if not self.encrypted_content.startswith('ENC:'):
                return self.encrypted_content

            encrypted_data = base64.b64decode(self.encrypted_content[4:])
            iv = encrypted_data[:16]
            cipher = AES.new(key, AES.MODE_CFB, iv)
            decrypted_bytes = cipher.decrypt(encrypted_data[16:])
            decrypted_message = decrypted_bytes.decode('utf-8').strip()
            return decrypted_message
        except (ValueError, UnicodeDecodeError) as e:
            return "Decryption error"

    def mark_as_read(self):
        if not self.read:
            self.read = True
            self.save()

    def get_absolute_url(self):
        return reverse('forum:message_detail', kwargs={'pk': self.pk})
