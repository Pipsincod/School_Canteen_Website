from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Alergen, Reviews, Product, Dish, Menu


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите логин'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Введите пароль'})
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['login', 'email', 'name', 'birth_date', 'password1', 'password2']
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Логин'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ФИО'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Подтвердите пароль'})


class ProfileForm(forms.ModelForm):
    alergens_choices = forms.ModelMultipleChoiceField(
        queryset=Alergen.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-list'}),
        required=False,
        label='Аллергены'
    )
    
    class Meta:
        model = User
        fields = ['name', 'email', 'birth_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.alergens:
            selected_ids = self.instance.get_alergens_list()
            self.fields['alergens_choices'].initial = Alergen.objects.filter(id__in=selected_ids)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        selected = self.cleaned_data.get('alergens_choices', [])
        user.alergens = ','.join(str(a.id) for a in selected)
        if commit:
            user.save()
        return user


class PaymentForm(forms.Form):
    amount = forms.IntegerField(
        min_value=1,
        label='Сумма',
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Сумма пополнения'})
    )


class SubscriptionForm(forms.Form):
    DURATION_CHOICES = [
        (7, '1 неделя'),
        (14, '2 недели'),
        (30, '1 месяц'),
    ]
    MEAL_CHOICES = [
        ('breakfast', 'Только завтрак'),
        ('lunch', 'Только обед'),
        ('both', 'Завтрак и обед'),
    ]
    
    duration = forms.ChoiceField(
        choices=DURATION_CHOICES,
        label='Длительность',
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    meal_type = forms.ChoiceField(
        choices=MEAL_CHOICES,
        label='Тип питания',
        widget=forms.Select(attrs={'class': 'form-input'})
    )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['review', 'comment']
        widgets = {
            'review': forms.Select(attrs={'class': 'form-input'}),
            'comment': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Ваш комментарий...'}),
        }
        labels = {
            'review': 'Оценка',
            'comment': 'Комментарий',
        }


class DishForm(forms.ModelForm):
    products_choices = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-list'}),
        required=False,
        label='Продукты'
    )
    
    class Meta:
        model = Dish
        fields = ['name', 'price', 'amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-input'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.products:
            selected_ids = self.instance.get_products_list()
            self.fields['products_choices'].initial = Product.objects.filter(id__in=selected_ids)
    
    def save(self, commit=True):
        dish = super().save(commit=False)
        selected = self.cleaned_data.get('products_choices', [])
        dish.products = ','.join(str(p.id) for p in selected)
        if commit:
            dish.save()
        return dish


class MenuForm(forms.ModelForm):
    breakfast_dishes = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-list'}),
        required=False,
        label='Блюда на завтрак'
    )
    lunch_dishes = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-list'}),
        required=False,
        label='Блюда на обед'
    )
    
    class Meta:
        model = Menu
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            breakfast_ids = [int(x.strip()) for x in self.instance.breakfast.split(',') if x.strip().isdigit()]
            lunch_ids = [int(x.strip()) for x in self.instance.lunch.split(',') if x.strip().isdigit()]
            self.fields['breakfast_dishes'].initial = Dish.objects.filter(id__in=breakfast_ids)
            self.fields['lunch_dishes'].initial = Dish.objects.filter(id__in=lunch_ids)
    
    def save(self, commit=True):
        menu = super().save(commit=False)
        breakfast = self.cleaned_data.get('breakfast_dishes', [])
        lunch = self.cleaned_data.get('lunch_dishes', [])
        menu.breakfast = ','.join(str(d.id) for d in breakfast)
        menu.lunch = ','.join(str(d.id) for d in lunch)
        if commit:
            menu.save()
        return menu


class ProductForm(forms.ModelForm):
    alergens_choices = forms.ModelMultipleChoiceField(
        queryset=Alergen.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-list'}),
        required=False,
        label='Аллергены'
    )
    
    class Meta:
        model = Product
        fields = ['name', 'amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.alergens:
            selected_ids = self.instance.get_alergens_list()
            self.fields['alergens_choices'].initial = Alergen.objects.filter(id__in=selected_ids)
    
    def save(self, commit=True):
        product = super().save(commit=False)
        selected = self.cleaned_data.get('alergens_choices', [])
        product.alergens = ','.join(str(a.id) for a in selected)
        if commit:
            product.save()
        return product
