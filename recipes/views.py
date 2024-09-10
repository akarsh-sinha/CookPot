from django.shortcuts import render
import requests

# Home View
def home(request):
    if request.method == "POST":
        # Get form data (selected ingredients, allergies, and meal type)
        selected_ingredients = request.POST.getlist('ingredients')
        allergies = request.POST.getlist('allergies')
        meal_type = request.POST.get('meal_type')

        # Prepare data for results view
        context = {
            'selected_ingredients': selected_ingredients,
            'allergies': allergies,
            'meal_type': meal_type
        }
        return render(request, 'recipes/results.html', context)

    return render(request, 'recipes/home.html')

# About View
def about(request):
    return render(request, 'recipes/about.html')

# Results View (Fetching Recipes)
def results(request):
    if request.method == "POST":
        # Get form data from the request
        selected_ingredients = request.POST.getlist('ingredients')
        allergies = request.POST.getlist('allergies')
        meal_type = request.POST.get('meal_type')

        # Format the ingredients and allergies for the API
        ingredients = ','.join(selected_ingredients)
        intolerances = ','.join(allergies)

        # Make API call to Spoonacular to search for recipes
        spoonacular_api_key = 'api_key'  # Replace with your actual Spoonacular API key
        url = f"https://api.spoonacular.com/recipes/complexSearch"
        params = {
            'apiKey': spoonacular_api_key,
            'includeIngredients': ingredients,
            'intolerances': intolerances,
            'type': meal_type,
            'number': 10  # Number of recipes to return
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            recipes = data.get('results', [])
        else:
            recipes = []

        # Render the results page with the list of recipes
        return render(request, 'recipes/results.html', {'recipes': recipes})

    return render(request, 'recipes/error.html', {'message': 'Invalid request method'})

# Recipe Detail View
def recipe_detail(request, recipe_id):
    # Fetch recipe details from Spoonacular API using the recipe ID
    spoonacular_api_key = 'api_key'  # Replace with your actual Spoonacular API key
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    response = requests.get(url, params={"apiKey": spoonacular_api_key})

    if response.status_code == 200:
        recipe_data = response.json()
        context = {
            'recipe': recipe_data,
        }
        return render(request, 'recipes/recipe_detail.html', context)
    else:
        return render(request, 'recipes/error.html', {'message': 'Failed to retrieve recipe details.'})
