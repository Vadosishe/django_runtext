from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name="home"),
    re_path(r"runtext=.*", views.generate_video),
    path("about", views.about, name="about"),
    path("documentation", views.documentation, name="docs"),
    path('', views.my_form_view, name='my_form'),

]
