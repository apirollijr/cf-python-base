import mysql.connector

# Initialize connection object
conn = mysql.connector.connect(
    host='localhost',
    user='admin',
    passwd='admin'
)

# Initialize cursor object
cursor = conn.cursor()

# Create database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

# Access the database
cursor.execute("USE task_database")

# Create Recipes table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS Recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    ingredients VARCHAR(255),
    cooking_time INT,
    difficulty VARCHAR(20)
)
""")

print("Database and table setup completed successfully!")

def calculate_difficulty(cooking_time, ingredients):
    """
    Calculate recipe difficulty based on cooking time and number of ingredients
    
    Args:
        cooking_time (int): Cooking time in minutes
        ingredients (list): List of ingredients
    
    Returns:
        str: Difficulty level (Easy, Medium, Intermediate, or Hard)
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

def create_recipe(conn, cursor):
    """Function to create a new recipe"""
    print("\n--- Creating a New Recipe ---")
    
    # Collect recipe details from user
    name = input("Enter the recipe name: ")
    
    # Get cooking time with validation
    while True:
        try:
            cooking_time = int(input("Enter cooking time (in minutes): "))
            break
        except ValueError:
            print("Please enter a valid number for cooking time.")
    
    # Collect ingredients
    ingredients = []
    print("Enter ingredients (type 'done' when finished):")
    while True:
        ingredient = input("Enter an ingredient: ").strip()
        if ingredient.lower() == 'done':
            break
        if ingredient:  # Only add non-empty ingredients
            ingredients.append(ingredient)
    
    # Calculate difficulty
    difficulty = calculate_difficulty(cooking_time, ingredients)
    
    # Convert ingredients list to comma-separated string
    ingredients_str = ", ".join(ingredients)
    
    # Build and execute SQL query
    query = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    values = (name, ingredients_str, cooking_time, difficulty)
    
    try:
        cursor.execute(query, values)
        conn.commit()
        print(f"\nRecipe '{name}' with difficulty '{difficulty}' has been successfully added to the database!")
    except mysql.connector.Error as err:
        print(f"Error adding recipe: {err}")
        conn.rollback()

def search_recipe(conn, cursor):
    """Function to search for recipes by ingredient"""
    print("\n--- Search for Recipes by Ingredient ---")
    
    # Get all ingredients from the database
    try:
        cursor.execute("SELECT ingredients FROM Recipes")
        results = cursor.fetchall()
        
        if not results:
            print("No recipes found in the database. Please add some recipes first.")
            return
        
        # Extract all unique ingredients
        all_ingredients = []
        for row in results:
            ingredients_str = row[0]  # Get the ingredients string from the tuple
            # Split the ingredients string by comma and strip whitespace
            ingredients_list = [ingredient.strip() for ingredient in ingredients_str.split(',')]
            
            # Add each ingredient to all_ingredients if not already present
            for ingredient in ingredients_list:
                if ingredient and ingredient not in all_ingredients:
                    all_ingredients.append(ingredient)
        
        # Sort ingredients alphabetically for better display
        all_ingredients.sort()
        
        # Display all ingredients to the user
        print("\nAvailable ingredients:")
        print("-" * 30)
        for i, ingredient in enumerate(all_ingredients, 1):
            print(f"{i}. {ingredient}")
        print("-" * 30)
        
        # Get user's choice
        while True:
            try:
                choice = int(input(f"Pick an ingredient to search for (1-{len(all_ingredients)}): "))
                if 1 <= choice <= len(all_ingredients):
                    search_ingredient = all_ingredients[choice - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(all_ingredients)}.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Search for recipes containing the selected ingredient
        search_query = "SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes WHERE ingredients LIKE %s"
        search_pattern = f"%{search_ingredient}%"
        
        cursor.execute(search_query, (search_pattern,))
        recipe_results = cursor.fetchall()
        
        # Display the results
        if recipe_results:
            print(f"\nRecipes containing '{search_ingredient}':")
            print("="*60)
            for recipe in recipe_results:
                recipe_id, name, ingredients, cooking_time, difficulty = recipe
                print(f"ID: {recipe_id}")
                print(f"Name: {name}")
                print(f"Ingredients: {ingredients}")
                print(f"Cooking Time: {cooking_time} minutes")
                print(f"Difficulty: {difficulty}")
                print("-"*40)
        else:
            print(f"\nNo recipes found containing '{search_ingredient}'.")
    
    except mysql.connector.Error as err:
        print(f"Error searching for recipes: {err}")

