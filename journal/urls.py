from django.urls import path

from . import views

urlpatterns = [
    path('', views.car_list, name="index"),
    path('car_list', views.car_list, name="car_list"),
    path('car/<int:car_id>', views.car, name="car"),
    path('milage/<int:car_id>', views.milage_list, name="milage"),
    path('plan/<int:car_id>', views.service_plan, name="service_plan"),
    path('actions/<int:car_id>', views.action_list, name="action_list"),

]
