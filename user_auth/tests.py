from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Branch, Item, Material, Model_data, User, UserRole


class ItemMutationSafetyTests(APITestCase):
    def setUp(self):
        self.user_role = UserRole.objects.create(name="User")
        self.branch = Branch.objects.create(name="Main", code="MAIN")
        self.other_branch = Branch.objects.create(name="Other", code="OTHER")
        self.user = User.objects.create_user(
            email="user@example.com",
            username="user",
            password="password",
            first_name="Test",
            last_name="User",
            role=self.user_role,
            branch=self.branch,
        )
        self.model = Model_data.objects.create(name="Jersey")
        self.material = Material.objects.create(name="Cotton", model_id=self.model)
        self.item = Item.objects.create(
            name="Original",
            item_cost=Decimal("100.00"),
            material=self.material,
            branch=self.branch,
            is_sleeve="FULL SLEEVE",
            created_by=self.user,
        )

    def item_url(self, item):
        return reverse("item_detailed_list", kwargs={"item_id": item.id})

    def test_item_update_requires_authentication(self):
        response = self.client.put(self.item_url(self.item), {"name": "Changed"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Original")

    def test_partial_update_preserves_omitted_material_and_branch(self):
        self.client.force_authenticate(self.user)

        response = self.client.put(
            self.item_url(self.item),
            {"name": "Renamed", "item_cost": "125.00", "sleevecase": "HALF SLEEVE"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Renamed")
        self.assertEqual(self.item.item_cost, Decimal("125.00"))
        self.assertEqual(self.item.is_sleeve, "HALF SLEEVE")
        self.assertEqual(self.item.material_id, self.material.id)
        self.assertEqual(self.item.branch_id, self.branch.id)

    def test_user_cannot_update_another_branch_item(self):
        other_item = Item.objects.create(
            name="Private",
            item_cost=Decimal("200.00"),
            branch=self.other_branch,
        )
        self.client.force_authenticate(self.user)

        response = self.client.put(self.item_url(other_item), {"name": "Changed"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        other_item.refresh_from_db()
        self.assertEqual(other_item.name, "Private")

    def test_delete_requires_authentication(self):
        response = self.client.delete(self.item_url(self.item))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.item.refresh_from_db()
        self.assertTrue(self.item.is_active)
