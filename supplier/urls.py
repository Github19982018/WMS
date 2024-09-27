from django.urls import path
from supplier import views

urlpatterns = [
    path('approve/',views.backend),
    path('cancel/',views.cancel),
    path('front/approve/',views.frontend),
    path('purchases/',views.purchases),
    path('purchases/<int:id>',views.purchase),
]