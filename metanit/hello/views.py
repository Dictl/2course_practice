from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Аккаунт удалён')
        return redirect('login')
    return render(request, 'hello/delete_account_confirm.html')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']
        labels = {
            'first_name': 'Имя пользователя',
            'username': 'Логин',
            'email': 'Адрес электронной почты',
        }

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        pwd_form = PasswordChangeForm(request.user, request.POST)
        change_password = 'change_password' in request.POST
        if change_password:
            if pwd_form.is_valid() and request.POST.get('confirm_change') == 'yes':
                user = pwd_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль успешно изменён')
                return redirect('profile_edit')
            else:
                messages.error(request, 'Ошибка смены пароля')
        else:
            if form.is_valid():
                form.save()
                messages.success(request, 'Профиль обновлён')
                return redirect('profile_edit')
    else:
        form = ProfileEditForm(instance=request.user)
        pwd_form = PasswordChangeForm(request.user)
    return render(request, 'hello/profile_edit.html', {'form': form, 'pwd_form': pwd_form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Неверный логин или пароль')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'hello/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = CustomUserCreationForm()
    return render(request, 'hello/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def index_view(request):
    return render(request, 'hello/index.html')

