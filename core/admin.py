from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Alergen, Product, Dish, Menu, Attendance, Payment, Subscription, Applications, Reviews


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('login', 'name', 'email', 'role', 'balance', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('login', 'name', 'email')
    ordering = ('login',)
    
    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        ('Личная информация', {'fields': ('name', 'email', 'birth_date', 'alergens')}),
        ('Роль и баланс', {'fields': ('role', 'balance')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'email', 'name', 'password1', 'password2', 'role'),
        }),
    )


@admin.register(Alergen)
class AlergenAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'amount', 'alergens')
    search_fields = ('name',)
    list_editable = ('amount',)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'amount')
    search_fields = ('name',)
    list_editable = ('price', 'amount')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('date', 'breakfast', 'lunch', 'given_breakfasts_amount', 'given_lunches_amount')
    list_filter = ('date',)
    date_hierarchy = 'date'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'meal_type')
    list_filter = ('date', 'meal_type')
    search_fields = ('user__name', 'user__login')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date', 'succesful')
    list_filter = ('date', 'succesful')
    search_fields = ('user__name',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_type', 'register_date', 'end_date', 'duration')
    list_filter = ('meal_type', 'register_date')
    search_fields = ('user__name',)


@admin.register(Applications)
class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'price', 'status')
    list_filter = ('status', 'date')
    search_fields = ('user__name',)
    list_editable = ('status',)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'dish', 'review', 'created_at')
    list_filter = ('review', 'created_at')
    search_fields = ('user__name', 'dish__name')
