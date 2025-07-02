from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))



from django import forms
from .models import GalleryItem

class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ['title', 'caption', 'image', 'link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title', 'required': 'required'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter caption'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Optional link'}),
        }


from django import forms
from .models import CKEditorContent

class CKEditorContentForm(forms.ModelForm):
    class Meta:
        model = CKEditorContent
        fields = ['title', 'content']
