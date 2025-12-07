from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up SQLAlchemy
# Database connection details
username = 'admin'
password = 'admin'
hostname = 'localhost'
database_name = 'task_database'

# Create engine object that connects to the database
engine = create_engine(f'mysql+pymysql://{username}:{password}@{hostname}/{database_name}')

# Create declarative base for model definitions
Base = declarative_base()

# Generate Session class and bind it to the engine
Session = sessionmaker(bind=engine)

# Initialize session object
session = Session()

# Define Recipe model
class Recipe(Base):
    """Recipe model for storing recipe information"""
    
    # Set table name
    __tablename__ = 'final_recipes'
    
    # Define table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))
    
    def __repr__(self):
        """Quick representation of the recipe"""
        return f"<Recipe(id={self.id}, name='{self.name}', difficulty='{self.difficulty}')>"
    
    def __str__(self):
        """Well-formatted string representation of the recipe"""
        output = "\n" + "="*50 + "\n"
        output += f"\t🍽️  RECIPE: {self.name.upper()}\n"
        output += "="*50 + "\n"
        output += f"📝 ID: {self.id}\n"
        output += f"⏰ Cooking Time: {self.cooking_time} minutes\n"
        output += f"🥘 Ingredients: {self.ingredients}\n"
        output += f"📊 Difficulty Level: {self.difficulty}\n"
        output += "="*50
        return output
    
    def calculate_difficulty(self):
        """
        Calculate difficulty based on cooking time and number of ingredients
        """
        # Get ingredients as list to count them
        ingredients_list = self.return_ingredients_as_list()
        num_ingredients = len(ingredients_list)
        
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        else:  # cooking_time >= 10 and num_ingredients >= 4
            self.difficulty = "Hard"
    
    def return_ingredients_as_list(self):
        """
        Return ingredients as a list, splitting by comma and space
        """
        if not self.ingredients or self.ingredients == "":
            return []
        else:
            return self.ingredients.split(", ")

# Create the table in the database
Base.metadata.create_all(engine)

print("SQLAlchemy setup completed successfully!")
print(f"Connected to database: {database_name}")
print("Recipe model and table created successfully!")

# Main Operations Functions

def create_recipe():
    """Function to create a new recipe"""
    print("\n--- Creating a New Recipe ---")
    
    # Get recipe name with validation
    while True:
        name = input("Enter the recipe name: ").strip()
        if len(name) > 50:
            print("Recipe name must be 50 characters or less. Please try again.")
        elif len(name) == 0:
            print("Recipe name cannot be empty. Please try again.")
        else:
            break
    
    # Get cooking time with validation
    while True:
        cooking_time_input = input("Enter cooking time (in minutes): ").strip()
        if cooking_time_input.isnumeric():
            cooking_time = int(cooking_time_input)
            break
        else:
            print("Cooking time must be a number. Please try again.")
    
    # Collect ingredients
    ingredients = []
    while True:
        try:
            num_ingredients = int(input("How many ingredients would you like to enter? "))
            if num_ingredients > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    for i in range(num_ingredients):
        ingredient = input(f"Enter ingredient {i + 1}: ").strip()
        if ingredient:
            ingredients.append(ingredient)
    
    # Convert ingredients list to string
    ingredients_str = ", ".join(ingredients)
    
    # Create recipe entry
    recipe_entry = Recipe(
        name=name,
        ingredients=ingredients_str,
        cooking_time=cooking_time
    )
    
    # Calculate difficulty
    recipe_entry.calculate_difficulty()
    
    # Add to database
    session.add(recipe_entry)
    session.commit()
    
    print(f"\nRecipe '{name}' with difficulty '{recipe_entry.difficulty}' has been added successfully!")

def view_all_recipes():
    """Function to view all recipes"""
    print("\n--- All Recipes ---")
    
    # Retrieve all recipes
    all_recipes = session.query(Recipe).all()
    
    if not all_recipes:
        print("There are no entries in the database.")
        return None
    
    # Display each recipe
    for recipe in all_recipes:
        print(recipe)

def search_by_ingredients():
    """Function to search recipes by ingredients"""
    print("\n--- Search by Ingredients ---")
    
    # Check if table has any entries
    if session.query(Recipe).count() == 0:
        print("There are no entries in the database.")
        return None
    
    # Get all ingredients from database
    results = session.query(Recipe.ingredients).all()
    
    # Extract all unique ingredients
    all_ingredients = []
    for result in results:
        ingredients_list = result[0].split(", ")
        for ingredient in ingredients_list:
            if ingredient and ingredient not in all_ingredients:
                all_ingredients.append(ingredient)
    
    # Display ingredients with numbers
    print("\nAvailable ingredients:")
    for i, ingredient in enumerate(all_ingredients, 1):
        print(f"{i}. {ingredient}")
    
    # Get user selection
    try:
        selected_numbers = input("\nEnter the numbers of ingredients to search for (separated by spaces): ").split()
        selected_numbers = [int(num) for num in selected_numbers]
        
        # Validate selections
        for num in selected_numbers:
            if num < 1 or num > len(all_ingredients):
                print("Invalid selection. Please try again.")
                return None
        
        # Create search ingredients list
        search_ingredients = [all_ingredients[num - 1] for num in selected_numbers]
        
    except ValueError:
        print("Invalid input. Please enter numbers separated by spaces.")
        return None
    
    # Create search conditions
    conditions = []
    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"
        conditions.append(Recipe.ingredients.like(like_term))
    
    # Search for recipes
    from sqlalchemy import or_
    recipes_found = session.query(Recipe).filter(or_(*conditions)).all()
    
    if recipes_found:
        print(f"\nRecipes containing {', '.join(search_ingredients)}:")
        for recipe in recipes_found:
            print(recipe)
    else:
        print("No recipes found with the selected ingredients.")

