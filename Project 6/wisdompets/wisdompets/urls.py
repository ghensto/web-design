from django.contrib import admin
from django.urls import re_path
from adoption import views

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path(r'^$', views.home, name='home'),
    re_path(r'^adoption/(\d+)/', views.pet_detail, name='pet_detail')
]
