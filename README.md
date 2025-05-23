# Recipe Management Application

A Django-based recipe management application with GraphQL API support.

## Features

- Create, update, and delete ingredients
- List ingredients with filtering and pagination
- Create recipes with multiple ingredients
- View recipe details with ingredient count
- Add/remove ingredients from recipes
- JWT-based authentication

## Setup

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

### Docker Setup

1. Build the Docker image:
```bash
docker build -t recipe-manager .
```

2. Run the Docker container:
```bash
docker run -p 8000:8000 recipe-manager
```

## API Usage

### Authentication

1. Get JWT token:
```bash
curl -X POST http://localhost:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin"}'
```

2. Use the token in GraphQL requests:
```bash
curl -X POST http://localhost:8000/graphql/ \
     -H "Authorization: Bearer your_token" \
     -H "Content-Type: application/json" \
     -d '{"query": "your_graphql_query"}'
```

### Example GraphQL Queries

1. List all ingredients:
```graphql
query {
  ingredients {
    id
    name
    unit
  }
}
```

2. Create a recipe with ingredients:
```graphql
mutation {
  createRecipe(
    input: {
      name: "Pasta Carbonara"
      description: "Classic Italian pasta dish"
      ingredients: [1, 2, 3]
    }
  ) {
    recipe {
      id
      name
      ingredientCount
    }
  }
}
```

====================================================================================
1. To run the graphql without UI and Postman I have added 1 run_graphql_queries.py File so you can Run that file too.
## License

Only Tests and code cleaning things done by the ChatGPT 
