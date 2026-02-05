from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    path('student/menu/', views.student_menu, name='student_menu'),
    path('student/take-meal/<str:meal_type>/', views.student_take_meal, name='student_take_meal'),
    path('student/payment/', views.student_payment, name='student_payment'),
    path('student/subscription/', views.student_subscription, name='student_subscription'),
    path('student/reviews/', views.student_reviews, name='student_reviews'),
    path('student/reviews/add/<int:dish_id>/', views.student_add_review, name='student_add_review'),
    
    path('cook/', views.cook_dashboard, name='cook_dashboard'),
    path('cook/menu/', views.cook_menu, name='cook_menu'),
    path('cook/menu/create/', views.cook_menu_edit, name='cook_menu_create'),
    path('cook/menu/<int:menu_id>/edit/', views.cook_menu_edit, name='cook_menu_edit'),
    path('cook/dishes/', views.cook_dishes, name='cook_dishes'),
    path('cook/dishes/create/', views.cook_dish_edit, name='cook_dish_create'),
    path('cook/dishes/<int:dish_id>/edit/', views.cook_dish_edit, name='cook_dish_edit'),
    path('cook/products/', views.cook_products, name='cook_products'),
    path('cook/products/create/', views.cook_product_edit, name='cook_product_create'),
    path('cook/products/<int:product_id>/edit/', views.cook_product_edit, name='cook_product_edit'),
    path('cook/applications/', views.cook_applications, name='cook_applications'),
    path('cook/applications/create/', views.cook_application_create, name='cook_application_create'),
    
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/applications/', views.admin_applications, name='admin_applications'),
    path('admin-panel/applications/<int:app_id>/<str:action>/', views.admin_application_action, name='admin_application_action'),
    path('admin-panel/statistics/', views.admin_statistics, name='admin_statistics'),
    path('admin-panel/reports/', views.admin_reports, name='admin_reports'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/alergens/', views.admin_alergens, name='admin_alergens'),
]
