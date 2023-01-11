from django.urls import path
from . import views

urlpatterns=[
    path('',views.apioverview,name='api-overview'),
    path('rooms/',views.getrooms,name='api-list'),
    path('rooms/<str:pk>',views.getroom,name='api-detail'),
]