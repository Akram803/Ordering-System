from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView 
from .views import register, StuffOrderListView

app_name = "stuff"
urlpatterns = [
    path('logout/', LogoutView.as_view(template_name='users/logged-out.html') , name='logout'),
    path('login/', LoginView.as_view(template_name='users/login.html') , name='login'),    
    path('register/', register.as_view(), name='register'),

    path('order-list/', StuffOrderListView.as_view(), name='order-list')


]   