from django.urls import path
from web import views

urlpatterns = [
    path('person/<int:pk>', views.person),
    path('title/<int:pk>', views.title),
    path('<slug:slug>', views.navigate),
]
