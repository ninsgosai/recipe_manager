from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'created_at', 'updated_at')
    search_fields = ('name', 'unit')

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'ingredient_count', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_by', 'created_at')

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity', 'created_at', 'updated_at')
    list_filter = ('recipe', 'ingredient')
