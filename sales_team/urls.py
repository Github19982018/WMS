from django.urls import path
from sales_team import views

urlpatterns = [
    path('packages/approve/',views.backend_package_approve),
    path('packages/cancel/',views.package_cancel),
    path('packages/front/approve/',views.frontend_package_approve),
    path('ships/approve/',views.backend_ship_approve),
    path('ships/cancel/',views.ship_cancel),
    path('ships/front/',views.frontend_ship_approve),
    path('packages/',views.packages,name='packages'),
    path('ships/',views.ships,name='ships'),
    path('packages/<int:id>',views.package,name='package'),
    path('ships/<int:id>',views.ship,name='ship'),
]