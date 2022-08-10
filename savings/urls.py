from django.urls import path

from . import views
app_name = 'savings'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:entry_id>/', views.detail, name='detail')
]
