import requests

BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/login/"
GRAPHQL_URL = f"{BASE_URL}/graphql/"

def get_token():
    data = {"username": "admin", "password": "admin"}
    response = requests.post(LOGIN_URL, json=data)
    try:
        return response.json()["access"]
    except (KeyError, requests.exceptions.RequestException) as e:
        print("Error getting token:", e)
        return None

ACCESS_TOKEN = get_token()
if not ACCESS_TOKEN:
    print("Failed to get token. Exiting.")
    exit(1)

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def run_query(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    response = requests.post(GRAPHQL_URL, json=payload, headers=headers)
    try:
        print(f"Query: {query}\nResponse: {response.json()}\n")
    except requests.exceptions.JSONDecodeError:
        print(f"Query: {query}\nRaw response: {response.text}\n")

# 1. Create ingredient
run_query("""
mutation CreateIngredient($input: IngredientInput!) {
  createIngredient(input: $input) {
    id
    name
    unit
  }
}
""", variables={"input": {"name": "Salt", "unit": "g"}})

# 2. Query ingredients with pagination
run_query("""
query {
  ingredients(limit: 10, offset: 0) {
    id
    name
    unit
  }
}
""")

# 3. Create recipe with ingredients
run_query("""
mutation CreateRecipe($input: RecipeInput!) {
  createRecipe(input: $input) {
    id
    name
    description
    ingredientCount
    ingredients {
      id
      quantity
      ingredient {
        id
        name
      }
    }
  }
}
""", variables={"input": {
    "name": "Simple Salad",
    "description": "A simple salad recipe",
    "ingredients": [1, 2]  # Using IDs of existing ingredients
}})

# 4. Query recipes with search and pagination
run_query("""
query {
  recipes(name: "Salad", limit: 10, offset: 0) {
    id
    name
    description
    ingredientCount
    ingredients {
      id
      quantity
      ingredient {
        id
        name
      }
    }
  }
}
""")

# 5. Update recipe
run_query("""
mutation UpdateRecipe($id: Int!, $input: UpdateRecipeInput!) {
  updateRecipe(id: $id, input: $input) {
    id
    name
    description
    ingredientCount
    ingredients {
      id
      quantity
      ingredient {
        id
        name
      }
    }
  }
}
""", variables={
    "id": 1,
    "input": {
        "name": "Updated Salad",
        "description": "An updated salad recipe",
        "ingredients": [1, 2]
    }
})

# 6. Add ingredient to recipe
run_query("""
mutation AddIngredientToRecipe($input: RecipeIngredientInput!) {
  addIngredientToRecipe(input: $input) {
    id
    quantity
    ingredient {
      id
      name
    }
    recipe {
      id
      name
    }
  }
}
""", variables={"input": {"recipeId": 1, "ingredientId": 1, "quantity": 2.0}})

# 7. Remove ingredient from recipe
run_query("""
mutation RemoveIngredientFromRecipe($recipeId: Int!, $ingredientId: Int!) {
  removeIngredientFromRecipe(recipeId: $recipeId, ingredientId: $ingredientId)
}
""", variables={"recipeId": 1, "ingredientId": 1}) 