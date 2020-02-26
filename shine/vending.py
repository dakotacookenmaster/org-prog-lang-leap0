# LEAP 0: *Shine*
# CPTR-405-A: Organization of Programming Languages
# filename: vending.py
# Programmed by:
#   Dakota Cookenmaster
#   Michael Yoon
# Last edit: 02/25/2020

class VendingMachine():
    def __init__(self):
        ''' Constructs a VendingMachine object and initializes the inventory to a default 10 x 10. '''
        self.inventory = {}
        self.row_size = 5
        self.col_size = 5
        self.admin = False
        self.admin_password = "admin"
        self.commands = {
            "INVENTORY": self.view_inventory,
            "PURCHASE": self.purchase_item,
            "ADD": self.add_item,
            "HELP": self.sys_help,
            "EXIT": self.sys_exit,
            "ADMIN": self.authenticate,
            "BOOST": self.add_to_inventory,
            "PRICE": self.modify_price,
        }
        
        # initialize the inventory to the sizes above
        for row in range(self.row_size):
            first_letter = chr(65 + row)
            for col in range(self.col_size):
                self.inventory[first_letter + str(col)] = []

    def sys_help(self, arg_list):
        print()
        print("All users have access to the following commands:")
        print("'inventory' --> prints the vending machine's current inventory.")
        print("'purchase' SLOT_NUMBER --> initiates the purchasing process for the given SLOT_NUMBER.")
        print("'help' --> accesses this help file.")
        print()
        print("Admin-only commands:")
        print("'add' SLOT_NUMBER NAME QUANTITY PRICE --> adds a new item to the vending machine's inventory. " \
              "If you need spaces in the name of the product, replace them with underscores (i.e. '_') instead.")
        print("'exit' --> initiates the vending machine shutdown.")
        print("'boost' SLOT_NUMBER QUANTITY --> increases the current quantity of the given SLOT_NUMBER by the given QUANTITY.")
        print("'price' SLOT_NUMBER PRICE --> changes the current price of the given SLOT_NUMBER to the given PRICE")
        print("'admin' PASSWORD --> promotes the current user to admin if the PASSWORD is authenticated.")
        print()

    def modify_price(self, arg_list):
        if self.admin:
            if len(arg_list) != 2:
                print("Please type 'price' followed by the SLOT_NUMBER and the PRICE you wish to change it to.")
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
        else:
            self.auth_required()

    def add_to_inventory(self, arg_list):

        if self.admin:
            if len(arg_list) != 2:
                print("Please type 'boost' followed by the SLOT_NUMBER and the QUANTITY you wish to boost it by.")
                return False
            
            slot_number = arg_list[0].upper()
            quantity = int(arg_list[1])

            try:
                self.inventory[slot_number][1] = str(int(self.inventory[slot_number][1]) + quantity)
                return True
            except Exception:
                print("Unable to boost inventory. Check to make sure your command was structured correctly.")
        else:
            self.auth_required()
        
    def authenticate(self, arg_list):
        """
        authenticate(password) --> bool
        Returns True if authentication was successful, else returns False
        Changes the user mode from user to admin.
        """
        if len(arg_list) != 1:
            print("Please enter the keyword 'admin' followed by your password.")
            return False

        pw = arg_list[0]

        if pw == self.admin_password:
            self.admin = True
            print("Authentication was successful.")
        else:
            self.auth_failed()

    def auth_failed(self):
        print("The password you entered was invalid. Please try again.")

    def auth_required(self):
        print("You do not have the authorization to execute that command. Type 'admin' followed by your password to enable this feature.")

    def sys_exit(self, arg_list):
        '''
        sys_exit() --> void
        Exits from the current program.
        '''
        if self.admin:
            exit(0)
        else:
            self.auth_required()

    def function_not_implemented(self, arg_list):
        print("This function has not yet been implemented.")

    def purchase_item(self, arg_list):
        '''purchase_item(item_id) --> bool;
        When passed an item_id, purchase_item will check if there are items in that item_id to purchase
        '''
        keys = self.inventory.keys()
        if len(arg_list) != 1:
            print("Please type 'purchase' without the quotes followed by the SLOT_NUMBER you would like to purchase (e.g. purchase A0).")
            return False
        
        item_id = arg_list[0].upper()

        if item_id in keys:
            if self.inventory[item_id] != []:
                if int(self.inventory[item_id][1]) != 0:
                    print("This item costs: " + str(self.inventory[item_id][2]))
                    self.request_currency(item_id)
                    print(f"Now vending: {self.inventory[item_id][0]}.")
                    self.inventory[item_id][1] = str(int(self.inventory[item_id][1]) - 1)
                    return True
                else:
                    print("That slot is out of stock. Please try again.")
                    return False

            else:
                print("That slot is out of stock. Please try again.")
                return False

        else:
            print("Invalid Choice. Please try again.")
            return False

    def request_currency(self, item_id):
        '''
        request_currency(item_id) --> void
        Will continually request money until the price is met. Will return change if there is any.

        >>> ven = VendingMachine()
        >>> ven.inventory["A0"] = [Lay's_Potato_Chips, 28, 4.00]
        >>> ven.inventory["A1"] = [Lay's_Potato_Chips", 0, 4.00]
        >>> ven.purchase_item("A0")
        True
        >>> ven.purchase_item("A1")
        False
        >>> ven.purchase_item("Z2")
        False
        '''
        price = float(self.inventory[item_id][2])
        money = float(input("Please pay here: "))

        while money < float(price):
            remaining = price - money
            try:
                money = money + float(input("Please add more money (%.2f remaining): " % remaining))
            except Exception:
                print("Please enter a valid monetary amount.")
     
        if money > price:
            money = money - price
            print("Here is your change of: $%.2f" % money)

    def add_item(self, arg_list):
        '''
        add_item([slot_number, name, quantity, price]) --> bool
        Attempts to add an item to the vending machine inventory.
        If the item already exists, allows user to choose to replace
        or cancel the operation. Returns True if the item was added
        (or replaced), otherwise False. 
        '''
        if self.admin:
            if len(arg_list) != 4:
                print("Please specify the appropriate SLOT_NUMBER, NAME, QUANTITY, and PRICE in order to add an item.")
                return False

            slot_number = arg_list[0].upper()
            name = " ".join(list(map(str.capitalize, arg_list[1].replace("_", " ").split())))
            quantity = arg_list[2]
            price = arg_list[3]

            if slot_number not in self.inventory:
                print(f"The SLOT_NUMBER '{slot_number}' is invalid. Operation cancelled.")
                return False
            
            if (not self.inventory[slot_number]) or (self.inventory[slot_number][1] == 0):
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
        view_inventory(arg_list)
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
            print(str(lst).center(string_max, " "), end="")
            for item in self.inventory[lst]:
                print(str(item).center(string_max, " "), end="")
            print()

    def prompt(self):
        '''
        prompt() --> void
        Prompts the user for commands and attempts to execute them.
        '''
        user_input = input("> ").split()
        user_input[0] = user_input[0].upper()
        if user_input[0] in self.commands:
            self.commands[user_input[0]](user_input[1::])
        else:
            print(f"{user_input[0]} is not a valid command. For a list of valid commands, please type 'help'.")


MY_VEN = VendingMachine()

while True:
    MY_VEN.prompt()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
