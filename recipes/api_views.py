from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Ingredient, Recipe, RecipeIngredient
from .serializers import IngredientSerializer, RecipeSerializer, RecipeIngredientSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def search(self, request):
        name = request.query_params.get('name', '')
        queryset = self.queryset.filter(name__icontains=name)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class AddIngredientSerializer(serializers.Serializer):
    ingredient_id = serializers.IntegerField(required=True)
    quantity = serializers.FloatField(required=False, default=1.0)

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['ingredient_id'],
            properties={
                'ingredient_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The ID of the ingredient to add.'),
                'quantity': openapi.Schema(type=openapi.TYPE_NUMBER, description='The quantity of the ingredient. Defaults to 1.0.')
            }
        )
    )
    @action(detail=True, methods=['post'])
    def add_ingredient(self, request, pk=None):
        serializer = AddIngredientSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        recipe = self.get_object()
        ingredient_id = serializer.validated_data['ingredient_id']
        quantity = serializer.validated_data.get('quantity', 1.0)
        
        try:
            ingredient = Ingredient.objects.get(id=ingredient_id)
            recipe_ingredient = RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=quantity
            )
            return Response(RecipeIngredientSerializer(recipe_ingredient).data)
        except Ingredient.DoesNotExist:
            return Response({'error': 'Ingredient not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['ingredient_id'],
            properties={
                'ingredient_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The ID of the ingredient to remove.')
            }
        )
    )
    @action(detail=True, methods=['post'])
    def remove_ingredient(self, request, pk=None):
        recipe = self.get_object()
        ingredient_id = request.data.get('ingredient_id')
        
        try:
            recipe_ingredient = RecipeIngredient.objects.get(recipe=recipe, ingredient_id=ingredient_id)
            recipe_ingredient.delete()
            return Response({'status': 'ingredient removed'})
        except RecipeIngredient.DoesNotExist:
            return Response({'error': 'Recipe ingredient not found'}, status=status.HTTP_404_NOT_FOUND) 