from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

app_name= 'myapp'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.loginpage, name='loginpage'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('registerpatient/', views.registerpatient, name='registerpatient'),
    path('predictionform/', views.predictionform, name='predictionform'),
    path('results/', views.results, name='results'),
    path('patientreport/', views.patientreport, name='patientreport'),
    path('logout/', views.logout, name='logout'),
    path('test/', views.test, name='test'),
    path('index/', views.index, name='index'),

    
]
urlpatterns += staticfiles_urlpatterns()


