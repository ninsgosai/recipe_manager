from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.unit})"

    class Meta:
        ordering = ['name']

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def ingredient_count(self):
        return self.ingredients.count()

    class Meta:
        ordering = ['-created_at']

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('recipe', 'ingredient')
