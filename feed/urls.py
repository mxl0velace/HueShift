from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('makepiece', views.makepiece, name="makepiece"),
    path('artist/<str:username>',views.artist,name="artist"),
]