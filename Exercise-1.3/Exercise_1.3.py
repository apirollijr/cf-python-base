# Initialize two empty lists
recipes_list = []
ingredients_list = []

# Define a function to take recipe input from user
def take_recipe():
    # Get recipe name from user
    name = input("Enter the recipe name: ")
    
    # Get cooking time from user and convert to integer
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    
    # Initialize ingredients list
    ingredients = []
    
    # Get ingredients from user
    print("Enter ingredients (type 'done' when finished):")
    while True:
        ingredient = input("Enter an ingredient: ")
        if ingredient.lower() == 'done':
            break
        ingredients.append(ingredient)
    
    # Create recipe dictionary
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients
    }
    
    return recipe

# Main section
n = int(input("How many recipes would you like to enter? "))

# Run loop n times to collect recipes
for i in range(n):
    # Get recipe from user
    recipe = take_recipe()
    
    # Process each ingredient in the recipe
    for ingredient in recipe['ingredients']:
        # Add ingredient to ingredients_list if not already present
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    
    # Add the recipe to recipes_list
    recipes_list.append(recipe)

# Display recipes with difficulty levels
print("\nRecipe List:")
print("=" * 50)

for recipe in recipes_list:
    # Determine difficulty based on cooking time and number of ingredients
    cooking_time = recipe['cooking_time']
    num_ingredients = len(recipe['ingredients'])
    
    if cooking_time < 10 and num_ingredients < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
    else:  # cooking_time >= 10 and num_ingredients >= 4
        difficulty = "Hard"
    
    # Display the recipe information
    print(f"Recipe: {recipe['name']}")
    print(f"Cooking Time (min): {recipe['cooking_time']}")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty level: {difficulty}")
    print("-" * 30)

# Display all ingredients in alphabetical order
print("\nAll Ingredients Available Across All Recipes:")
print("=" * 50)
ingredients_list.sort()  # Sort ingredients alphabetically
for ingredient in ingredients_list:
    print(ingredient)