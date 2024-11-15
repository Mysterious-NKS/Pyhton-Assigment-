from database import load_users
production_log = []
equipment_log = []
import os
#ee

def clear_screen():
    os.system("cls")

def chef_login():
    print("\n==== Chef Login ====")
    while True:
        username = input("Please enter a username (type 'undo' to go back) ► ")
        if username.lower() == 'undo':
            return
        password = input("Please enter a password: ")
        users = load_users()
        user_dict = {user[0]: user for user in users}
        user = user_dict.get(username)
        if user:
            if user[1] == password and user[2] == 'chef':
                print("Login successful!")
                chef_settings()
                break
        else:
            print("Username or password is incorrect, or you are not a chef. Please try again.")
            
def save_menu_to_file(food_list, drink_list):
    with open('menu.txt', 'w') as file:
        # Set column widths based on maximum lengths for each column
        name_width = max(max(len(item['name']) for item in food_list),
                        max(len(item['name']) for item in drink_list),
                        len("Name"))
        price_width = len("Price (RM)")
        recipe_width = max(max(len(item['recipe']) for item in food_list),
                        max(len(item['recipe']) for item in drink_list),
                        len("Recipe"))

        # Define the horizontal separator for the table
        separator = "+-{}-+-{}-+-{}-+\n".format('-' * name_width, '-' * price_width, '-' * recipe_width)

        # Write food menu header
        file.write("Food:\n")
        file.write(separator)
        file.write("| {:<{}} | {:<{}} | {:<{}} |\n".format("Name", name_width, "Price (RM)", price_width, "Recipe", recipe_width))
        file.write(separator)

        # Write food items
        for item in food_list:
            file.write("| {:<{}} | {:<{}} | {:<{}} |\n".format(
                item['name'], name_width,
                item['price'], price_width,
                item['recipe'], recipe_width
            ))

        file.write(separator + "\n")

        # Write drink menu header
        file.write("Drink:\n")
        file.write(separator)
        file.write("| {:<{}} | {:<{}} | {:<{}} |\n".format("Name", name_width, "Price (RM)", price_width, "Recipe", recipe_width))
        file.write(separator)

        # Write drink items
        for item in drink_list:
            file.write("| {:<{}} | {:<{}} | {:<{}} |\n".format(
                item['name'], name_width,
                item['price'], price_width,
                item['recipe'], recipe_width
            ))

        file.write(separator)

    print("Menu has been saved to 'menu.txt' with the requested table format.")

# 1.2.1 厨师菜单
food_list = [
    {"name": "Burger", "price": 15, "recipe": "Patty, burger bun, lettuce, ketchup"},
    {"name": "Pizza", "price": 20, "recipe": "Flour, mozzarella cheese, pepperoni, onions"},
    {"name": "Salad", "price": 10, "recipe": "Sliced tomatoes, sliced avocado, sliced cucumber, mustard"},
    {"name": "Sushi", "price": 25, "recipe": "Rice, salmon fish, seaweeds"},
    {"name": "Tacos", "price": 12, "recipe": "Onions, chopped chicken, chili powder, lettuce, diced tomatoes, shredded cheese"},
    {"name": "Pasta", "price": 18, "recipe": "Fettuccine , grilled chicken, tomato sauce, meatballs, garnish"}
]

drink_list = [
    {"name": "Tea", "price": 4, "recipe": "Tea bag with water"},
    {"name": "Water", "price": 1.50, "recipe": "Plain water"}
]

food_inv = {
    "Bread": {"quantity": 100, "unit": "10Kg"},
    "Pepperoni": {"quantity": 50, "unit": "20Kg"},
    "Ham": {"quantity": 30, "unit": "30Kg"},
    "Lettuce": {"quantity": 75, "unit": "40Kg"},
    "Bottle tomato sauce": {"quantity": 20, "unit": "10L"},
    "Fish": {"quantity": 50, "unit": "50Kg"},
    "Rice": {"quantity": 100, "unit": "60Kg"},
    "Tomato": {"quantity": 12, "unit": "70Kg"},
    "Chicken": {"quantity": 50, "unit": "80Kg"},
    "Flour": {"quantity": 500, "unit": "90Kg"}
}


