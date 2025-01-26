from django.urls import path

from . import views

urlpatterns = [
    path('login',views.MyLoginView.as_view(),name='Authen.login'),
    path('register',views.RegisterView.as_view(),name='Authen.register'),
    path('logout',views.Mylogout,name='Authen.logout'),
]
