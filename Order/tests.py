from datetime import date
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user_auth.models import Branch, Customer, Item, Material, Model_data, User, UserRole
from .models import OrderItem, Orderdata


class OrderItemMutationSafetyTests(APITestCase):
    def setUp(self):
        role = UserRole.objects.create(name="User")
        self.branch = Branch.objects.create(name="Main", code="MAIN")
        self.user = User.objects.create_user(
            email="order-user@example.com",
            username="order-user",
            password="password",
            first_name="Order",
            last_name="User",
            role=role,
            branch=self.branch,
        )
        model = Model_data.objects.create(name="Jersey")
        self.material = Material.objects.create(name="Cotton", model_id=model)
        self.other_material = Material.objects.create(name="Polyester", model_id=model)
        self.item = Item.objects.create(
            name="Catalog item",
            item_cost=Decimal("100.00"),
            model=model,
            material=self.material,
            branch=self.branch,
            created_by=self.user,
        )
        customer = Customer.objects.create(
            name="Customer",
            address1="Address",
            mobile_number1="9999999999",
            created_by=self.user,
        )
        self.order = Orderdata.objects.create(
            orderID="ORDER-1",
            customer=customer,
            delivery_date=date.today(),
            created_by=self.user,
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            item=self.item,
            size="M",
            qty=1,
        )

    def test_order_update_requires_authentication(self):
        response = self.client.put(reverse("update-order-item"), {"orderID": self.order.id})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_update_does_not_mutate_master_item(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(
            reverse("update-order-item"),
            {
                "orderID": self.order.id,
                "items[0][item_id]": self.item.id,
                "items[0][material]": self.other_material.id,
                "items[0][qty]": 2,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.item.refresh_from_db()
        self.order_item.refresh_from_db()
        self.assertEqual(self.item.material_id, self.material.id)
        self.assertEqual(self.order_item.qty, 2)
