from rest_framework.response import Response
from rest_framework import generics
from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import Group, User
from .serializers import (
    MenuItemSerializer,
    UserSerilializer,
    CategorySerializer,
    CartSerializer,
    OrderSerializer,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from rest_framework import status

from django.shortcuts import render
from .forms import MenuForm
from .models import Menu
from django.http import JsonResponse


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user.groups.filter(name="Manager").exists()
        )


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    search_fields = ["category__title"]
    ordering_fields = ["price", "inventory"]

    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [IsManager]

        return [permission() for permission in permission_classes]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [IsManager]

        return [permission() for permission in permission_classes]


class ManagerGroupView(generics.ListCreateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(groups__name="Manager")
        serializer = UserSerilializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data["username"])
        manager = Group.objects.get(name="Manager")
        manager.user_set.add(user)
        return Response({"message": "user added to the manager group"}, 200)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data["username"])
        manager = Group.objects.get(name="Manager")
        manager.user_set.remove(user)
        return Response({"message": "user removed from the manager group"}, 200)


class DeliveryCrewView(generics.ListCreateAPIView):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method != "GET":
            permission_classes = [IsManager | IsAdminUser]

        return [permission() for permission in permission_classes]

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(groups__name="Delivery crew")
        serializer = UserSerilializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data["username"])
        delivery_group = Group.objects.get(name="Delivery crew")
        delivery_group.user_set.add(user)
        return Response({"message": "user added to the delivery group"}, 200)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data["username"])
        manager = Group.objects.get(name="Delivery crew")
        manager.user_set.remove(user)
        return Response({"message": "user removed from the delivery group"}, 200)


class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=self.request.user).delete()
        return Response("Cart Emptied", 200)


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_total_price(self, user):
        total = 0
        items = Cart.objects.all().filter(user=user).all()
        for item in items.values():
            total += item["price"]
        return total

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.groups.count() == 0:  # normal customer - no group
            return Order.objects.all().filter(user=self.request.user)
        elif self.request.user.groups.filter(
            name="Delivery crew"
        ).exists():  # delivery crew
            return Order.objects.all().filter(
                delivery_crew=self.request.user
            )  # only show oreders assigned to him
        else:  # delivery crew or manager
            return Order.objects.all()

    def post(self, request):
        user = request.user
        cart_items = Cart.objects.all().filter(user=user).count()
        if cart_items == 0:
            return Response({"message:": "no item in cart"})

        data = request.data.copy()
        total = self.get_total_price(user)
        data["user"] = request.user.id
        data["total"] = total

        order_serializer = OrderSerializer(data=data)
        order_serializer.is_valid(raise_exception=True)
        order = order_serializer.save()
        # create order items
        items = Cart.objects.all().filter(user=user)
        for item in items.values():
            orderitem = OrderItem(
                order=order,
                menuitem_id=item["menuitem_id"],
                quantity=item["quantity"],
                price=item["price"],
            )

            orderitem.save()

        Cart.objects.all().filter(user=self.request.user).delete()

        return Response(order_serializer.data)


class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [IsManager | IsAdminUser]

        return [permission() for permission in permission_classes]

    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
