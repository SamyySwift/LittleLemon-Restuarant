from django.urls import path
from . import views


urlpatterns = [
    path("menu-items", views.MenuItemsView.as_view()),
    path("menu-items/<int:pk>", views.SingleMenuItemView.as_view()),
    path("menu-items/form", views.form_view),
    #     # path("throttle-check-auth/", views.throttle_check_auth),
    path("groups/manager/users", views.ManagerGroupView.as_view()),
    #     path("groups/manager/users/<int:manager_id>", views.single_manager),
    path("groups/delivery-crew/users", views.DeliveryCrewView.as_view()),
    #     path("groups/delivery-crew/users/<int:crew_id>", views.single_delivery_crew),
    path("cart/menu-items", views.CartView.as_view()),
    path("orders", views.OrderView.as_view()),
    path("orders/<int:pk>", views.SingleOrderView.as_view()),
]