def update_recipe(conn, cursor):
    """Function to update an existing recipe"""
    print("\n--- Update an Existing Recipe ---")
    
    try:
        # Fetch all recipes from the database
        cursor.execute("SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes")
        recipes = cursor.fetchall()
        
        if not recipes:
            print("No recipes found in the database. Please add some recipes first.")
            return
        
        # Display all recipes to the user
        print("\nAvailable recipes:")
        print("="*80)
        for recipe in recipes:
            recipe_id, name, ingredients, cooking_time, difficulty = recipe
            print(f"ID: {recipe_id}")
            print(f"Name: {name}")
            print(f"Ingredients: {ingredients}")
            print(f"Cooking Time: {cooking_time} minutes")
            print(f"Difficulty: {difficulty}")
            print("-"*40)
        
        # Get user's choice for which recipe to update
        while True:
            try:
                recipe_id = int(input("Enter the ID of the recipe you want to update: "))
                # Check if the recipe ID exists
                recipe_exists = any(recipe[0] == recipe_id for recipe in recipes)
                if recipe_exists:
                    break
                else:
                    print("Recipe ID not found. Please enter a valid ID.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Get the current recipe data
        selected_recipe = next(recipe for recipe in recipes if recipe[0] == recipe_id)
        current_name, current_ingredients, current_cooking_time, current_difficulty = selected_recipe[1:]
        
        # Display update options
        print("\nWhich column would you like to update?")
        print("1. Name")
        print("2. Cooking Time")
        print("3. Ingredients")
        
        while True:
            try:
                column_choice = int(input("Enter your choice (1-3): "))
                if 1 <= column_choice <= 3:
                    break
                else:
                    print("Please enter a number between 1 and 3.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Collect new value based on user's choice
        if column_choice == 1:
            # Update name
            new_value = input("Enter the new recipe name: ").strip()
            if new_value:
                update_query = "UPDATE Recipes SET name = %s WHERE id = %s"
                cursor.execute(update_query, (new_value, recipe_id))
                print(f"Recipe name updated to '{new_value}'")
            else:
                print("Name cannot be empty. No changes made.")
                return
                
        elif column_choice == 2:
            # Update cooking time
            while True:
                try:
                    new_cooking_time = int(input("Enter the new cooking time (in minutes): "))
                    break
                except ValueError:
                    print("Please enter a valid number for cooking time.")
            
            # Update cooking time
            update_query = "UPDATE Recipes SET cooking_time = %s WHERE id = %s"
            cursor.execute(update_query, (new_cooking_time, recipe_id))
            
            # Recalculate difficulty since cooking time changed
            ingredients_list = [ingredient.strip() for ingredient in current_ingredients.split(',')]
            new_difficulty = calculate_difficulty(new_cooking_time, ingredients_list)
            
            # Update difficulty
            difficulty_query = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
            cursor.execute(difficulty_query, (new_difficulty, recipe_id))
            
            print(f"Cooking time updated to {new_cooking_time} minutes")
            print(f"Difficulty recalculated to '{new_difficulty}'")
            
        elif column_choice == 3:
            # Update ingredients
            print("Enter new ingredients (type 'done' when finished):")
            new_ingredients = []
            while True:
                ingredient = input("Enter an ingredient: ").strip()
                if ingredient.lower() == 'done':
                    break
                if ingredient:
                    new_ingredients.append(ingredient)
            
            if new_ingredients:
                # Convert ingredients list to comma-separated string
                new_ingredients_str = ", ".join(new_ingredients)
                
                # Update ingredients
                update_query = "UPDATE Recipes SET ingredients = %s WHERE id = %s"
                cursor.execute(update_query, (new_ingredients_str, recipe_id))
                
                # Recalculate difficulty since ingredients changed
                new_difficulty = calculate_difficulty(current_cooking_time, new_ingredients)
                
                # Update difficulty
                difficulty_query = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
                cursor.execute(difficulty_query, (new_difficulty, recipe_id))
                
                print(f"Ingredients updated to: {new_ingredients_str}")
                print(f"Difficulty recalculated to '{new_difficulty}'")
            else:
                print("No ingredients entered. No changes made.")
                return
        
        # Commit all changes
        conn.commit()
        print("\nRecipe updated successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error updating recipe: {err}")
        conn.rollback()

def delete_recipe(conn, cursor):
    """Function to delete a recipe"""
    print("\n--- Delete a Recipe ---")
    
    try:
        # Fetch all recipes from the database
        cursor.execute("SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes")
        recipes = cursor.fetchall()
        
        if not recipes:
            print("No recipes found in the database. Nothing to delete.")
            return
        
        # Display all recipes to the user
        print("\nAvailable recipes:")
        print("="*80)
        for recipe in recipes:
            recipe_id, name, ingredients, cooking_time, difficulty = recipe
            print(f"ID: {recipe_id}")
            print(f"Name: {name}")
            print(f"Ingredients: {ingredients}")
            print(f"Cooking Time: {cooking_time} minutes")
            print(f"Difficulty: {difficulty}")
            print("-"*40)
        
        # Get user's choice for which recipe to delete
        while True:
            try:
                recipe_id = int(input("Enter the ID of the recipe you want to delete: "))
                # Check if the recipe ID exists
                recipe_exists = any(recipe[0] == recipe_id for recipe in recipes)
                if recipe_exists:
                    break
                else:
                    print("Recipe ID not found. Please enter a valid ID.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Get the recipe name for confirmation
        selected_recipe = next(recipe for recipe in recipes if recipe[0] == recipe_id)
        recipe_name = selected_recipe[1]
        
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete '{recipe_name}'? (y/n): ").lower().strip()
        
        if confirm == 'y' or confirm == 'yes':
            # Build and execute DELETE query
            delete_query = "DELETE FROM Recipes WHERE id = %s"
            cursor.execute(delete_query, (recipe_id,))
            
            # Commit the changes
            conn.commit()
            
            print(f"\nRecipe '{recipe_name}' has been successfully deleted from the database!")
        else:
            print("Deletion cancelled.")
            
    except mysql.connector.Error as err:
        print(f"Error deleting recipe: {err}")
        conn.rollback()

def main_menu(conn, cursor):
    """Main menu function with user options"""
    
    while True:
        print("\n" + "="*50)
        print("RECIPE MANAGEMENT SYSTEM - MAIN MENU")
        print("="*50)
        print("Pick a choice:")
        print("1. Create a new recipe")
        print("2. Search for recipes by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("5. Exit")
        print("-"*50)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == '5':
            print("\nExiting the program...")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1-5.")
    
    # Commit any changes and close connections
    conn.commit()
    cursor.close()
    conn.close()
    print("Connection closed. Goodbye!")

# Call the main menu
main_menu(conn, cursor)