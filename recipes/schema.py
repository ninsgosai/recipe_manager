import strawberry
from typing import List, Optional
from . import models
from .types import (
    IngredientType, RecipeType, RecipeIngredientType,
    IngredientInput, RecipeInput, RecipeIngredientInput, UpdateRecipeInput
)
from .serializers import IngredientSerializer, RecipeSerializer

@strawberry.type
class Query:
    @strawberry.field
    def ingredients(self, name: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> List[IngredientType]:
        queryset = models.Ingredient.objects.all()
        if name:
            queryset = queryset.filter(name__icontains=name)
        if offset is not None:
            queryset = queryset[offset:]
        if limit is not None:
            queryset = queryset[:limit]
        return queryset

    @strawberry.field
    def ingredient(self, id: int) -> Optional[IngredientType]:
        return models.Ingredient.objects.filter(id=id).first()

    @strawberry.field
    def recipes(self, name: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> List[RecipeType]:
        queryset = models.Recipe.objects.prefetch_related('recipeingredient_set__ingredient').all()
        if name:
            queryset = queryset.filter(name__icontains=name)
        if offset is not None:
            queryset = queryset[offset:]
        if limit is not None:
            queryset = queryset[:limit]
        return queryset

    @strawberry.field
    def recipe(self, id: int) -> Optional[RecipeType]:
        return models.Recipe.objects.prefetch_related('recipeingredient_set__ingredient').filter(id=id).first()

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_ingredient(self, input: IngredientInput) -> IngredientType:
        serializer = IngredientSerializer(data=input.__dict__)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @strawberry.mutation
    def update_ingredient(self, id: int, input: IngredientInput) -> Optional[IngredientType]:
        try:
            ingredient = models.Ingredient.objects.get(id=id)
            serializer = IngredientSerializer(ingredient, data=input.__dict__, partial=True)
            serializer.is_valid(raise_exception=True)
            return serializer.save()
        except models.Ingredient.DoesNotExist:
            return None

    @strawberry.mutation
    def delete_ingredient(self, id: int) -> bool:
        try:
            models.Ingredient.objects.get(id=id).delete()
            return True
        except models.Ingredient.DoesNotExist:
            return False

    @strawberry.mutation
    def create_recipe(self, input: RecipeInput, info) -> RecipeType:
        user = info.context.request.user
        recipe = models.Recipe.objects.create(
            name=input.name,
            description=input.description,
            created_by=user
        )
        for ingredient_id in input.ingredients:
            ingredient = models.Ingredient.objects.get(id=ingredient_id)
            models.RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=1.0  # Default quantity
            )
        return recipe

    @strawberry.mutation
    def update_recipe(self, id: int, input: UpdateRecipeInput) -> Optional[RecipeType]:
        try:
            recipe = models.Recipe.objects.get(id=id)
            if input.name is not None:
                recipe.name = input.name
            if input.description is not None:
                recipe.description = input.description
            recipe.save()

            if input.ingredients is not None:
                # Remove existing ingredients
                models.RecipeIngredient.objects.filter(recipe=recipe).delete()
                # Add new ingredients
                for ingredient_id in input.ingredients:
                    ingredient = models.Ingredient.objects.get(id=ingredient_id)
                    models.RecipeIngredient.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        quantity=1.0  # Default quantity
                    )
            return recipe
        except (models.Recipe.DoesNotExist, models.Ingredient.DoesNotExist):
            return None

    @strawberry.mutation
    def add_ingredient_to_recipe(self, input: RecipeIngredientInput) -> Optional[RecipeIngredientType]:
        try:
            recipe = models.Recipe.objects.get(id=input.recipe_id)
            ingredient = models.Ingredient.objects.get(id=input.ingredient_id)
            recipe_ingredient, created = models.RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient,
                defaults={'quantity': input.quantity}
            )
            if not created:
                recipe_ingredient.quantity = input.quantity
                recipe_ingredient.save()
            return recipe_ingredient
        except (models.Recipe.DoesNotExist, models.Ingredient.DoesNotExist):
            return None

    @strawberry.mutation
    def remove_ingredient_from_recipe(self, recipe_id: int, ingredient_id: int) -> bool:
        try:
            models.RecipeIngredient.objects.filter(
                recipe_id=recipe_id,
                ingredient_id=ingredient_id
            ).delete()
            return True
        except models.RecipeIngredient.DoesNotExist:
            return False

schema = strawberry.Schema(query=Query, mutation=Mutation) 