from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('room/<str:pk>/',views.room,name='room'),
    path('createroom/',views.createroom,name='createroom'),
    path('updateroom/<str:pk>/',views.updateroom,name='updateroom'),
    path('deleteroom/<str:pk>/',views.deleteroom,name='deleteroom'),
    path('userlogin/',views.loginpage,name='loginpage'),
    path('userlogout/',views.logoutuser,name='logoutpage'),
    path('userregister/',views.registeruser,name='register'),
    path('deletemessage/<str:pk>/',views.deletemessage,name='delete-message'),
    path('userProfile/<str:pk>/',views.userprofile,name='user-profile'),
    path('update-user/',views.updateuser,name='update-user'),
    path('topics/',views.topicpage,name='topics'),
    path('activities/',views.activitypage,name='activities'),
]