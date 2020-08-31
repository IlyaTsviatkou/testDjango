from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Player

class StudentForm(forms.ModelForm):
    class Meta:
        model=Player
        fields = ['name','age','org']
    def tostr(self,name,age):
        return str(name + age)


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password','email')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    def correct_password(self):
        password_value = self.data["password"]
        password_repeat = self.data["password_repeat"]
        if password_repeat == password_value:
            return True
        return False
    def error_value(self):
        user_value = self.data["username"]
        mail = self.data["mail"]
        if User.objects.filter(email__iexact=mail).exists():
            return "error_mail", "Данная почта уже сужествует"
        if User.objects.filter(username__iexact=user_value).exists():
            return "error_name", "Данное имя уже сужествует"
        if not self.correct_password():
            return "error_password", "Пароли не совпадают"
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user