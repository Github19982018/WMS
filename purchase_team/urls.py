from django.urls import path
from purchase_team import views

urlpatterns = [
    path('approve/',views.approve),
    path('front/approve',views.front_approve),
]