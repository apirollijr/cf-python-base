import pickle

def display_recipe(recipe):
    """
    Function to display a recipe with all its attributes
    Takes a recipe dictionary as argument and prints all details
    """
    print(f"Recipe: {recipe['name']}")
    print(f"Cooking Time (min): {recipe['cooking_time']}")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty level: {recipe['difficulty']}")
    print("-" * 40)

def search_ingredient(data):
    """
    Function to search for recipes containing a specific ingredient
    Takes a data dictionary as argument and allows user to search by ingredient
    """
    # Display all available ingredients with numbers
    print("Available ingredients:")
    print("-" * 30)
    all_ingredients = data['all_ingredients']
    
    for index, ingredient in enumerate(all_ingredients):
        print(f"{index}: {ingredient}")
    
    print("-" * 30)
    
    try:
        # Get user input for ingredient selection
        choice = int(input("Enter the number corresponding to the ingredient: "))
        ingredient_searched = all_ingredients[choice]
        
    except (ValueError, IndexError):
        # Handle incorrect input (non-integer or out of range)
        print("Incorrect input. Please enter a valid number from the list.")
        
    else:
        # Search for recipes containing the selected ingredient
        print(f"\nRecipes containing '{ingredient_searched}':")
        print("=" * 50)
        
        recipes_found = False
        for recipe in data['recipes_list']:
            if ingredient_searched in recipe['ingredients']:
                display_recipe(recipe)
                recipes_found = True
        
        if not recipes_found:
            print("No recipes found with this ingredient.")

# Main code
filename = input("Enter the filename that contains your recipe data: ")

try:
    # Open and load the recipe data file
    with open(filename, 'rb') as file:
        data = pickle.load(file)
        
except FileNotFoundError:
    # Handle case when file is not found
    print(f"File '{filename}' not found. Please make sure the file exists and try again.")
    
else:
    # If file loaded successfully, call search_ingredient function
    search_ingredient(data)