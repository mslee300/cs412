from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Post, Comment, Reply
from .models import University

# Registration Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

        error_messages = {
        "password_mismatch": "Passwords do not match.",
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        domain = email.split('@')[1]
        # Check if the email domain matches a university
        university = University.objects.filter(name__iexact=domain.split('.')[0]).first()
        if not university:
            raise forms.ValidationError("This email domain does not match any registered university.")
        return email

# Login Form
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # Replace username with email

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # Exclude images because they are handled separately

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
