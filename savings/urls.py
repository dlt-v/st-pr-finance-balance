from django.urls import path

from . import views

app_name = 'savings'
urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<int:entry_id>/', views.delete, name='delete'),
    path('edit/<int:entry_id>/', views.edit, name='edit'),
]
