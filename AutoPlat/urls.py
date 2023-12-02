
from django.contrib import admin
from django.urls import path
from web.views import login
# from web.views import user_list
from web import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login/', login),
    path('user/', views.user),
    path('add/user/', views.add_user),
    path('delete/user/', views.delete_user),
    path('update/user/', views.update_user),
    path('phone/list/', views.phone_list),
    path('index/', views.index),
    path('depart/', views.depart),
    path('add/depart/', views.add_depart),
    path('delete/depart/', views.delete_depart),
    path('update/depart/', views.update_depart),
]
