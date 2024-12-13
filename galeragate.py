import sqlite3

# Database setup
conn = sqlite3.connect('galeragate.db') # Connect to SQLite database (or create it if it doesn't exist)
cursor = conn.cursor() # Create a cursor object to execute SQL commands

# Create the 'tourists' table to store tourist information
cursor.execute(''' 
CREATE TABLE IF NOT EXISTS tourists (
    tourist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR (300) NOT NULL,
    age INTEGER,
    sex VARCHAR (10),
    nationality VARCHAR (100),
    contact_number INTEGER,
    entry_date DATE,
    exit_date DATE
)
''')

# Create the 'selections' table to store tourist selections (e.g., attractions, services)
cursor.execute('''
CREATE TABLE IF NOT EXISTS selections (
    tourist_id INTEGER,
    category VARCHAR (100),
    choice VARCHAR (100),
    PRIMARY KEY (tourist_id, category, choice),  
    FOREIGN KEY (tourist_id) REFERENCES tourists(tourist_id)
)
''')

# Create the 'payment_methods' table to store payment details
cursor.execute('''
CREATE TABLE IF NOT EXISTS payment_methods (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tourist_id INTEGER,
    payment_method VARCHAR (100),
    amount_paid INT,
    payment_date DATE,
    FOREIGN KEY (tourist_id) REFERENCES tourists(tourist_id)
)
''')

conn.commit() # Save the changes to the database

# Functions
def welcome_screen():
    import time  # Import the time module to determine the current time for the greeting
    current_hour = time.localtime().tm_hour # Get the current hour of the day
    if 5 <= current_hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
        

    # Display the welcome menu
    print("\n" + "=" * 80)
    print("\033[1;35m" + f" " * 20 + f"✨ {greeting}! Welcome to GaleraGate ✨" + "\033[0m")
    print("\033[1;36m" + " " * 20 + "Your Gateway to Puerto Galera's Paradise!" + "\033[0m")
    print("=" * 80)
    
    print("\033[1;37m"+ " " * 20 + "Please choose an option to proceed:\033[0m")
    print("\033[1;33m[1] 🏖 Tourist - Explore attractions, make reservations, and more.\033[0m")
    print("\033[1;35m[2] 🛠 Admin - Manage tourist data and view reports.\033[0m")
    print("\033[1;36m[3] 💬 FAQ's - Learn how to use the system and find answers.\033[0m")
    print("\033[1;31m[4] ❌ Exit - Close the application.\033[0m")
    
    print("-" * 80)
    valid_choices = {'1', '2', '3', '4'} # Validate user input
    choice = input("\033[1;37mEnter your choice: \033[0m").strip().upper()
    
    while choice not in valid_choices: # Check if the input is valid; if not, prompt the user to try again
        print("\033[1;31mInvalid choice. Please try again.\033[0m")
        choice = input("\033[1;37mEnter your choice: \033[0m").strip().upper()
    
    print("=" * 80)
    return choice

