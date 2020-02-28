# LEAP 0: *Shine*
# CPTR-405-A: Organization of Programming Languages
# filename: vending.py
# Programmed by:
#   Dakota Cookenmaster
#   Michael Yoon
# Last edit: 02/26/2020

debug = True #Make True to run tests

class VendingMachine():
    def __init__(self):
        ''' 
        Constructs a VendingMachine object and initializes the inventory to a default 5 x 5. 
        '''
        self.inventory = {}
        self.row_size = 5
        self.col_size = 5
        self.admin = False
        self.admin_password = hash("admin")
        self.commands = {
            "INVENTORY": self.view_inventory,
            "PURCHASE": self.purchase_item,
            "ADD": self.add_item,
            "HELP": self.sys_help,
            "EXIT": self.sys_exit,
            "ADMIN": self.authenticate,
            "BOOST": self.increase_quantity,
            "PRICE": self.modify_price,
            "PASSWORD": self.change_password,
            "LOGOUT": self.logout,
        }
        
        # initialize the inventory to the sizes above
        for row in range(self.row_size):
            first_letter = chr(65 + row)
            for col in range(self.col_size):
                self.inventory[first_letter + str(col)] = ["Ø (Empty)", "0", "0"]

    def __repr__(self):
        '''
        repr(VendingMachine) --> String \n
        Returns a string representation of the object's definition
        '''
        return "VendingMachine()"

    def sys_help(self, arg_list):
        ''' 
        sys_help([]) --> void \n
        Prints out the list of commands that can be used in the VendingMachine \n
        '''
        print()
        print("All users have access to the following commands:")
        print("'inventory' --> prints the vending machine's current inventory.")
        print("'purchase' SLOT_NUMBER --> initiates the purchasing process for the given SLOT_NUMBER.")
        print("'help' --> accesses this help file.")
        print()
        print("Admin-only commands:")
        print("'add' SLOT_NUMBER NAME QUANTITY PRICE --> adds a new item to the vending machine's inventory. " \
              "If you need spaces in the name of the product, replace them with underscores (i.e. '_') instead. " \
              "QUANTITY should be an integer value, and price should be a number with two decimal points (American Currency)")
        print("'exit' --> initiates the vending machine shutdown.")
        print("'boost' SLOT_NUMBER QUANTITY --> increases the current quantity of the given SLOT_NUMBER by the given QUANTITY.")
        print("'price' SLOT_NUMBER PRICE --> changes the current price of the given SLOT_NUMBER to the given PRICE.")
        print("'password' PASSWORD --> changes the current admin password to PASSWORD.")
        print("'logout' --> demotes the current admin to user status.")
        print("'admin' PASSWORD --> promotes the current user to admin status if the PASSWORD is authenticated.")
        print()

    def check_arg_count(self, number, arg_list):
        '''
        check_arg_count([number, arg_list]) --> bool
        Checks whether the current argument count is equal to number. If it is, return True. Otherwise, return False.
        '''
        if len(arg_list) > number:
            print(f"Too many arguments passed to command (expected {number}). Type 'help' to learn what arguments are expected for each command.")
            return False
        elif len(arg_list) < number:
            print(f"Too few arguments passed to command (expected {number}). Type 'help' to learn what arguments are expected for each command.")
            return False
        return True

    def logout(self, arg_list):
        '''
        logout([]) --> bool \n
        Logs the current user out if they're logged in and returns True. Otherwise, returns False.
        '''
        if self.admin:
            self.admin = False
            print("You have been logged out successfully.")
            return True
        else:
            print("You are not logged in. Type 'admin' followed by your password to get started.")
            return False
        
    def change_password(self, arg_list):
        '''
        change_password(PASSWORD) --> bool \n
        Change the admin password to what is passed. Returns True upon successful change, False otherwise. \n
        '''
        if self.admin:
            if not self.check_arg_count(1, arg_list):
                return False

            try:
                self.admin_password = hash(arg_list[0])
                print(f"Password change was successful! Password hash: {self.admin_password}")
                return True

            except Exception:
                print("Unable to change the admin password. Please try again.")
                return False
        else:
            self.auth_required()
            return False

    def modify_price(self, arg_list):
        '''
        modify_price([SLOT_NUMBER, PRICE]) --> bool \n
        allows the admin to modify the price of an exsisting item \n
        if the arguments passed are valid, will change the price and return, True. \n
        otherwise, will return, False \n
        '''
        if self.admin:
            if not self.check_arg_count(2, arg_list):
                return False

            slot_number = arg_list[0].upper()

            if slot_number not in self.inventory:
                print("Invalid SLOT_NUMBER. Please try again.")
                return False

            try:
                price = float(arg_list[1])
                self.inventory[slot_number][2] = str(price)
                return True

            except Exception:
                print("Unable to modify price. Check to make sure your command was structured correctly.")
                return False
        else:
            self.auth_required()
            return False

    def increase_quantity(self, arg_list):
        '''
        increase_quantity([SLOT_NUMBER, QUANTITY]) --> bool \n
        Allows the admin to increase the amount of an exsisting item \n
        if the item is present and the request is formated correctly, returns True \n
        otherwise, the function will prompt the user and return false
        '''
        if self.admin:
            if not self.check_arg_count(2, arg_list):
                return False
            
            slot_number = arg_list[0].upper()
            quantity = int(float(arg_list[1]))

            if self.inventory[slot_number][1] == "0":
                print("You must add an item to the inventory before you can boost it. Type 'help' to learn more.")
                return False

            try:
                self.inventory[slot_number][1] = str(int(self.inventory[slot_number][1]) + quantity)
                return True
            except Exception:
                print("Unable to boost inventory. Check to make sure your command was structured correctly.")
                return False
        else:
            self.auth_required()
            return False
        
    def authenticate(self, arg_list):
        """
        authenticate(PASSWORD) --> bool \n
        Returns True if authentication was successful, else returns False \n
        The returned bool values are used to exit out of the function early, if necessary \n
        Changes the user mode from user to admin. \n
        """
        if not self.check_arg_count(1, arg_list):
            return False

        pw = hash(arg_list[0])

        if pw == self.admin_password:
            self.admin = True
            print("Authentication was successful.")
            return True
        else:
            self.auth_failed()
            return False

    def auth_failed(self):
        '''
        auth_failed([]) --> void \n
        prompts the user that the password that was entered is invalid \n
        '''
        print("The password you entered was invalid. Please try again.")

    def auth_required(self):
        '''
        auth_required([]) --> void \n
        If the user is not logged in as an admin, rejects access. \n
        '''
        print("You do not have the authorization to execute that command. Type 'admin' followed by your password to enable this feature.")

    def sys_exit(self, arg_list):
        '''
        sys_exit([]) --> void \n
        Exits from the current program. \n
        '''
        if self.admin:
            exit(0)
        else:
            self.auth_required()

    def purchase_item(self, arg_list):
        '''purchase_item(SLOT_NUMBER) --> bool; \n
        When passed an item id, purchase_item will check if there are items in that item id to purchase \n
        If the item requested is avaliable, proceeds with the purchase and returns true \n
        otherwise, prompts the user with a message and returns false \n
        '''
        keys = self.inventory.keys()
        if not self.check_arg_count(1, arg_list):
            return False
        
        item_id = arg_list[0].upper()

        if item_id in keys:
            if int(self.inventory[item_id][1]) != 0:
                print("This item costs: $%.2f" % float(self.inventory[item_id][2]))
                self.request_currency(item_id)
                print(f"Now vending: {self.inventory[item_id][0]}.")
                self.inventory[item_id][1] = str(int(self.inventory[item_id][1]) - 1)
                if self.inventory[item_id][1] == "0":
                    self.inventory[item_id] = ["Ø (Empty)", "0", "0"]
                return True
            else:
                print("That slot is out of stock. Please try again.")
                return False

        else:
            print("Invalid Choice. Please try again.")
            return False

    def request_currency(self, item_id):
        '''
        request_currency(SLOT_NUMBER) --> void \n
        Will continually request money until the price is met. Will return change if there is any. \n
        '''
        price = float(self.inventory[item_id][2])
        money = 0

        while money < price:
            remaining = price - money
            try:
                money = money + float(input("Please insert currency ($%.2f remaining): " % remaining))
            except Exception:
                print("Please enter a valid monetary amount.")
     
        if money > price:
            money = money - price
            print("Here is your change of: $%.2f" % money)

    def add_item(self, arg_list):
        '''
        add_item([slot_number, name, quantity, price]) --> bool \n
        Attempts to add an item to the vending machine inventory. \n 
        If the item already exists, allows user to choose to replace \n
        or cancel the operation. If the item was added \n
        (or replaced), a prompt will be printed and returns true. \n
        otherwise, will prompt user and return false. \n
        '''
        if self.admin:
            if not self.check_arg_count(4, arg_list):
                return False

            try:
                slot_number = arg_list[0].upper()
                name = " ".join(list(map(str.capitalize, arg_list[1].split("_"))))
                quantity = str(int(float(arg_list[2])))
                price = "%.2f" % float(arg_list[3])
            except Exception as e:
                print("Unable to add item to inventory. Type 'help' to review command syntax.")
                print(e)
                return False

            if slot_number not in self.inventory:
                print(f"The SLOT_NUMBER '{slot_number}' is invalid. Operation cancelled.")
                return False

            if ((self.inventory[slot_number][0] == "Ø (Empty)") and (self.inventory[slot_number][1] == "0")):
                try:
                    self.inventory[slot_number] = [name, quantity, price]
                    print(f"Successfully added {name} to the inventory.")
                    return True
                except Exception:
                    print("Unable to add item to inventory. Type 'help' to review command syntax.")
                    return False
            else:
                user_input = input(f"SLOT_NUMBER {slot_number} is already in use by {self.inventory[slot_number][0]}. Would you like to replace it? ").lower()
                while ("y" not in user_input) and ("n" not in user_input):
                    user_input = input(f"SLOT_NUMBER {slot_number} is already in use by {self.inventory[slot_number][0]}. Would you like to replace it? ").lower()
                if("y" in user_input):
                    old = self.inventory[slot_number][0]
                    self.inventory[slot_number] = [name, quantity, price]
                    new = self.inventory[slot_number][0]
                    print(f"Successfully replaced {old} with {new}")
                    return True
                else:
                    print("Cancelling operation.")
                    return False
        else:
            self.auth_required()

    def view_inventory(self, arg_list):
        '''
        view_inventory([]) --> void \n
        Prints the current inventory.
        '''
        # Handle dynamic inventory sizing
        string_max = 0
        for item in self.inventory.values():
            local_max = max(x) if (x := list(map(len, item))) else 0
            if local_max > string_max:
                string_max = local_max
        string_max = max([(string_max + 2), len("SLOT_NUMBER") + 2])

        inventory_string_len = string_max * 4
        print("=" * inventory_string_len)
        print(" Vending Machine Inventory ".center(inventory_string_len, "="))
        print("=" * inventory_string_len)
        print("SLOT NUMBER".center(string_max, " "), end="")
        print("ITEM NAME".center(string_max, " "), end="")
        print("QUANTITY".center(string_max, " "), end="")
        print("PRICE".center(string_max, " "))

        for lst in self.inventory:
            items = self.inventory[lst]
            quantity = "%d" % int(items[1])
            price = "$%.2f" % float(items[2])
            print(str(lst).center(string_max, " "), end="")
            print(items[0].center(string_max, " "), end="")
            print(quantity.center(string_max, " "), end="")
            print(price.center(string_max, " "), end="")
            print()

    def prompt(self):
        '''
        prompt([]) --> void
        Prompts the user for commands and attempts to execute them.
        '''
        user_input = input("> ").split()
        user_input[0] = user_input[0].upper()
        if user_input[0] in self.commands:
            self.commands[user_input[0]](user_input[1::])
        else:
            print(f"{user_input[0]} is not a valid command. For a list of valid commands, please type 'help'.")


