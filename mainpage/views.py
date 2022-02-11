from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import DetailOfUser, Position, Subdivision
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from datetime import datetime
from django.contrib.auth.hashers import make_password

# Декоратор для проверки аутентификации пользователя
def is_authenticated(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'mainpage/not_authentificated.html')
    return wrapper

# Декоратор для проверки суперпользователя
def is_superuser(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return func(request, *args, **kwargs)
            else:
                return redirect('/')
        else:
            return render(request, 'mainpage/not_authentificated.html')
    return wrapper


@is_authenticated
def list_of_users(request):

    data = {
        'list': DetailOfUser.objects.all(),
    }

    return render(request, 'mainpage/list_of_users.html', data)

@is_authenticated
def positions(request):

    print('Привет')

    data = {
        'positions': Position.objects.all()
    }

    return render(request, 'mainpage/positions.html', data)

def index(request):

    data = {}

    if request.user.is_authenticated:
        try:
            data['user_name'] = DetailOfUser.objects.get(user=request.user).name
            data['user_surname'] = DetailOfUser.objects.get(user=request.user).surname
        except:
            data['user_name'] = {'username_name': 'No information!'}
            data['user_surname'] = {'username_surname': 'No information!'}

    return render(request, 'mainpage/index.html', data)

def login(request):

    data = {
        'error': '',
    }

    if not request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('nickname') != '' and request.POST.get('password') != '':
                user = authenticate(username=request.POST.get('nickname'), password=request.POST.get('password'))
                if user is not None:
                    if user.is_active:
                        print('Успешная авторизация')
                        auth_login(request, user)
                        return redirect('/')
                    else:
                        print('Пользователь отключен')
                        data['error'] = 'Пользователь отключен'
                else:
                    print('Логин или пароль неверны')
                    data['error'] = 'Логин или пароль неверны'

        return render(request, 'mainpage/login.html', data)   
    else:
        return redirect('/')
        
@is_authenticated
def logout(request):

    if request.GET.get('response') == 'True':
        auth_logout(request)
        return redirect('/')

    return render(request, 'mainpage/logout.html')

@is_superuser
def add_user(request):

    data = {
        'positions': Position.objects.all(),
        'subdivisions': Subdivision.objects.all(),
        'error': '',
    }

    if request.method == 'POST':

        name = request.POST.get('name')
        surname = request.POST.get('surname')
        patronymic = request.POST.get('patronymic')
        position = request.POST.get('position')
        date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d')
        subdivision = request.POST.get('subdivision')

        nickname = request.POST.get('nickname')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if name != '' and surname != '' and patronymic != '' and nickname != '' and password1 != '' and password2 != '':
            if password1 == password2:
                user, created = User.objects.get_or_create(username=nickname)
                if created:
                    user.password = make_password(password1)
                    detail_of_user = DetailOfUser.objects.create(user=User.objects.get(username=nickname), name=name, surname=surname, patronymic=patronymic, position=Position.objects.get(name=position), start_date=date, subdivision=Subdivision.objects.get(name=subdivision))
                return redirect('/')
            else:
                data['error'] = 'Пароли не совпадают'

    return render(request, 'mainpage/add_user.html', data)

@is_authenticated
def my_card(request):
    
    try:
        data = {
            'me': DetailOfUser.objects.get(user=request.user)
        }
    except:
        data = {
            'me': 'No information!'
        }

    return render(request, 'mainpage/my_card.html', data)

@is_superuser
def add_subdivision(request):

    data = {
        'error': ''
    }

    if request.method == 'POST':
        if request.POST.get('name') != '':
            Subdivision.objects.create(name=request.POST.get('name'))
            return redirect('/')
        else:
            data['error'] = 'Не было введено название отдела'
        

    return render(request, 'mainpage/add_subdivision.html', data)