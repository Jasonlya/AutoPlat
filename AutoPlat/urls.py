
from django.contrib import admin
from django.urls import path
from web.views import login
from web import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', login),
    path('login/', login),
    path('home/', views.home),
    path('ylgl/', views.ylgl),
]
