from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Ingredient, Recipe, RecipeIngredient
from django.contrib.auth.models import User

# Create your tests here.

class RecipeAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.ingredient = Ingredient.objects.create(name='Test Ingredient', unit='g')
        self.recipe = Recipe.objects.create(name='Test Recipe', description='Test Description', created_by=self.user)

    def test_add_ingredient(self):
        url = reverse('recipe-add-ingredient', args=[self.recipe.id])
        data = {'ingredient_id': self.ingredient.id, 'quantity': 2.0}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RecipeIngredient.objects.count(), 1)

    def test_remove_ingredient(self):
        RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredient, quantity=1.0)
        url = reverse('recipe-remove-ingredient', args=[self.recipe.id])
        data = {'ingredient_id': self.ingredient.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RecipeIngredient.objects.count(), 0)

    def test_ingredient_not_found(self):
        url = reverse('recipe-add-ingredient', args=[self.recipe.id])
        data = {'ingredient_id': 999, 'quantity': 2.0}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_recipe_ingredient_not_found(self):
        url = reverse('recipe-remove-ingredient', args=[self.recipe.id])
        data = {'ingredient_id': 999}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
