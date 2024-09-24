from django.urls import path
from purchase_team import views

urlpatterns = [
    path('',views.purchases),
    path('<int:id>/',views.purchase),
    path('approve/',views.approve),
    path('front/approve/',views.front_approve),
]