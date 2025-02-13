from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # path('',views.index,name="index"),
    path('',views.IndexView.as_view(),name='index'),
    path('messages/',views.GlobeHistoryMessages.as_view(),name='load_messages'),
    path('send_message',views.MessageSent.as_view(),name='send_message'),
    path('test',views.test,name='test')
]
