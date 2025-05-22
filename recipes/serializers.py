from rest_framework import serializers
from .models import Ingredient, Recipe, RecipeIngredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'unit', 'created_at', 'updated_at']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'recipe', 'ingredient', 'quantity', 'created_at', 'updated_at']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    ingredient_count = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'created_by', 'created_at', 'updated_at', 'ingredients', 'ingredient_count']

    def get_ingredient_count(self, obj):
        return obj.ingredient_count 