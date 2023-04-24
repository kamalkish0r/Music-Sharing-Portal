from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, FileExtensionValidator
from .models import MusicFile
import re

class MusicFileForm(forms.ModelForm):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('protected', 'Protected')
    ]

    visibility = forms.ChoiceField(choices=VISIBILITY_CHOICES, initial='public')
    allowed_emails = forms.CharField(required=False, label='Allowed emails (comma-separated)')
    
    class Meta:
        model = MusicFile
        fields = ['file', 'visibility']
    
    def clean_allowed_emails(self):
        visibility = self.cleaned_data.get('visibility')
        allowed_emails = self.cleaned_data.get('allowed_emails')
        
        if visibility == MusicFile.PROTECTED and not allowed_emails:
            raise ValidationError("At least one email address is required for protected files.")
        
        if allowed_emails:
            # Split the entered email addresses by comma or newline character
            emails = re.split(',|\n', allowed_emails)
            validator = EmailValidator()
            cleaned_emails = []
            for email in emails:
                email = email.strip()
                try:
                    validator(email)
                    cleaned_emails.append(email)
                except ValidationError:
                    raise ValidationError("Please enter valid email addresses.")
                    
            # Remove any duplicates from the list of email addresses
            cleaned_emails = list(set(cleaned_emails))
            return cleaned_emails
        
        return None
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise ValidationError("Please select a file to upload.")
        
        file_ext = file.name.split('.')[-1]
        if file_ext not in MusicFile.ALLOWED_FILE_TYPES:
            raise ValidationError(f"File type not supported. Allowed file types are: {', '.join(MusicFile.ALLOWED_FILE_TYPES)}")
        
        return file
    
    def clean(self):
        cleaned_data = super().clean()
        visibility = cleaned_data.get('visibility')
        allowed_emails = cleaned_data.get('allowed_emails')
        
        if visibility == MusicFile.PROTECTED and not allowed_emails:
            raise ValidationError("At least one email address is required for protected files.")
        
        return cleaned_data
