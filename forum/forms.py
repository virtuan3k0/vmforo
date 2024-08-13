from django import forms
from .models import PrivateMessage
from django.contrib.auth import get_user_model

User = get_user_model()

class PrivateMessageForm(forms.ModelForm):
    recipients = forms.CharField(widget=forms.Textarea, label='Recipients (comma separated)')
    content = forms.CharField(widget=forms.Textarea, label='Message Content')  # This will map to `encrypted_content`

    class Meta:
        model = PrivateMessage
        fields = ['recipients', 'title', 'content']

    def save(self, commit=True):
        recipients_usernames = self.cleaned_data['recipients'].split(',')
        recipients = User.objects.filter(username__in=[username.strip() for username in recipients_usernames])

        if recipients.count() != len(recipients_usernames):
            invalid_usernames = set(recipients_usernames) - set(recipients.values_list('username', flat=True))
            raise forms.ValidationError(f"No username found with the nickname(s): {', '.join(invalid_usernames)}")

        instance = PrivateMessage(
            sender=self.instance.sender,
            title=self.cleaned_data['title'],
            encrypted_content=self.cleaned_data['content'],  # Use content field as encrypted_content
        )

        if commit:
            instance.save()
            instance.recipients.set(recipients)  # Assign recipients after the instance is saved

        return instance
