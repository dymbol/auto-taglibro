from django.urls import path

from . import views

urlpatterns = [
    path('', views.car_list, name="index"),
    path('login', views.login_user, name="login_user"),
    path('logout', views.logoutuser, name="logoutuser"),
    path('car_list', views.car_list, name="car_list"),
    path('car/<int:car_id>', views.car, name="car"),
    path('milage/<int:car_id>', views.milage_list, name="milage"),
    path('update_milage/<int:car_id>', views.update_milage, name="update_milage"),
    path('plan/<int:car_id>', views.service_plan, name="service_plan"),
    path('actions/<int:car_id>', views.action_list, name="action_list"),
    path('action_list_by_tmpl/<int:tmplaction_id>', views.action_list_by_tmpl, name="action_list_by_tmpl"),
    path('files/<int:car_id>', views.files, name="files"),
    path('tmpl_action/<int:tmplaction_id>', views.tmpl_action, name="tmpl_action"),
    path('tmpl_action_add/<int:car_id>', views.add_tmpl_action, name="add_tmpl_action"),
    path('notify', views.send_notifications, name="send_notifications")


]
