from django.urls import path

from . import views

urlpatterns=[
    path('',views.index, name='index'),
    path('game',views.game, name='game'),
    path('submit_quiz', views.submit_quiz, name='submit_quiz'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('speech-to-text/', views.speech_to_text, name='speech_to_text'),

]

