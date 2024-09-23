from django.urls import path
from sales_team import views

urlpatterns = [
    path('packages/approve/',views.backend_package_approve),
    path('packages/front/approve/',views.frontend_package_approve),
    path('ships/approve/',views.backend_ship_approve),
    path('ships/front/',views.frontend_ship_approve),
    path('packages',views.packages,name='packages'),
    path('ships',views.ships,name='ships'),
    path('package',views.package,name='package'),
    path('ship',views.ship,name='ship'),
]