from datetime import date, datetime
from random import randint, choice

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from first_app.forms import CommentForm, ClickerForm
from first_app.models import CommentHistory, ExpHistory, studentHistory


def get_menu_context():
    return [
        {"name": "Home", "url": "/"},
        {"name": "Time", "url": "/time/"},
        {"name": "Calc", "url": "/calc/"},
        {"name": "Comment", "url": "/comment/"},
        {"name": "Riddle", "url": "/riddle/"},
        {"name": "Answer", "url": "/answer/"},
        {"name": "Multiply", "url": "/multiply/"},
        {"name": "Expression", "url": "/expression/"},
        {"name": "History", "url": "/history/"},
    ]


def index(request):
    contex = {
        'author': 'Maxim',
        'menu': get_menu_context()
    }

    return render(request, 'index.html', contex)


def time_page(request):
    contex = {
        'topic': 'Курс "Промышленное программирование"',
        'date_now': datetime.now().strftime('%m.%d.%Y'),
        'time_now': datetime.now().strftime('%H:%M:%S'),
        'menu': get_menu_context()
    }

    return render(request, 'time.html', contex)


def calc_page(request):
    a = int(request.GET.get("a", 0))
    b = int(request.GET.get("b", 0))
    contex = {
        'topic': 'Курс "Промышленное программирование"',
        'a': a,
        'b': b,
        'sum_num': a + b,
        'menu': get_menu_context()
    }

    return render(request, 'calc.html', contex)


@login_required
def comment_page(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            words = comment_form.cleaned_data['text']
            comment = CommentHistory(text=words, author=request.user)
            comment.save()
    else:
        comment_form = CommentForm()

    comments = CommentHistory.objects.filter(author=request.user).order_by('-create_at')

    context = {
        'comments': comments,
        'menu': get_menu_context(),
        'topic': 'Курс "Промышленное программирование"',
        'topic_2': 'Комментарии',
        'comment_form': comment_form,
    }
    return render(request, 'comment.html', context)


def riddle(request):
    context = {
        'topic': 'Курс "Промышленное программирование"',
        'riddle': 'What comes once in a minute, twice in a moment, but never in a thousand years?',
        'menu': get_menu_context()
    }

    return render(request, 'riddle.html', context)


def answer(request):
    context = {
        'topic': 'Курс "Промышленное программирование"',
        'answer': 'The letter M.',
        'menu': get_menu_context()
    }

    return render(request, 'answer.html', context)


def multiply(request):
    num = int(request.GET.get("num", 1))
    context = {
        'topic': 'Курс "Промышленное программирование"',
        'table': [f'{i} * {num} = {i * num}' for i in range(1, 11)],
        'menu': get_menu_context()
    }

    return render(request, 'multiply.html', context)


def expression(request):
    res = ''

    for i in range(randint(2, 4)):
        res += f'{randint(10, 99)}{choice([" + ", " - "])}'

    res = res[:-3]

    context = {
        'topic': 'Курс "Промышленное программирование"',
        'res': res,
        'answer': eval(res),
        'menu': get_menu_context()
    }

    if request.user.is_authenticated:
        obj = ExpHistory(res=res, solution=context['answer'], author=request.user)
        obj.save()

    return render(request, 'expression.html', context)


def history(request):
    all_obj = []

    if request.user.is_authenticated:
        all_obj = ExpHistory.objects.filter(author=request.user).order_by('-create_at')

    paginator = Paginator(all_obj, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'topic': 'Курс "Промышленное программирование"',
        'all_obj': all_obj,
        'menu': get_menu_context(),
        'page_obj': page_obj
    }

    return render(request, 'history.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def clicker(request):
    clicker_obj, created = studentHistory.objects.get_or_create(author=request.user)

    if request.method == "POST":
        form = ClickerForm(request.POST)
        if form.is_valid():
            clicker_obj.hp = form.cleaned_data['hp']
            clicker_obj.iq = form.cleaned_data['iq']
            clicker_obj.happi_index = form.cleaned_data['happi_index']
            clicker_obj.save()
    else:
        form = ClickerForm(initial={
            'hp': clicker_obj.hp,
            'iq': clicker_obj.iq,
            'happi_index': clicker_obj.happi_index
        })

    context = {
        'topic': 'СИМУЛЯЦИЯ СТУДЕНТА',
        'form': form,
    }

    return render(request, 'clicker.html', context)


