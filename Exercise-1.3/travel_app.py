# Simple Travel App
# Practice with if-elif-else statements

print("Welcome to the Simple Travel App!")
print("=" * 40)

# Ask user where they want to travel
destination = input("Where would you like to travel? ").strip().lower()

# Define 3 travel destinations and check user input
if destination == "paris":
    print("Enjoy your stay in Paris!")
elif destination == "tokyo":
    print("Enjoy your stay in Tokyo!")
elif destination == "new york":
    print("Enjoy your stay in New York!")
else:
    print("Oops, that destination is not currently available.")

print("\nThank you for using our travel app!")