if debug:
    ##################################
    ############ Tests ###############
    ##################################

    # check_arg_count
    vm = VendingMachine()
    test_list = ["hi", "there", "test"]
    test = vm.check_arg_count(3, test_list)
    assert test, f"check_arg_count failed."

    test_list = [1, 2, 4, 5, 6, 1, 5]
    test = vm.check_arg_count(2, test_list)
    assert not test, f"check_arg_count failed"

    test = vm.check_arg_count(19, test_list)
    assert not test, f"check_arg_count failed"

    # logout
    vm.admin = True
    test = vm.logout([])
    assert test, f"logout() failed in {vm}."

    vm.admin = False
    test = vm.logout([])
    assert not test, f"logout() failed in {vm}."

    # change_password
    vm.admin = True
    test = vm.change_password(["change"])
    assert test, f"change_password() failed in {vm}."

    vm.admin = False
    test = vm.change_password(["NEW_PASSWORD!"])
    assert not test, f"change_password() failed in {vm}."

    # add_item
    vm.add_item(['b0', 'peanut_butter_crisps', '10', '1.50'])
    assert vm.inventory['B0'] == ['Ø (Empty)', '0', '0'], f"Erroneously allowed non-admin user to add items to inventory in {vm}."

    vm.admin = True
    vm.add_item(['B0', 'peanut_butter_crisps', '10', '1.50'])
    assert vm.inventory['B0'] == ['Peanut Butter Crisps', '10', '1.50'], f"add_item() failed in {vm}."

    vm.add_item(['b1', 'chocolate_bar', '10', '1.50'])
    assert vm.inventory['B1'] == ['Chocolate Bar', '10', '1.50'], f"add_item() failed in {vm}."

    #modify_price()
    vm.admin = True
    vm.add_item(["A0", "bag'o_chips", "5", "5.00"])
    test = vm.modify_price(["A0", "9.00"])
    assert test, f"modify_price() failed"

    vm.admin = True
    test = vm.modify_price(["Hello", "5.00"])
    assert not test, f"modify_price() failed"

    vm.admin = False
    test = vm.modify_price(["A9", "300"])
    assert not test, f"modify_price() failed"

    #increase_quantity()
    vm.admin = True
    vm.add_item(["A1", "bag'o_chips", "5", "5.00"])
    test = vm.increase_quantity(["A1", "9000"])
    assert test, f"increase_quantity() failed"

    vm.admin = False
    vm.add_item(["A4", "bag'o_chips", "5", "5.00"])
    test = vm.increase_quantity(["A4", "9000"])
    assert not test, f"increase_quantity() failed"

    vm.admin = True
    vm.add_item(["A3", "bag'o_chips", "5", "5.00"])
    test = vm.increase_quantity(["A2", "9000"])
    assert not test, f"increase_quantity() failed"

    #authenticate()
    test = vm.authenticate(["change"])
    assert test, f"authenticate() failed"
    
    test = vm.authenticate(["Password"])
    assert not test, f"authenticate() failed"



MY_VEN = VendingMachine()

while True:
    MY_VEN.prompt()
