from django.urls import path
from apis import views

urlpatterns = [
    path('person/<int:pk>/', views.PersonDetail.as_view(), name='person_detail'),
    path('person/lookup/<name>/', views.PersonList.as_view(), name='person_lookup'),
    path('title/<int:pk>/', views.TitleDetail.as_view(), name='title_detail'),
]
