import pickle

def calc_difficulty(cooking_time, ingredients):
    """
    Function to calculate recipe difficulty based on cooking time and number of ingredients
    """
    num_ingredients = len(ingredients)
    
    if cooking_time < 10 and num_ingredients < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
    else:  # cooking_time >= 10 and num_ingredients >= 4
        difficulty = "Hard"
    
    return difficulty

def take_recipe():
    """
    Function to take recipe input from user and return a recipe dictionary
    """
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
    
    # Calculate difficulty using calc_difficulty function
    difficulty = calc_difficulty(cooking_time, ingredients)
    
    # Create and return recipe dictionary
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients,
        'difficulty': difficulty
    }
    
    return recipe

# Main code
filename = input("Enter a filename to store your recipes: ")

try:
    # Attempt to open and load existing file
    file = open(filename, 'rb')
    data = pickle.load(file)
except FileNotFoundError:
    # File not found - create new data dictionary
    print("File not found. Creating a new recipe file.")
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
except:
    # Handle any other exceptions
    print("An error occurred. Creating a new recipe file.")
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
else:
    # Close the file if it was successfully opened
    file.close()
    print("File loaded successfully.")
finally:
    # Extract the values from dictionary into separate lists
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']

# Ask user how many recipes to enter
n = int(input("How many recipes would you like to enter? "))

# Loop to collect recipes
for i in range(n):
    print(f"\nEntering recipe {i + 1}:")
    # Get recipe from user
    recipe = take_recipe()
    
    # Add recipe to recipes_list
    recipes_list.append(recipe)
    
    # Add new ingredients to all_ingredients if not already present
    for ingredient in recipe['ingredients']:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

# Update the data dictionary with new recipes and ingredients
data = {
    'recipes_list': recipes_list,
    'all_ingredients': all_ingredients
}

# Save data to binary file
try:
    with open(filename, 'wb') as file:
        pickle.dump(data, file)
    print(f"\nRecipes successfully saved to {filename}!")
except:
    print(f"An error occurred while saving to {filename}.")