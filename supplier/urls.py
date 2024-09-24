from django.urls import path
from supplier import views

urlpatterns = [
    path('',views.backend),
    path('front/',views.frontend),
    path('purchases/',views.purchases),
    path('purchases/<int:id>',views.purchase),
]