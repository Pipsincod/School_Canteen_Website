from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, login, email, password=None, **extra_fields):
        if not login:
            raise ValueError('Логин обязателен')
        if not email:
            raise ValueError('Email обязателен')

        email = self.normalize_email(email)
        user = self.model(login=login, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(login, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('student', 'Ученик'),
        ('cook', 'Повар'),
        ('admin', 'Администратор'),
    ]

    email = models.EmailField('Email', unique=True)
    name = models.CharField('ФИО', max_length=255)
    login = models.CharField('Логин', max_length=100, unique=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, default='student')
    alergens = models.TextField('Аллергены', blank=True, default='')
    balance = models.IntegerField('Баланс', default=0)

    is_active = models.BooleanField('Активен', default=True)
    is_staff = models.BooleanField('Администратор', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'name']


class Alergen(models.Model):
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Аллерген'
        verbose_name_plural = 'Аллергены'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Название', max_length=200)
    alergens = models.TextField('Аллергены', blank=True, default='')
    amount = models.IntegerField('Количество', default=0)
    unit_measurement = models.IntegerField('Единица измерения', default=0)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f"{self.name} ({self.amount} {self.unit_measurement}.)"

    def get_alergens_list(self):
        if not self.alergens:
            return []
        return [int(x.strip()) for x in self.alergens.split(',') if x.strip().isdigit()]


class Dish(models.Model):
    name = models.CharField('Название', max_length=200)
    products = models.TextField('Продукты', blank=True, default='')
    amount = models.IntegerField('Количество порций', default=0)
    price = models.IntegerField('Цена', default=0)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name

    def get_products_list(self):
        if not self.products:
            return []
        return [int(x.strip()) for x in self.products.split(',') if x.strip().isdigit()]

    def get_alergens(self):
        alergens = set()
        for product_id in self.get_products_list():
            try:
                product = Product.objects.get(id=product_id)
                alergens.update(product.get_alergens_list())
            except Product.DoesNotExist:
                pass
        return list(alergens)


class Menu(models.Model):
    date = models.DateField('Дата', unique=True)
    breakfast = models.TextField('Завтрак', blank=True, default='')
    lunch = models.TextField('Обед', blank=True, default='')
    given_breakfasts_amount = models.IntegerField('Выдано завтраков', default=0)
    given_lunches_amount = models.IntegerField('Выдано обедов', default=0)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
        ordering = ['-date']

    def __str__(self):
        return f"Меню на {self.date}"

    def get_breakfast_dishes(self):
        if not self.breakfast:
            return []
        ids = [int(x.strip()) for x in self.breakfast.split(',') if x.strip().isdigit()]
        return Dish.objects.filter(id__in=ids)

    def get_lunch_dishes(self):
        if not self.lunch:
            return []
        ids = [int(x.strip()) for x in self.lunch.split(',') if x.strip().isdigit()]
        return Dish.objects.filter(id__in=ids)


class Attendance(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
    ]

    date = models.DateField('Дата')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    meal_type = models.CharField('Тип приема пищи', max_length=20, choices=MEAL_CHOICES, default='lunch')

    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'
        unique_together = ['date', 'user', 'meal_type']

    def __str__(self):
        return f"{self.user.name} - {self.date} ({self.get_meal_type_display()})"


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо')
    review = models.IntegerField('Оценка', choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField('Комментарий', blank=True, default='')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ['user', 'dish']

    def __str__(self):
        return f"{self.user.name} - {self.dish.name}: {self.review}/5"

