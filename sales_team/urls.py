from django.urls import path
from sales_team import views

urlpatterns = [
    path('packages/approve/',views.backend_package_approve),
    path('packages/front/approve/',views.frontend_package_approve),
]