# 1.2.2 添加菜品
def add_recipe():
    print("Please insert your recipe")
    print("Press Enter without typing anything to finish.")

    while True:
        food = input("Name (press Enter to finish): ").strip()

        if not food:
            break

        ask_menu = input("Type ('food' or 'drink'): ").strip().lower()
        if ask_menu not in ["food", "drink"]:
            print("Invalid type. Must be 'food' or 'drink'.")
            continue

        price = input("Price (press Enter to skip): ").strip()
        recipe = input("Recipe (press Enter to skip): ").strip()

        if not price:
            price = 0
        else:
            try:
                price = float(price)
            except ValueError:
                print("Invalid price entered. Defaulting to 0.")
                price = 0

        if not recipe:
            recipe = "No recipe provided"

        new_recipe = {
            "name": food,
            "price": price,
            "recipe": recipe
        }

        if ask_menu == "food":
            food_list.append(new_recipe)
        else:
            drink_list.append(new_recipe)

        print("\nAdded successfully!")
        print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")
        print(f"| {'Name':<20} | {'Price (RM)':<10} | {'Recipe':<50} |")
        print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")
        print(f"| {new_recipe['name']:<20} | {new_recipe['price']:<10.2f} | {new_recipe['recipe']:<50} |")
        print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")
        print("")

        save_menu_to_file(food_list, drink_list)  # Save the updated menu
        print(f"Menu saved to file after adding '{food}'.")
        print("")

# 1.2.3 删除菜品
def remove_recipe():
    print("==== Delete Food and Drinks ====")
    name_q = input("Enter the food or drink name to remove: ").strip()
    exit_choice = input("Do you want to proceed with deletion? (yes to proceed / no to cancel): ")

    if exit_choice.lower() == 'no':
        print("Exiting the process...")
        return

    for item_list, label in [(food_list, "food"), (drink_list, "drink")]:
        for item in item_list:
            if item['name'] == name_q:
                item_list.remove(item)
                print(f"'{name_q}' along with its price and recipe has been deleted from {label} list!")
                save_menu_to_file(food_list, drink_list)  # Save the updated menu
                print(f"Menu saved to file after removing '{name_q}'.")
                return

    print("Recipe not found.")
    print("")


# 1.2.4 更新菜品
import textwrap

def update_menu():
    update_txt = input("Enter the name of the food or drink to update: ")

    for item_list, label in [(food_list, "food"), (drink_list, "drink")]:
        for item in item_list:
            if item['name'] == update_txt:
                print("\nCurrent menu item details:")
                print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")
                print(f"| {'Name':<20} | {'Price (RM)':<10} | {'Recipe':<50} |")
                print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")

                # Display current details
                print(f"| {item['name']:<20} | {item['price']:<10.2f} | {item['recipe']:<50} |")
                print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")

                new_name = input("\nEnter new name (press Enter to skip): ")
                new_price = input("Enter new price (press Enter to skip): ")
                new_recipe = input("Enter new recipe (press Enter to skip): ")

                if new_name:
                    item['name'] = new_name
                if new_price:
                    try:
                        item['price'] = float(new_price)
                    except ValueError:
                        print("Invalid price. Keeping the old price.")
                if new_recipe:
                    item['recipe'] = new_recipe

                print(f"\n{label.capitalize()} '{update_txt}' updated successfully!")
                save_menu_to_file(food_list, drink_list)  # Save the updated menu
                print(f"Menu saved to file after updating '{update_txt}'.")
                return

    print(f"'{update_txt}' not found in the food or drink lists.\n")
    print("")


# 1.2.5 查看菜品
import textwrap

