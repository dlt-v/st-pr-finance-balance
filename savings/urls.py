from django.urls import path

from . import views

app_name = 'savings'
urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<int:entry_id>/', views.delete, name='delete'),
    path('<int:entry_id>/', views.detail, name='detail')
]
