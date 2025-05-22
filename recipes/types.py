import strawberry
from typing import List, Optional
from . import models

@strawberry.type
class IngredientType:
    id: int
    name: str
    unit: str
    created_at: str
    updated_at: str

@strawberry.type
class RecipeIngredientType:
    id: int
    quantity: float
    ingredient: IngredientType
    recipe: 'RecipeType'

@strawberry.type
class RecipeType:
    id: int
    name: str
    description: str
    created_by: str
    created_at: str
    updated_at: str

    @strawberry.field
    def ingredients(self) -> List[RecipeIngredientType]:
        return models.RecipeIngredient.objects.filter(recipe_id=self.id).select_related('ingredient')

    @strawberry.field
    def ingredient_count(self) -> int:
        return models.RecipeIngredient.objects.filter(recipe_id=self.id).count()

@strawberry.input
class IngredientInput:
    name: str
    unit: str

@strawberry.input
class RecipeInput:
    name: str
    description: str
    ingredients: List[int]

@strawberry.input
class RecipeIngredientInput:
    recipe_id: int
    ingredient_id: int
    quantity: float

@strawberry.input
class UpdateRecipeInput:
    name: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[List[int]] = None  # List of ingredient IDs 