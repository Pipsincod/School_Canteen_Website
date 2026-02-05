from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import User, Alergen, Product, Dish, Menu


class Command(BaseCommand):
    help = 'Создает демо-данные для тестирования'

    def handle(self, *args, **options):
        self.stdout.write('Создание демо-данных...')
        
        alergens = ['Глютен', 'Молочные продукты', 'Орехи', 'Яйца', 'Рыба', 'Соя']
        for name in alergens:
            Alergen.objects.get_or_create(name=name)
        
        products_data = [
            ('Молоко', '2', 50),
            ('Мука', '1', 30),
            ('Яйца', '4', 100),
            ('Масло сливочное', '2', 20),
            ('Курица', '', 25),
            ('Рис', '', 40),
            ('Овощи', '', 60),
            ('Хлеб', '1', 50),
            ('Сыр', '2', 15),
            ('Макароны', '1', 35),
        ]
        for name, alergens_ids, amount in products_data:
            Product.objects.get_or_create(name=name, defaults={'alergens': alergens_ids, 'amount': amount})
        
        dishes_data = [
            ('Каша овсяная', '1,2,4', 30, 50),
            ('Омлет', '3,4', 20, 60),
            ('Бутерброд с сыром', '8,9', 15, 40),
            ('Куриный суп', '5,7', 25, 80),
            ('Рис с курицей', '5,6', 20, 90),
            ('Макароны с сыром', '9,10', 18, 70),
            ('Салат овощной', '7', 22, 50),
            ('Компот', '', 50, 30),
        ]
        for name, products, amount, price in dishes_data:
            Dish.objects.get_or_create(name=name, defaults={'products': products, 'amount': amount, 'price': price})
        
        today = timezone.now().date()
        Menu.objects.get_or_create(
            date=today,
            defaults={'breakfast': '1,2,3,8', 'lunch': '4,5,7,8'}
        )
        
        if not User.objects.filter(login='admin').exists():
            User.objects.create_superuser(
                login='admin', email='admin@school.ru', password='admin123', name='Администратор Школы'
            )
        
        if not User.objects.filter(login='cook').exists():
            User.objects.create_user(
                login='cook', email='cook@school.ru', password='cook123',
                name='Иванова Мария Петровна', role='cook'
            )
        
        if not User.objects.filter(login='student').exists():
            User.objects.create_user(
                login='student', email='student@school.ru', password='student123',
                name='Петров Иван Сергеевич', role='student', balance=500, alergens='2,3'
            )
        
        self.stdout.write(self.style.SUCCESS('Демо-данные созданы'))
        self.stdout.write('Учетные записи: admin/admin123, cook/cook123, student/student123')