def tourist_menu():
    print("\033[1;32m" + " " * 25 + "🌴 Welcome, dear Tourist! 🌴" + "\033[0m")
    print("\033[1;36m" + " " * 10 + "Get ready to immerse yourself in the beauty of Puerto Galera. \033[0m")
    print("=" * 80)
    
    print("\033[1;33m" + "Please provide your personal information below to proceed." + "\033[0m")
    print("-" * 80)
    
    name = input("👤 Name: ").strip()
   # Age input validation
    while True:
        try:
            age = int(input("🎂 Age: ").strip())
            if age <= 0:
                print("\033[1;31mAge must be a positive number. Please enter a valid age.\033[0m")
                continue
            break
        except ValueError as e: # Handle case where input is not a valid number
            print(f"\033[1;31mInvalid input for age. Please enter a valid number. \n{e}\033[0m")
    sex = input("⚤ Sex (Male/Female): ").strip()
    nationality = input("🌍 Nationality: ").strip()
    contact = input("📞 Contact Number: ").strip()
    entry_date = input("📅 Entry Date (YYYY-MM-DD): ").strip()
    exit_date = input("📅 Exit Date (YYYY-MM-DD): ").strip()
    try:  # Insert the tourist data into the database
        cursor.execute(''' 
        INSERT INTO tourists (name, age, sex, nationality, contact_number, entry_date, exit_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, age, sex, nationality, contact, entry_date, exit_date))
        conn.commit()
    except sqlite3.Error as e:   # Handle any SQLite errors
        print(f"Error occurred: {e}")
    
    tourist_id = cursor.lastrowid # Get the last inserted tourist's ID
    print("\n\033[1;32m" + f"🎉 Your Tourist ID is: {str(tourist_id).zfill(4)} 🎉" + "\033[0m")
    print("=" * 80)
    
    return tourist_id

def edit_personal_info(tourist_id):
    print("\n" + "=" * 80)
    print("\033[1;34m" + "Edit Your Personal Information".center(80) + "\033[0m")
    print("=" * 80)
    
    # Retrieve the tourist's current information from the database
    cursor.execute("SELECT * FROM tourists WHERE tourist_id = ?", (tourist_id,))
    tourist = cursor.fetchone()
    
    if tourist:
        print("\033[1;32m" + "Current Information".center(80) + "\033[0m")
        print("-" * 80)
        print(f"\033[1mTourist ID   : {tourist_id:04}\033[0m")
        print(f"Name         : {tourist[1]}")
        print(f"Age          : {tourist[2]}")
        print(f"Sex          : {tourist[3]}")
        print(f"Nationality  : {tourist[4]}")
        print(f"Contact No.  : {tourist[5]}")
        print(f"Entry Date   : {tourist[6]}")
        print(f"Exit Date    : {tourist[7]}")
        print("-" * 80)
        
        # Prompt the user to enter new details or press Enter to keep the current values
        print("\n\033[1;33m" + "Enter new details or press Enter to keep the current value:".center(80) + "\033[0m")
        
        name = input(f"Name [{tourist[1]}]: ") or tourist[1]
        age = input(f"Age [{tourist[2]}]: ")
        age = int(age) if age.isdigit() else tourist[2]
        sex = input(f"Sex [{tourist[3]}]: ") or tourist[3]
        nationality = input(f"Nationality [{tourist[4]}]: ") or tourist[4]
        contact = input(f"Contact Number [{tourist[5]}]: ") or tourist[5]
        entry_date = input(f"Entry Date [{tourist[6]}]: ") or tourist[6]
        exit_date = input(f"Exit Date [{tourist[7]}]: ") or tourist[7]
        
        print("\n\033[1;36mProcessing...\033[0m")
        print("=" * 80)
        
        # Update the tourist's information in the database
        cursor.execute('''
            UPDATE tourists 
            SET name = ?, age = ?, sex = ?, nationality = ?, contact_number = ?, entry_date = ?, exit_date = ?
            WHERE tourist_id = ?
        ''', (name, age, sex, nationality, contact, entry_date, exit_date, tourist_id))
        conn.commit()
        
        print("\033[1;32mInformation updated successfully!\033[0m")
    else:
        print("\033[1;31mTourist not found. Please try again.\033[0m")
    print("=" * 80)

def category_selection(tourist_id):
    # Dictionary holding categories and their respective options
    categories = {
        "Resort": ["Mermaid Resort", "Blue Crystal Beach Resort", "Edgewater Dive & Spa", "Arkipelago Beach Resort", "Steps and Garden Resort"],
        "Restaurant": ["Atlantis Restaurant", "Aplayang Munti Resto", "Badladz", "Fisherman's Cove", "Jalyn's Resto"],
        "Activities": ["Snorkeling", "Scuba Diving", "Island Hopping", "Sunset Cruise", "Water Sports"],
        "Places": ["White Beach", "Sabang Beach", "Tamaraw Falls", "Mangrove Forest", "Coral Garden"]
    }

    while True:
        print("=" * 80)
        print("\033[1;36m" + " " * 20 + "🗺️ Categories: Choose your options below!" + "\033[0m")
        print("=" * 80)
        # Show the available categories (Resort, Restaurant, Activities, Places)
        for i, category in enumerate(categories.keys(), start=1):
            print(f"\033[1;33m[{i}] {category} 🏖️\033[0m")
        
        print("\033[1;35m[5] Overall Selection 📋\033[0m")
        print("\033[1;31m[6] Delete Selection ❌\033[0m")
        print("\033[1;32m[7] Back to Main Menu ↩️\033[0m")

        choice = input("Enter your choice: ").strip()
        
        if choice in "1234": # User selects a category, show available options within that category
            category = list(categories.keys())[int(choice) - 1]
            print(f"\n\033[1;34m{category} Options 🏖️\033[0m")
            print("-" * 80)
            
            for i, option in enumerate(categories[category], start=1):
                print(f"\033[1;32m[{i}] {option}\033[0m")
            
            selection = int(input("Enter your choice: ")) - 1
            selected_item = categories[category][selection]
            
            cursor.execute("INSERT INTO selections (tourist_id, category, choice) VALUES (?, ?, ?)",
                           (tourist_id, category, selected_item))
            conn.commit()
            print(f"\n\033[1;32mAdded: {selected_item} under {category} ✅\033[0m")
        
        elif choice == "5": # View the overall selections made by the tourist
            cursor.execute("SELECT category, choice FROM selections WHERE tourist_id = ?", (tourist_id,))
            selections = cursor.fetchall()
            if selections:
                print("\n\033[1;36mOverall Selections 📋\033[0m")
                print("=" * 80)
                for category, choice in selections:
                    index = categories[category].index(choice) + 1
                    print(f"[{index}] {category}: {choice}")
                print("\033[1;33m[1] Proceed to Reservation 📅\033[0m")
                print("\033[1;31m[2] Exit ❌\033[0m")
                option = input("Enter your choice: ").strip()
                print("=" * 80)
                if option == "1":
                    print("\033[1;33mProceeding to payment...\033[0m")
                    print("\033[1;31mUpon arriving at Puerto Galera's Balatero Pier\nmake sure to pay the Environmental User Fee of 120 pesos per tourist.\nFrom there, trikes are readily available to transport you to your resort.\033[0m")
                    print("=" * 80)
                    
                    # Payment Method Input
                    print("\033[1;34mPayment Options 🛒\033[0m")
                    print("\033[1;35m1. Credit Card\033[0m")
                    print("\033[1;35m2. Cash\033[0m")
                    print("\033[1;35m3. PayPal\033[0m")
                    payment_choice = input("Choose a payment method: ").strip()
                    payment_methods = { "1": "Credit Card", "2": "Cash", "3": "PayPal" }
                    
                    if payment_choice in payment_methods: # Record the payment details in the database
                        payment_method = payment_methods[payment_choice]
                        amount_paid = float(input("Enter the total amount paid: "))
                        payment_date = input("Enter the payment date (YYYY-MM-DD): ").strip()
                        
                        cursor.execute(
                            "INSERT INTO payment_methods (tourist_id, payment_method, amount_paid, payment_date) VALUES (?, ?, ?, ?)",
                            (tourist_id, payment_method, amount_paid, payment_date)
                        )
                        conn.commit()
                        print("\n\033[1;32mPayment completed successfully! ✅\033[0m")
                        proceed_to_reservation(tourist_id)
                    else:
                        print("\n\033[1;31mInvalid payment method selected.❌\033[0m")
                elif option == "2":
                    break
            else:
                print("\n\033[1;31mNo selections made yet. Please make a selection first!❌\033[0m")
        
        elif choice == "6": # Delete a selection made by the tourist
            cursor.execute("SELECT rowid, category, choice FROM selections WHERE tourist_id = ?", (tourist_id,))
            selections = cursor.fetchall()
            if selections:
                print("\n\033[1;31mYour Selections to Delete❌\033[0m")
                print("=" * 80)
        
                for rowid, category, choice in selections:
                    category_index = list(categories.keys()).index(category) + 1
                    choice_index = categories[category].index(choice) + 1
                    print(f"[{category_index}] {category}: {choice}")
        
                choice_index = int(input(f"Enter the option number to delete under {category}: ").strip()) - 1
                selected_choice = categories[category][choice_index]
                
                confirmation = input(f"\n\033[1;33mAre you sure you want to delete this selection: {selected_choice}? \nType 'yes' to confirm: \033[0m").strip().lower()
                
                if confirmation == 'yes':
                    cursor.execute("DELETE FROM selections WHERE tourist_id = ? AND category = ? AND choice = ?",
                                (tourist_id, category, selected_choice))
                    conn.commit()
                    print("\n\033[1;32mSelection deleted successfully. ✅\033[0m")
                else:
                    print("\n\033[1;31mDeletion cancelled. No changes were made.❌\033[0m")
            else:
                print("\n\033[1;31mNo selections to delete.❌\033[0m")
                
        elif choice == "7":
            break

def proceed_to_reservation(tourist_id):
    print("\n\033[1;36m" + " " * 30 + "Generating Receipt..." "\033[0m\n")
    # Fetch Tourist Details
    cursor.execute("SELECT * FROM tourists WHERE tourist_id = ?", (tourist_id,))
    tourist = cursor.fetchone()
    
    print("=" * 80)
    print("\033[1;35m" + " " * 30 + "===== Tourist Receipt =====" + "\033[0m")
    print("=" * 80)
    
    # Tourist Info with formatting
    print(f"\033[1;33mTourist ID: \033[0m{str(tourist_id).zfill(4)}")
    print(f"\033[1;33mName: \033[0m{tourist[1]}")
    print(f"\033[1;33mAge: \033[0m{tourist[2]}")
    print(f"\033[1;33mSex: \033[0m{tourist[3]}")
    print(f"\033[1;33mNationality: \033[0m{tourist[4]}")
    print(f"\033[1;33mContact: \033[0m{tourist[5]}")
    print(f"\033[1;33mEntry Date: \033[0m{tourist[6]}")
    print(f"\033[1;33mExit Date: \033[0m{tourist[7]}")
    
    # Display Selections
    print("\n\033[1;36mSelections:\033[0m")
    print("=" * 80)
    cursor.execute("SELECT category, choice FROM selections WHERE tourist_id = ?", (tourist_id,))
    selections = cursor.fetchall()
    
    if selections:
        for category, choice in selections:
            print(f"\033[1;34m{category}: \033[0m{choice}")
    else:
        print("\033[1;31mNo selections made yet.\033[0m")
    
    # Fetch and Display Payment Information
    print("\n\033[1;36mPayment Details:\033[0m")
    print("=" * 80)
    cursor.execute("SELECT payment_method, amount_paid, payment_date FROM payment_methods WHERE tourist_id = ?", (tourist_id,))
    payment = cursor.fetchone()
    
    if payment:
        print(f"\033[1;33mPayment Method: \033[0m{payment[0]}")
        print(f"\033[1;33mAmount Paid: \033[0m₱{payment[1]:,.2f}")
        print(f"\033[1;33mPayment Date: \033[0m{payment[2]}")
    else:
        print("\033[1;31mNo payment information found.\033[0m")
    
    # Footer Message
    print("=" * 80)
    print("\033[1;32mThank you for your reservation! We hope you have a great time at Puerto Galera! 🌞\033[0m")

def login():
    print("\033[1;36m" + " " * 33 + "🔒 Admin Login\033[0m")
    print("=" * 80)
    
     # Prompt user for email and password input
    email = input("\033[1;33m📧 Enter email: \033[0m")
    password = input("\033[1;33m🔑 Enter password: \033[0m")
    
    # Retry mechanism in case of incorrect credentials
    retry_count = 3
    while retry_count > 0: # Check credentials and grant access
        if email == "admin@galeragate.com" and password == "admin123":
            print("\n\033[1;32m✅ Login successful! Redirecting to Admin Panel... 🌟\033[0m")
            admin_menu()
            break
        else:
            retry_count -= 1
            if retry_count > 0:
                print(f"\033[1;31m❌ Invalid email or password. {retry_count} attempts left. Please try again. 🔄\033[0m")
                email = input("\033[1;33m📧 Enter email: \033[0m")
                password = input("\033[1;33m🔑 Enter password: \033[0m")
            else:
                print("\033[1;31m❌ Too many failed attempts. Please try again later. 🔒\033[0m")
                break
            
def count_tourist(): # Query to count the total number of tourists in the database
    query = "SELECT COUNT(*) AS total_tourists FROM tourists;"
    cursor.execute(query)
    result = cursor.fetchone()
    print("\033[1;32m" + " " * 20 + "🎉 Total Number of Tourists: \033[1;33m" + str(result[0]) + "\033[0m")
    print("=" * 80)
        
def reset_tables():
    print("=" * 80)
    print("\033[1;31m🧹 Resetting tables... ⚠️ This will delete all data and reset IDs.\033[0m")  # Print a message warning the user about resetting the tables and deleting all data
    confirm = input("\033[1;33mAre you sure? Type 'yes' to confirm: \033[0m").strip().lower()
    
    if confirm == 'yes':
        print("\n\033[1;36m🔄 Resetting tables...\033[0m")
        
         # Execute SQL queries to delete all records from relevant tables
        cursor.execute("DELETE FROM tourists")
        cursor.execute("DELETE FROM selections")
        cursor.execute("DELETE FROM payment_methods")  # Clear payment_methods table
        conn.commit()

        # Reset AUTOINCREMENT for all tables
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='tourists'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='selections'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='payment_methods'")  # Reset payment_methods
        conn.commit()

        print("\n\033[1;32m✅ Tables cleared and IDs reset successfully! 🎉\033[0m")
    else:
        print("\n\033[1;31m❌ Reset canceled. No changes made.\033[0m")
    print("=" * 80)

def admin_menu():
    print("\n" + "=" * 80)
    print("\033[1;35m"+ " " * 30 + "✨ Admin Panel ✨\033[0m")
    print("=" * 80)
    print("\033[1;33m[1] 👀 View All Tourists\033[0m")
    print("\033[1;34m[2] ✏️ Update Tourist Info\033[0m")
    print("\033[1;35m[3] 🧑 Count All Tourists\033[0m")
    print("\033[1;31m[4] 🗑️ Delete Tourist\033[0m")
    print("\033[1;32m[5] 💳 View Payment Methods\033[0m")
    print("\033[1;36m[6] 🔄 Reset Tables\033[0m")
    print("\033[1;32m[7] 🚪 Exit\033[0m")
    choice = input("\nEnter your choice: ").strip()
    print("=" * 80)
    
    if choice == "1":  # Query to fetch all tourists along with their selections from the database
        cursor.execute("""
        SELECT tourists.tourist_id, tourists.name, tourists.age, tourists.nationality,
               tourists.contact_number, tourists.entry_date, tourists.exit_date,
               selections.category, selections.choice
        FROM tourists
        LEFT JOIN selections ON tourists.tourist_id = selections.tourist_id
        """)
    
        tourists = cursor.fetchall()
        print("\n\033[1;32mAll Tourists:\033[0m")
        print("=" * 80)
    
        current_tourist_id = None
        for row in tourists: # Loop through the fetched tourist data
            tourist_id, name, age, nationality, contact_number, entry_date, exit_date, category, choice = row # Unpack the row into respective variables
        
            if tourist_id != current_tourist_id:  # Display tourist info for each new tourist ID (avoiding duplicates)
                if current_tourist_id is not None:
                    print("=" * 80)
            
                print(f"\033[1;33mTourist ID: \033[0m{str(tourist_id).zfill(4)}")
                print(f"\033[1;34mName:\033[0m \033[1;36m{name}\033[0m")
                print(f"\033[1;34mAge:\033[0m \033[1;33m{age}\033[0m")
                print(f"\033[1;34mNationality:\033[0m \033[1;32m{nationality}\033[0m")
                print(f"\033[1;34mContact Number:\033[0m \033[1;31m{contact_number}\033[0m")
                print(f"\033[1;34mEntry Date:\033[0m \033[1;36m{entry_date}\033[0m")
                print(f"\033[1;34mExit Date:\033[0m \033[1;38m{exit_date}\033[0m")
        
            if category and choice:
                print(f"\033[1;32mSelections:\033[0m")
                print(f"\033[1;34m{category}: \033[0m\033[1;33m{choice}\033[0m")
        
            current_tourist_id = tourist_id

        print("=" * 80)
        admin_menu()

    elif choice == "2":
        tourist_id = int(input("\033[1;33mEnter Tourist ID to update: \033[0m"))
        edit_personal_info(tourist_id)
        admin_menu()

    elif choice == "3":
        count_tourist()
        admin_menu()

    elif choice == "4":
        tourist_id = int(input("\033[1;31mEnter Tourist ID to delete: \033[0m"))
        cursor.execute("DELETE FROM tourists WHERE tourist_id = ?", (tourist_id,)) # Execute SQL query to delete the tourist record from the database using the entered ID 
        conn.commit()
        print("\n\033[1;31mTourist deleted successfully. 🗑️\033[0m")
        admin_menu()

    elif choice == "5":  # View Payment Methods
        # Advanced SQL query to fetch detailed payment records and aggregated summaries
        cursor.execute("""
        SELECT 
            pm.payment_id, 
            t.name, 
            pm.amount_paid, 
            pm.payment_method, 
            pm.payment_date,
            SUM(pm.amount_paid) OVER (PARTITION BY pm.payment_method) AS TotalPerMethod,
            COUNT(pm.payment_id) OVER (PARTITION BY pm.payment_method) AS TransactionCount
        FROM payment_methods pm
        JOIN tourists t ON pm.tourist_id = t.tourist_id
        ORDER BY pm.payment_date DESC;
        """)
        payments = cursor.fetchall()

        # Display payment records   
        print("\033[1;32m" + " " * 30 + "All Payment Records: " + "\033[0m")
        print("-" * 80)
        for payment in payments:
            payment_id, name, amount_paid, payment_method, payment_date, total_per_method, transaction_count = payment
            print(f"\033[1;33mPayment ID: \033[0m{payment_id}")
            print(f"\033[1;34mTourist Name: \033[0m{name}")
            print(f"\033[1;34mAmount: \033[0m₱{amount_paid}")
            print(f"\033[1;34mPayment Type: \033[0m{payment_method}")
            print(f"\033[1;34mDate: \033[0m{payment_date}")
            print(f"\033[1;35mTotal for {payment_method}: \033[0m₱{total_per_method} "
                  f"(\033[1;33m{transaction_count} Transactions\033[0m)")
            print("=" * 80)
        admin_menu()

    elif choice == "6":
        reset_tables()
        admin_menu()

    elif choice == "7":
        print("\033[1;36mGoodbye! 👋\033[0m")
        return

    else:
        print("\033[1;31mInvalid choice. Please try again. ❌\033[0m")
    print("=" * 80)
    
def faq():
    print("\033[1;36m"+ " " * 20 + "💬 Frequently Asked Questions (FAQ) 💬" + "\033[0m")
    print("=" * 80)
    print("\033[1;33m[1] How do I register as a tourist?\033[0m")
    print("\033[1;34m[2] What is the Tourist ID and how is it generated?\033[0m")
    print("\033[1;35m[3] How do I make selections for resorts, restaurants, and activities?\033[0m")
    print("\033[1;32m[4] Can I edit my personal information after registration?\033[0m")
    print("\033[1;31m[5] How do I delete my selections?\033[0m")
    print("\033[1;37m[6] How can I view my reservation and selections?\033[0m")
    print("\033[1;36m[7] What should I do if I forgot my Tourist ID?\033[0m")
    print("\033[38;5;208m[8] Back to Main Menu ↩️\033[0m")
    print("=" * 80)

    choice = input("Enter the number of your question: ").strip()

    if choice == "1":
        print("\n\033[1;36mHow do I register as a tourist?\033[0m")
        print("=" * 80)
        print("To register as a tourist, simply choose the 'Tourist' option from the main menu\nand provide your personal information (Name, Age, Sex, Nationality, etc.).\nOnce you submit, you'll receive a unique Tourist ID for your records.")
    elif choice == "2":
        print("\n\033[1;36mWhat is the Tourist ID and how is it generated?\033[0m")
        print("=" * 80)
        print("The Tourist ID is a unique identifier assigned to each tourist.\nIt is generated automatically when you register with your\ndetails, ensuring no two tourists have the same ID.")
    elif choice == "3":
        print("\n\033[1;36mHow do I make selections for resorts, restaurants, and activities?\033[0m")
        print("=" * 80)
        print("Once you're registered, you'll be able to choose from different categories\nlike Resorts, Restaurants, Activities, and Places. Simply\nselect your preferred options, and they will be saved to your profile.")
    elif choice == "4":
        print("\n\033[1;36mCan I edit my personal information after registration?\033[0m")
        print("=" * 80)
        print("Yes! You can always edit your personal information after registration.\nJust visit the 'Edit Personal Information' section and\n update any details like name, age, contact number, etc.")
    elif choice == "5":
        print("\n\033[1;36mHow do I delete my selections?\033[0m")
        print("=" * 80)
        print("To delete any selection, simply go to your overall selections and\nchoose the 'Delete Selection' option. You can remove resorts,\nrestaurants, or activities you no longer wish to select.")
    elif choice == "6":
        print("\n\033[1;36mHow can I view my reservation and selections?\033[0m")
        print("=" * 80)
        print("You can view your reservation and overall selections by selecting\n'Overall Selection' from the menu. This will show all the\nresorts, restaurants, activities, and places you have chosen.")
    elif choice == "7":
        print("\n\033[1;36mWhat should I do if I forgot my Tourist ID?\033[0m")
        print("=" * 80)
        print("If you forgot your Tourist ID, you can always contact the admin\nto retrieve your ID or check any emails or messages confirming your registration.")
    elif choice == "8":
        print("\nReturning to Main Menu...\n")
        return  # Goes back to the main menu or previous function
    else:
        print("\033[1;31mInvalid selection. Please choose a valid question number.\033[0m")

    # Prompt user if they want to check more FAQs
    more_faq = input("\n\033[1;33m" + " " * 15 + "Would you like to see more FAQs? (y/n): " + "\033[0m").strip().lower()
    if more_faq == "y":
        faq()  # Calls the FAQ function again if user wants to see more FAQs
    else:
        print("\033[1;32m" + " " * 15 + "Thank you for using the FAQ service! 😊" + "\033[0m")
        
def main():
# Main program
    while True:
        choice = welcome_screen()
        if choice == "1":
            tourist_id = tourist_menu()
            while True:
                print("=" * 80)
                print("\033[1;33m[1] 🚪 Proceed to Selection\033[0m")
                print("\033[1;34m[2] ✏️ Edit My Personal Information\033[0m")
                print("\033[1;32m[3] ↩️ Back to Main Menu\033[0m")
                sub_choice = input("Enter your choice: ").strip()
                print("=" * 80)
            
                if sub_choice == "1":
                    category_selection(tourist_id)
                elif sub_choice == "2":
                    edit_personal_info(tourist_id)
                elif sub_choice == "3":
                    break
                else:
                    print("\033[1;31mInvalid choice, please try again. ❌\033[0m")
    
        elif choice == "2":
            login()
        
        elif choice == "3":
            faq()
        
        elif choice == "4":
            print("\033[1;32m" + " " * 20 +"Thank you for using GaleraGate! Goodbye! 👋" + "\033[0m")
            print("=" * 80)
            break
        else:
            print("\033[1;31mInvalid option. Please choose a valid option. ❌\033[0m")
            
if __name__ == "__main__":
    main()