def view_menu():
    print("==== Menu ====")

    print("\nFood:")
    print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")
    print(f"| {'Name':<20} | {'Price (RM)':<10} | {'Recipe':<50} |")
    print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")

    if not food_list:
        print(f"| {'No food items available':<86} |")
    else:
        for item in food_list:
            wrapped_name = textwrap.wrap(item['name'], width=20)
            wrapped_price = textwrap.wrap(f"{item['price']:.2f}", width=10)  # Price formatted to 2 decimal places
            wrapped_recipe = textwrap.wrap(item['recipe'], width=50)

            print(f"| {wrapped_name[0]:<20} | {wrapped_price[0]:<10} | {wrapped_recipe[0]:<50} |")

            for line in wrapped_name[1:]:
                print(f"| {line:<20} | {'':<10} | {'':<50} |")

            for line in wrapped_price[1:]:
                print(f"| {'':<20} | {line:<10} | {'':<50} |")

            for line in wrapped_recipe[1:]:
                print(f"| {'':<20} | {'':<10} | {line:<50} |")

    print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")

    print("\nDrink:")
    print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")
    print(f"| {'Name':<20} | {'Price (RM)':<10} | {'Recipe':<50} |")
    print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")

    if not drink_list:
        print(f"| {'No drink items available':<86} |")
    else:
        for item in drink_list:
            wrapped_name = textwrap.wrap(item['name'], width=20)
            wrapped_price = textwrap.wrap(f"{item['price']:.2f}", width=10)
            wrapped_recipe = textwrap.wrap(item['recipe'], width=50)

            print(f"| {wrapped_name[0]:<20} | {wrapped_price[0]:<10} | {wrapped_recipe[0]:<50} |")

            for line in wrapped_name[1:]:
                print(f"| {line:<20} | {'':<10} | {'':<50} |")

            for line in wrapped_price[1:]:
                print(f"| {'':<20} | {line:<10} | {'':<50} |")

            for line in wrapped_recipe[1:]:
                print(f"| {'':<20} | {'':<10} | {line:<50} |")

    print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")
    print("")


# 1.2.6 查看库存
def checking_inv():
    with open("inventory.txt", "w") as file:
        # Prompt user for choice
        print("==== Inventory Check ====")
        choice = input(
            "Do you want to check a specific ingredient or display the whole list? (enter 'specific' or 'all'): ").strip()

        if choice == 'specific':
            check_ing = input("Enter the ingredient: ").strip()
            if check_ing in food_inv:
                quantity = food_inv[check_ing]["quantity"]
                unit = food_inv[check_ing]["unit"]

                # Define header and specific ingredient info
                header = (
                    "==== Inventory Check ====\n"
                    f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+\n"
                    f"| {'Ingredient':<20} | {'Quantity':<10} | {'Unit':<50} |\n"
                    f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+\n"
                )

                # Write to both file and console
                print(header, end="")
                file.write(header)

                # Wrap unit text if it's too long
                if len(unit) > 50:
                    wrapped_unit = textwrap.fill(unit, width=50)
                    wrapped_lines = wrapped_unit.split('\n')
                    row = f"| {check_ing.capitalize():<20} | {quantity:<10} | {wrapped_lines[0]:<50} |\n"
                    print(row, end="")
                    file.write(row)
                    for line in wrapped_lines[1:]:
                        wrapped_row = f"| {' ':<20} | {' ':<10} | {line:<50} |\n"
                        print(wrapped_row, end="")
                        file.write(wrapped_row)
                else:
                    row = f"| {check_ing.capitalize():<20} | {quantity:<10} | {unit:<50} |\n"
                    print(row, end="")
                    file.write(row)

                footer = f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+\n"
                print(footer, end="")
                file.write(footer)
                print(f"'{check_ing.capitalize()}' has been saved to 'inventory.txt'.")
            else:
                message = f"'{check_ing.capitalize()}' not available in the inventory.\n"
                print(message)
                file.write(message)

        elif choice == 'all':
            # Define header for full inventory list
            header = (
                "==== Inventory List ====\n"
                f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+\n"
                f"| {'Ingredient':<20} | {'Quantity':<10} | {'Unit':<50} |\n"
                f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+\n"
            )

            # Write header to both file and console
            print(header, end="")
            file.write(header)

            # Write each item in the inventory to both file and console
            for ingredient, details in food_inv.items():
                unit = details['unit']
                if len(unit) > 50:
                    wrapped_unit = textwrap.fill(unit, width=50)
                    wrapped_lines = wrapped_unit.split('\n')
                    row = f"| {ingredient.capitalize():<20} | {details['quantity']:<10} | {wrapped_lines[0]:<50} |\n"
                    print(row, end="")
                    file.write(row)
                    for line in wrapped_lines[1:]:
                        wrapped_row = f"| {' ':<20} | {' ':<10} | {line:<50} |\n"
                        print(wrapped_row, end="")
                        file.write(wrapped_row)
                else:
                    row = f"| {ingredient.capitalize():<20} | {details['quantity']:<10} | {unit:<50} |\n"
                    print(row, end="")
                    file.write(row)

            footer = f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+\n"
            print(footer, end="")
            file.write(footer)
            print("Full inventory has been saved to 'inventory.txt'.")
            print("")

        else:
            print("Invalid choice. Please enter 'specific' or 'all'.")
            print("")


