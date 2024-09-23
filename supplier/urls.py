from django.urls import path
from sales_team import views

urlpatterns = [
    path('',views.backend),
    path('/front/',views.frontend),
]