# main.py
from storage import load_users, add_user, get_user, update_user
from user import User



def main():

    print("=== Welcom to my Bank ===")
    while True:
        users = load_users()
        print("\n1) Login")
        print("2) Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            u = login(users)
            if u is None:
                continue
            if u.username == "kerolos":
                admin_menu(u, users)
            else:
                user_menu(u, users)
            
        elif choice == "2":
            print("Bank_closed!")
            break
        else:
            print("Invalid option.")


"""I used this to check if the login is correct or not
    and to see the user is normal user or admin 
"""
def login(users):
    username = input("Username: ").strip()
    
    user1 = get_user(users, username)
    if user1 is None:
        print("No such user.")
        return None
    passe = input("Password: ").strip()
    if user1.check_password(passe):
        return user1
    print("Wrong password.")
    return None

def admin_menu(admin_user: User, users: dict):
    while True:
        print("\n--- ADMIN MENU ---")
        print("1) Add new user")
        print("2) View any user's balance")
        print("3) Give permission ")
        print("4) Remove permission")
        print("5) Show all users")
        print("6) Edit balance")
        print("7) Exit admin menu")

        choice = input("Select: ").strip()
        if choice == "1":
            """add new user"""
            uname = input("New username: ").strip()
            if uname == "":
                print("Invalid username.")
                continue
            if uname in users:
                print("Username already exists.")
                continue
            upass = input("Password for new user: ").strip()

            bal_input = input("Initial balance (number, default 0): ").strip()
            if bal_input and bal_input.replace('.', '', 1).isdigit():
                bal = float(bal_input)
            else:
                bal = 0.0

            added = add_user(users, uname, upass, bal)
            if added:
                print(f"User '{uname}' added.")
            else:
                print("Failed to add user (already exists).")
        elif choice == "2":
            target = input("Enter username to view balance: ").strip()
            t = get_user(users, target)
            if t is None:
                print("No such user.")
            else:
                print(f"{target} balance: {t.balance:.2f}")

                
        elif choice == "3":
            owner = input("Owner username : ").strip()
            if owner not in users:
                print("Owner not found.")
                continue
            grantee = input("Grant viewing permission to (username): ").strip()
            if grantee not in users:
                print("Grantee not found.")
                continue
            users[owner].grant_permission(grantee)
            update_user(users, owner)
            print(f"{grantee} can now view {owner}'s balance.")
        elif choice == "4":
            owner = input("Owner username (whose permission to remove): ").strip()
            if owner not in users:
                print("Owner not found.")
                continue
            grantee = input("Remove permission from (username): ").strip()
            users[owner].remove_permission(grantee)
            update_user(users, owner)
            print(f"Permission removed (if existed).")

        elif choice == "5":
            print("All users:")
            for uname, user in users.items():
                print(f"- {uname}: balance={user.balance:.2f}, permissions={user.permissions}")

        elif choice == "6":
            target = input("Enter username to edit balance: ").strip()
            t = get_user(users, target)
            if t is None:
                print("No such user.")
                continue
            new_bal_input = input(f"Enter new balance for {target}: ").strip()
            if new_bal_input and new_bal_input.replace('.', '', 1).isdigit():
                new_bal = float(new_bal_input)
                t.balance = new_bal
                update_user(users, target)
                print("Balance updated.")
            else:
                print("Invalid balance input.")

        elif choice == "7":
            print("Logging out admin.")
            break        
        else:
            print("Invalid choice.")

def user_menu(user: User, users: dict):
    while True:
        print(f"\n--- WLCOME {user.username} ---")
        print("1) View your balance")
        print("2) View another user's balance")
        print("3) Give permission to another user to view your balance")
        print("4) Remove permission")
        print("5) Edit balance")
        print("6) Logout")
        choice = input("Select: ").strip()
        if choice == "1":
            print(f"Your balance: {user.balance:.2f}")
        elif choice == "2":
            target = input("Enter username to view: ").strip()
            if target not in users:
                print("No such user.")
                continue
            if user.username == target or user.username in users[target].permissions:
                print(f"{target} balance: {users[target].balance:.2f}")
            else:
                print("Access denied. The other user hasn't granted you permission.")
        elif choice == "3":
            grantee = input("Enter username to grant permission to: ").strip()
            if grantee not in users:
                print("No such user.")
                continue
            user.grant_permission(grantee)
            update_user(users, user.username)
            print(f"{grantee} can now view your balance.")
        elif choice == "4":
            grantee = input("Enter username to remove permission from: ").strip()
            user.remove_permission(grantee)
            update_user(users, user.username)
            print("Permission removed (if it existed).")
        elif choice == "5":
            new_bal_input = input("Enter new balance: ").strip()
            if new_bal_input and new_bal_input.replace('.', '', 1).isdigit():
                new_bal = float(new_bal_input)
                user.balance = new_bal
                update_user(users, user.username)
                print("Balance updated.")
            else:
                print("Invalid balance input.")
        elif choice == "6":
            print("Logging out.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
