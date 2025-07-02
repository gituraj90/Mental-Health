from django import forms
from django.contrib.auth.models import User
from .models import ClientProfile
from django.contrib.auth.forms import UserCreationForm

class ClientSignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=100)
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['full_name', 'age', 'gender']



from django import forms
from .models import SupportPost, SupportReply

class SupportPostForm(forms.ModelForm):
    class Meta:
        model = SupportPost
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class SupportReplyForm(forms.ModelForm):
    class Meta:
        model = SupportReply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
