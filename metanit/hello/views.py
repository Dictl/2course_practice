from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import UserPreferences
from .forms import CustomAuthenticationForm, CustomUserCreationForm

class ProfileEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']
        labels = {
            'first_name': 'Имя пользователя',
            'username': 'Логин',
            'email': 'Адрес электронной почты',
        }

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Аккаунт удалён')
        return redirect('login')
    return render(request, 'hello/delete_account_confirm.html')

@login_required
def profile_edit_view(request):

    preferences, created = UserPreferences.objects.get_or_create(
        user=request.user,
        defaults={'purpose': 'gaming', 'priority': 'balanced'}
    )
    
    if request.method == 'POST':
        # Обработка сохранения предпочтений
        if 'save_preferences' in request.POST:
            preferences.purpose = request.POST.get('purpose', 'gaming')
            preferences.priority = request.POST.get('priority', 'balanced')
            preferences.save()
            messages.success(request, 'Предпочтения сохранены')
            return redirect('profile_edit')
        
        # Обработка смены пароля
        if 'change_password' in request.POST:
            pwd_form = PasswordChangeForm(request.user, request.POST)
            if pwd_form.is_valid() and request.POST.get('confirm_change') == 'yes':
                user = pwd_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль успешно изменён')
                return redirect('profile_edit')
            else:
                messages.error(request, 'Ошибка смены пароля')
        
        # Обработка основной формы профиля
        else:
            form = ProfileEditForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Профиль обновлён')
                return redirect('profile_edit')
    else:
        form = ProfileEditForm(instance=request.user)
        pwd_form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
        'pwd_form': pwd_form,
        'user_preferences': preferences,
    }
    return render(request, 'hello/profile_edit.html', context)

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Создаем предпочтения при первом входе, если их нет
            UserPreferences.objects.get_or_create(user=user)
            
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
            user = form.save()
            
            # Создаем предпочтения по умолчанию для нового пользователя
            UserPreferences.objects.get_or_create(user=user)
            
            # Автоматический вход после регистрации
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
    if request.user.is_authenticated:
        preferences = UserPreferences.objects.get_or_create(
            user=request.user,
            defaults={'purpose': 'gaming', 'priority': 'balanced'}
        )[0]
    else:
        preferences = None
    
    context = {
        'user_preferences': preferences,
    }
    return render(request, 'hello/index.html', context)