def edit_recipe():
    """Function to edit an existing recipe"""
    print("\n--- Edit Recipe ---")
    
    # Check if any recipes exist
    if session.query(Recipe).count() == 0:
        print("There are no entries in the database.")
        return None
    
    # Get all recipe IDs and names
    results = session.query(Recipe.id, Recipe.name).all()
    
    # Display available recipes
    print("\nAvailable recipes:")
    for recipe_id, name in results:
        print(f"{recipe_id}. {name}")
    
    # Get user selection
    try:
        selected_id = int(input("\nEnter the ID of the recipe you want to edit: "))
        
        # Check if ID exists
        if not any(recipe_id == selected_id for recipe_id, _ in results):
            print("Recipe ID not found.")
            return None
            
    except ValueError:
        print("Invalid input. Please enter a valid ID.")
        return None
    
    # Retrieve the recipe to edit
    recipe_to_edit = session.query(Recipe).filter(Recipe.id == selected_id).first()
    
    # Display editable attributes
    print(f"\nEditing recipe: {recipe_to_edit.name}")
    print("1. Name:", recipe_to_edit.name)
    print("2. Ingredients:", recipe_to_edit.ingredients)
    print("3. Cooking Time:", recipe_to_edit.cooking_time, "minutes")
    
    # Get user choice
    try:
        choice = int(input("\nWhich attribute would you like to edit (1-3)? "))
        if choice not in [1, 2, 3]:
            print("Invalid choice.")
            return None
    except ValueError:
        print("Invalid input.")
        return None
    
    # Edit based on choice
    if choice == 1:
        # Edit name
        while True:
            new_name = input("Enter new name: ").strip()
            if len(new_name) > 50:
                print("Name must be 50 characters or less.")
            elif len(new_name) == 0:
                print("Name cannot be empty.")
            else:
                recipe_to_edit.name = new_name
                break
                
    elif choice == 2:
        # Edit ingredients
        ingredients = []
        try:
            num_ingredients = int(input("How many ingredients? "))
            for i in range(num_ingredients):
                ingredient = input(f"Enter ingredient {i + 1}: ").strip()
                if ingredient:
                    ingredients.append(ingredient)
            recipe_to_edit.ingredients = ", ".join(ingredients)
        except ValueError:
            print("Invalid number of ingredients.")
            return None
            
    elif choice == 3:
        # Edit cooking time
        while True:
            cooking_time_input = input("Enter new cooking time (minutes): ").strip()
            if cooking_time_input.isnumeric():
                recipe_to_edit.cooking_time = int(cooking_time_input)
                break
            else:
                print("Cooking time must be a number.")
    
    # Recalculate difficulty
    recipe_to_edit.calculate_difficulty()
    
    # Commit changes
    session.commit()
    print("Recipe updated successfully!")

def delete_recipe():
    """Function to delete a recipe"""
    print("\n--- Delete Recipe ---")
    
    # Check if any recipes exist
    if session.query(Recipe).count() == 0:
        print("There are no entries in the database.")
        return None
    
    # Get all recipe IDs and names
    results = session.query(Recipe.id, Recipe.name).all()
    
    # Display available recipes
    print("\nAvailable recipes:")
    for recipe_id, name in results:
        print(f"{recipe_id}. {name}")
    
    # Get user selection
    try:
        selected_id = int(input("\nEnter the ID of the recipe you want to delete: "))
        
        # Check if ID exists
        if not any(recipe_id == selected_id for recipe_id, _ in results):
            print("Recipe ID not found.")
            return None
            
    except ValueError:
        print("Invalid input. Please enter a valid ID.")
        return None
    
    # Get the recipe to delete
    recipe_to_delete = session.query(Recipe).filter(Recipe.id == selected_id).first()
    
    # Confirm deletion
    confirm = input(f"Are you sure you want to delete '{recipe_to_delete.name}'? (yes/no): ").lower().strip()
    
    if confirm == 'yes':
        session.delete(recipe_to_delete)
        session.commit()
        print("Recipe deleted successfully!")
    else:
        print("Deletion cancelled.")

# Main Menu
def main_menu():
    """Main menu loop"""
    while True:
        print("\n" + "="*50)
        print("RECIPE APPLICATION - MAIN MENU")
        print("="*50)
        print("Pick a choice:")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("Type 'quit' to quit the application")
        print("-"*50)
        
        choice = input("Enter your choice: ").strip().lower()
        
        if choice == '1':
            create_recipe()
        elif choice == '2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        elif choice == 'quit':
            print("\nClosing application...")
            break
        else:
            print("Invalid input. Please try again.")
    
    # Close session and engine
    session.close()
    engine.dispose()
    print("Session and engine closed. Goodbye!")

# Run the application
if __name__ == "__main__":
    main_menu()