from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import timedelta

from .models import User, Menu, Dish, Attendance, Payment, Subscription, Applications, Product, Reviews, Alergen
from .forms import (LoginForm, RegisterForm, ProfileForm, PaymentForm, 
                    SubscriptionForm, ReviewForm, DishForm, MenuForm, ProductForm)
from .decorators import student_required, cook_required, admin_required


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    
    return render(request, 'auth/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    
    return render(request, 'auth/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('login')


@login_required
def dashboard(request):
    if request.user.role == 'student':
        return redirect('student_menu')
    elif request.user.role == 'cook':
        return redirect('cook_dashboard')
    elif request.user.role == 'admin':
        return redirect('admin_dashboard')
    return redirect('login')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    
    user_alergens = []
    if request.user.alergens:
        ids = request.user.get_alergens_list()
        user_alergens = Alergen.objects.filter(id__in=ids)
    
    return render(request, 'profile.html', {
        'form': form,
        'user_alergens': user_alergens
    })


@login_required
@student_required
def student_menu(request):
    today = timezone.now().date()
    menu = Menu.objects.filter(date=today).first()
    
    breakfast_dishes = []
    lunch_dishes = []
    user_alergens = set(request.user.get_alergens_list())
    
    if menu:
        for dish in menu.get_breakfast_dishes():
            dish_alergens = set(dish.get_alergens())
            dish.has_allergen = bool(user_alergens & dish_alergens)
            breakfast_dishes.append(dish)
        
        for dish in menu.get_lunch_dishes():
            dish_alergens = set(dish.get_alergens())
            dish.has_allergen = bool(user_alergens & dish_alergens)
            lunch_dishes.append(dish)
    
    breakfast_taken = Attendance.objects.filter(
        user=request.user, date=today, meal_type='breakfast'
    ).exists()
    lunch_taken = Attendance.objects.filter(
        user=request.user, date=today, meal_type='lunch'
    ).exists()
    
    subscription = Subscription.objects.filter(
        user=request.user, end_date__gte=today
    ).first()
    
    return render(request, 'student/menu.html', {
        'menu': menu,
        'breakfast_dishes': breakfast_dishes,
        'lunch_dishes': lunch_dishes,
        'breakfast_taken': breakfast_taken,
        'lunch_taken': lunch_taken,
        'subscription': subscription,
        'today': today,
    })


@login_required
@student_required
def student_take_meal(request, meal_type):
    today = timezone.now().date()
    
    if Attendance.objects.filter(user=request.user, date=today, meal_type=meal_type).exists():
        messages.error(request, 'Вы уже получали это питание сегодня')
        return redirect('student_menu')
    
    subscription = Subscription.objects.filter(
        user=request.user, end_date__gte=today
    ).first()
    
    menu = Menu.objects.filter(date=today).first()
    if not menu:
        messages.error(request, 'Меню на сегодня не найдено')
        return redirect('student_menu')
    
    if meal_type == 'breakfast':
        dishes = menu.get_breakfast_dishes()
    else:
        dishes = menu.get_lunch_dishes()
    
    total_price = sum(d.price for d in dishes)
    
    has_subscription = subscription and (
        subscription.meal_type == 'both' or 
        subscription.meal_type == meal_type
    )
    
    if not has_subscription:
        if request.user.balance < total_price:
            messages.error(request, f'Недостаточно средств. Необходимо: {total_price} руб.')
            return redirect('student_menu')
        request.user.balance -= total_price
        request.user.save()
    
    Attendance.objects.create(
        user=request.user,
        date=today,
        meal_type=meal_type
    )
    
    if meal_type == 'breakfast':
        menu.given_breakfasts_amount += 1
    else:
        menu.given_lunches_amount += 1
    menu.save()
    
    messages.success(request, f'Питание ({meal_type}) получено!')
    return redirect('student_menu')


@login_required
@student_required
def student_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            Payment.objects.create(
                user=request.user,
                amount=amount,
                succesful=True
            )
            
            request.user.balance += amount
            request.user.save()
            
            messages.success(request, f'Баланс пополнен на {amount} руб.')
            return redirect('student_menu')
    else:
        form = PaymentForm()
    
    payments = Payment.objects.filter(user=request.user)[:10]
    
    return render(request, 'student/payment.html', {
        'form': form,
        'payments': payments
    })


@login_required
@student_required
def student_subscription(request):
    today = timezone.now().date()
    active_subscription = Subscription.objects.filter(
        user=request.user, end_date__gte=today
    ).first()
    
    PRICES = {
        ('7', 'breakfast'): 700,
        ('7', 'lunch'): 1000,
        ('7', 'both'): 1500,
        ('14', 'breakfast'): 1300,
        ('14', 'lunch'): 1900,
        ('14', 'both'): 2800,
        ('30', 'breakfast'): 2500,
        ('30', 'lunch'): 3800,
        ('30', 'both'): 5500,
    }
    
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            duration = int(form.cleaned_data['duration'])
            meal_type = form.cleaned_data['meal_type']
            
            price = PRICES.get((str(duration), meal_type), 0)
            
            if request.user.balance < price:
                messages.error(request, f'Недостаточно средств. Необходимо: {price} руб.')
                return redirect('student_subscription')
            
            request.user.balance -= price
            request.user.save()
            
            end_date = today + timedelta(days=duration)
            Subscription.objects.create(
                user=request.user,
                duration=duration,
                end_date=end_date,
                meal_type=meal_type
            )
            
            messages.success(request, f'Абонемент оформлен до {end_date}')
            return redirect('student_menu')
    else:
        form = SubscriptionForm()
    
    return render(request, 'student/subscription.html', {
        'form': form,
        'active_subscription': active_subscription,
        'prices': PRICES,
    })


@login_required
@student_required
def student_reviews(request):
    dishes = Dish.objects.all()
    user_reviews = {r.dish_id: r for r in Reviews.objects.filter(user=request.user)}
    
    for dish in dishes:
        dish.user_review = user_reviews.get(dish.id)
    
    return render(request, 'student/reviews.html', {'dishes': dishes})


@login_required
@student_required
def student_add_review(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    review = Reviews.objects.filter(user=request.user, dish=dish).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.dish = dish
            obj.save()
            messages.success(request, 'Отзыв сохранен')
            return redirect('student_reviews')
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'student/add_review.html', {
        'form': form,
        'dish': dish
    })


@login_required
@cook_required
def cook_dashboard(request):
    today = timezone.now().date()
    menu = Menu.objects.filter(date=today).first()
    low_stock = Product.objects.filter(amount__lt=10)
    my_applications = Applications.objects.filter(user=request.user)[:5]
    
    return render(request, 'cook/dashboard.html', {
        'menu': menu,
        'low_stock': low_stock,
        'my_applications': my_applications,
        'today': today,
    })


@login_required
@cook_required
def cook_menu(request):
    menus = Menu.objects.all()[:14]
    return render(request, 'cook/menu_list.html', {'menus': menus})


@login_required
@cook_required
def cook_menu_edit(request, menu_id=None):
    menu = get_object_or_404(Menu, id=menu_id) if menu_id else None
    
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            messages.success(request, 'Меню сохранено')
            return redirect('cook_menu')
    else:
        form = MenuForm(instance=menu)
    
    return render(request, 'cook/menu_edit.html', {'form': form, 'menu': menu})


@login_required
@cook_required
def cook_dishes(request):
    dishes = Dish.objects.all()
    return render(request, 'cook/dishes.html', {'dishes': dishes})


@login_required
@cook_required
def cook_dish_edit(request, dish_id=None):
    dish = get_object_or_404(Dish, id=dish_id) if dish_id else None
    
    if request.method == 'POST':
        form = DishForm(request.POST, instance=dish)
        if form.is_valid():
            form.save()
            messages.success(request, 'Блюдо сохранено')
            return redirect('cook_dishes')
    else:
        form = DishForm(instance=dish)
    
    return render(request, 'cook/dish_edit.html', {'form': form, 'dish': dish})


@login_required
@cook_required
def cook_products(request):
    products = Product.objects.all()
    return render(request, 'cook/products.html', {'products': products})


@login_required
@cook_required
def cook_product_edit(request, product_id=None):
    product = get_object_or_404(Product, id=product_id) if product_id else None
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт сохранен')
            return redirect('cook_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'cook/product_edit.html', {'form': form, 'product': product})


@login_required
@cook_required
def cook_applications(request):
    applications = Applications.objects.filter(user=request.user)
    return render(request, 'cook/applications.html', {'applications': applications})


@login_required
@cook_required
def cook_application_create(request):
    if request.method == 'POST':
        products_ids = request.POST.getlist('products')
        amounts = request.POST.get('amounts', '')
        price = request.POST.get('price', 0)
        
        if products_ids:
            Applications.objects.create(
                user=request.user,
                list_of_products=','.join(products_ids),
                amount_of_products=amounts,
                price=int(price) if price else 0
            )
            messages.success(request, 'Заявка создана')
            return redirect('cook_applications')
    
    products = Product.objects.all()
    return render(request, 'cook/application_create.html', {'products': products})


@login_required
@admin_required
def admin_dashboard(request):
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    stats = {
        'total_users': User.objects.filter(role='student').count(),
        'payments_week': Payment.objects.filter(date__gte=week_ago, succesful=True).aggregate(
            total=Sum('amount'))['total'] or 0,
        'attendance_today': Attendance.objects.filter(date=today).count(),
        'pending_applications': Applications.objects.filter(status='pending').count(),
    }
    
    pending = Applications.objects.filter(status='pending')[:5]
    
    return render(request, 'admin/dashboard.html', {
        'stats': stats,
        'pending_applications': pending,
        'today': today,
    })


@login_required
@admin_required
def admin_applications(request):
    applications = Applications.objects.all()
    return render(request, 'admin/applications.html', {'applications': applications})


@login_required
@admin_required
def admin_application_action(request, app_id, action):
    application = get_object_or_404(Applications, id=app_id)
    
    if action == 'approve':
        application.status = 'approved'
        for product, amount in application.get_products_with_amounts():
            product.amount += amount
            product.save()
        messages.success(request, 'Заявка одобрена, продукты добавлены на склад')
    elif action == 'reject':
        application.status = 'rejected'
        messages.info(request, 'Заявка отклонена')
    
    application.save()
    return redirect('admin_applications')


@login_required
@admin_required
def admin_statistics(request):
    today = timezone.now().date()
    month_ago = today - timedelta(days=30)
    
    payments = Payment.objects.filter(date__gte=month_ago, succesful=True)
    payments_total = payments.aggregate(total=Sum('amount'))['total'] or 0
    
    attendance = Attendance.objects.filter(date__gte=month_ago)
    attendance_by_type = attendance.values('meal_type').annotate(count=Count('id'))
    
    popular_dishes = Dish.objects.annotate(
        avg_rating=Sum('reviews__review') / Count('reviews')
    ).filter(reviews__isnull=False).order_by('-avg_rating')[:5]
    
    return render(request, 'admin/statistics.html', {
        'payments_total': payments_total,
        'payments_count': payments.count(),
        'attendance_by_type': attendance_by_type,
        'popular_dishes': popular_dishes,
        'month_ago': month_ago,
        'today': today,
    })


@login_required
@admin_required
def admin_reports(request):
    today = timezone.now().date()
    
    start_date = request.GET.get('start_date', (today - timedelta(days=30)).isoformat())
    end_date = request.GET.get('end_date', today.isoformat())
    
    payments = Payment.objects.filter(
        date__gte=start_date, date__lte=end_date, succesful=True
    )
    attendance = Attendance.objects.filter(
        date__gte=start_date, date__lte=end_date
    )
    applications = Applications.objects.filter(
        date__gte=start_date, date__lte=end_date, status='approved'
    )
    
    report = {
        'payments_total': payments.aggregate(total=Sum('amount'))['total'] or 0,
        'payments_count': payments.count(),
        'attendance_total': attendance.count(),
        'breakfasts': attendance.filter(meal_type='breakfast').count(),
        'lunches': attendance.filter(meal_type='lunch').count(),
        'expenses': applications.aggregate(total=Sum('price'))['total'] or 0,
    }
    
    return render(request, 'admin/reports.html', {
        'report': report,
        'start_date': start_date,
        'end_date': end_date,
    })


@login_required
@admin_required
def admin_users(request):
    users = User.objects.all().order_by('role', 'name')
    return render(request, 'admin/users.html', {'users': users})


@login_required
@admin_required
def admin_alergens(request):
    alergens = Alergen.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Alergen.objects.create(name=name)
            messages.success(request, 'Аллерген добавлен')
            return redirect('admin_alergens')
    
    return render(request, 'admin/alergens.html', {'alergens': alergens})
