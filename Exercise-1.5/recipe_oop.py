class Recipe:
    """
    A class to represent a recipe with automatic difficulty calculation
    """
    
    # Class variable to track all ingredients across all recipes
    all_ingredients = []
    
    def __init__(self, name):
        """
        Initialize a Recipe object
        
        Args:
            name (str): The name of the recipe
        """
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = None
    
    # Getter and setter methods for name
    def get_name(self):
        """Get the recipe name"""
        return self.name
    
    def set_name(self, name):
        """Set the recipe name"""
        self.name = name
    
    # Getter and setter methods for cooking_time
    def get_cooking_time(self):
        """Get the cooking time"""
        return self.cooking_time
    
    def set_cooking_time(self, cooking_time):
        """Set the cooking time"""
        self.cooking_time = cooking_time
        self.calculate_difficulty()  # Recalculate difficulty when cooking time changes
    
    def add_ingredients(self, *ingredients):
        """
        Add ingredients to the recipe using variable-length arguments
        
        Args:
            *ingredients: Variable number of ingredient strings
        """
        for ingredient in ingredients:
            self.ingredients.append(ingredient)
        self.update_all_ingredients()
    
    def get_ingredients(self):
        """Get the ingredients list"""
        return self.ingredients
    
    def calculate_difficulty(self):
        """
        Calculate and set the difficulty of the recipe based on cooking time and ingredients
        
        Logic:
        - Easy: cooking_time < 10 minutes AND ingredients < 4
        - Medium: cooking_time < 10 minutes AND ingredients >= 4
        - Intermediate: cooking_time >= 10 minutes AND ingredients < 4
        - Hard: cooking_time >= 10 minutes AND ingredients >= 4
        """
        num_ingredients = len(self.ingredients)
        
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        else:  # cooking_time >= 10 and num_ingredients >= 4
            self.difficulty = "Hard"
    
    def get_difficulty(self):
        """
        Get the difficulty, calculating it first if not already done
        """
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty
    
    def search_ingredient(self, ingredient):
        """
        Search for an ingredient in the recipe
        
        Args:
            ingredient (str): The ingredient to search for
            
        Returns:
            bool: True if ingredient is found, False otherwise
        """
        return ingredient in self.ingredients
    
    def update_all_ingredients(self):
        """
        Update the class variable all_ingredients with ingredients from this recipe
        Adds ingredients that aren't already present in the class variable
        """
        for ingredient in self.ingredients:
            if ingredient not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)
    
    def __str__(self):
        """
        String representation of the recipe
        
        Returns:
            str: A well-formatted string containing all recipe information
        """
        output = f"Recipe: {self.name}\n"
        output += f"Cooking Time: {self.cooking_time} minutes\n"
        output += f"Ingredients: {', '.join(self.ingredients)}\n"
        output += f"Difficulty: {self.get_difficulty()}"
        return output


def recipe_search(data, search_term):
    """
    Search for recipes containing a specific ingredient
    
    Args:
        data (list): A list of Recipe objects to search from
        search_term (str): The ingredient to be searched for
    """
    print(f"Recipes containing '{search_term}':")
    print("=" * 40)
    
    found_recipes = False
    
    for recipe in data:
        # Use the search_ingredient method to check if ingredient is present
        if recipe.search_ingredient(search_term):
            print(recipe)
            print("-" * 40)
            found_recipes = True
    
    if not found_recipes:
        print("No recipes found with this ingredient.")
        print("-" * 40)


# Main code
if __name__ == "__main__":
    
    # Create Tea recipe
    tea = Recipe("Tea")
    tea.add_ingredients("Tea Leaves", "Sugar", "Water")
    tea.set_cooking_time(5)
    print(tea)
    print()
    
    # Create Coffee recipe
    coffee = Recipe("Coffee")
    coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
    coffee.set_cooking_time(5)
    print(coffee)
    print()
    
    # Create Cake recipe
    cake = Recipe("Cake")
    cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
    cake.set_cooking_time(50)
    print(cake)
    print()
    
    # Create Banana Smoothie recipe
    banana_smoothie = Recipe("Banana Smoothie")
    banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
    banana_smoothie.set_cooking_time(5)
    print(banana_smoothie)
    print()
    
    # Wrap recipes into a list
    recipes_list = [tea, coffee, cake, banana_smoothie]
    
    # Search for recipes containing specific ingredients
    print("="*60)
    print("RECIPE SEARCH RESULTS")
    print("="*60)
    print()
    
    # Search for Water
    recipe_search(recipes_list, "Water")
    print()
    
    # Search for Sugar
    recipe_search(recipes_list, "Sugar")
    print()
    
    # Search for Bananas
    recipe_search(recipes_list, "Bananas")
    print()
    
    # Display all ingredients across all recipes
    print("All ingredients used across all recipes:")
    print(", ".join(Recipe.all_ingredients))