# 1.2.7 记录生产
def rec_production():
    """Record a production log."""
    food_name = input("Enter the name of the food or drink produced: ")
    batch_number = input("Enter batch number food or drink (required 10 characters): ")

    if len(batch_number) != 10:
        print("Batch number must be exactly 10 characters. Please try again.")
        return

    quantity = input("Enter production quantity: ")
    expiration_date = input("Enter expiration date (YYYY-MM-DD): ")

    # Append to production log
    production_log.append({
        "food_name": food_name,
        "batch_number": batch_number,
        "quantity": quantity,
        "expiration_date": expiration_date
    })

    print(f"Production record for '{food_name}' added successfully!\n")
    print("")

# 1.2.8 查看生产
def view_production():
    """View and save the production log."""
    print("==== Production Log ====")
    # Open the production.txt file in write mode
    with open("production.txt", "w") as file:
        # Header for the file
        file.write("==== Production Log ====\n")

        if not production_log:
            no_records_message = "No production records available."
            print(no_records_message)
            file.write(no_records_message + "\n")
        else:
            for record in production_log:
                # Create formatted output for each record
                record_text = (
                    f"Dish: {record['food_name']}\n"
                    f"Batch Number: {record['batch_number']}\n"
                    f"Quantity: {record['quantity']}\n"
                    f"Expiration Date: {record['expiration_date']}\n"
                    f"{'-' * 30}\n"
                )

                # Display record in console
                print(record_text, end="")

                # Save record to the file
                file.write(record_text)

    print("Production log has been saved to 'production.txt'.")
    print("")


# 1.2.9 报告设备问题
def report_equip_i():
    """Report an issue with equipment."""
    equipment_name = input("Enter equipment name: ")
    issue_description = input("Describe the malfunction or maintenance need: ")

    # Append to the equipment log
    equipment_log.append({
        "equipment_name": equipment_name,
        "issue_description": issue_description
    })

    # Save the new issue to the report.txt file
    with open("report.txt", "a") as file:
        file.write("==== New Equipment Issue ====\n")
        file.write(f"Equipment: {equipment_name}\n")
        file.write(f"Issue: {issue_description}\n")
        file.write(f"{'-' * 30}\n")

    print(f"Issue reported for '{equipment_name}' successfully!\n")
    print("")

# 1.2.10 查看设备问题
def view_equip_i():
    print("==== Equipment Issues Log ====")

    # Open the report.txt file in write mode to overwrite with the complete log
    with open("report.txt", "w") as file:
        # Header for the file
        file.write("==== Equipment Issues Log ====\n")

        if not equipment_log:
            no_issues_message = "No equipment issues reported."
            print(no_issues_message)
            file.write(no_issues_message + "\n")
        else:
            for issue in equipment_log:
                # Create formatted output for each issue
                issue_text = (
                    f"Equipment: {issue['equipment_name']}\n"
                    f"Issue: {issue['issue_description']}\n"
                    f"{'-' * 30}\n"
                )

                # Display issue in console
                print(issue_text, end="")

                # Save issue to the file
                file.write(issue_text)

    print("Equipment issues log has been saved to 'report.txt'.")
    print("")


# 1.2.11 厨师设置
def chef_settings():
    clear_screen()
    while True:
        print("\n╔═══════════════════════════════╗")
        print("║         Chef Settings         ║")
        print("╚═══════════════════════════════╝")
        print("1. Add Food/Drink              ")
        print("2. Update Food/Drink           ")
        print("3. Delete Food/Drink           ")
        print("4. View Menu                   ")
        print("5. Check Inventory             ")
        print("6. Record Production           ")
        print("7. View production             ")
        print("8. Report Equipment Issue      ")
        print("9. View Equipment Issues       ")
        print("0. Exit                        ")
        print("")

        choice = input("Choose an option: ")
        if choice == "1":
            add_recipe()
        elif choice == "2":
            update_menu()
        elif choice == "3":
            remove_recipe()
        elif choice == "4":
            view_menu()
        elif choice == "5":
            checking_inv()
        elif choice == "6":
            rec_production()
        elif choice == "7":
            view_production()
        elif choice == '8':
            report_equip_i()
        elif choice == '9':
            view_equip_i()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

