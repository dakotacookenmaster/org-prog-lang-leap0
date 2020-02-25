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
        self.row_size = 10
        self.col_size = 10
        self.commands = {
            "INVENTORY": self.view_inventory,
            "PURCHASE": self.purchase_item,
            "ADD": self.add_item
        }
        
        # initialize the inventory to the sizes above
        for row in range(self.row_size):
            first_letter = chr(65 + row)
            for col in range(self.col_size):
                self.inventory[first_letter + str(col)] = []

    def purchase_item(self, id):
        '''purchase_item(id) --> bool;
        When passed an id, purchase_item will check if there are items in that id to purchase
        '''
        keys = self.inventory.keys()

        if id in keys:
            
            if self.inventory[id] != []:
                if self.inventory[id][1] != 0:
                    print("This item costs: " + str(self.inventory[id][2]))
                    self.request_currency(id)
                    print("Here is your " + self.inventory[id][0])
                    self.inventory[id][1] = self.inventory[id][1] - 1
                    return True
                else:
                    print("No longer in stock")
                    return False

            
            else:
                print("No longer in stock")
                return False

        else:
            print("Invalid Choice")
            return False
        

    def request_currency(self, id):
        '''
        request_currency(id) --> void
        Will continually request money until the price is met. Will return change if there is any

        >>> ven = VendingMachine()
        >>> ven.inventory["A0"] = ["Lay's Potato Chips", 28, 4.00]
        >>> ven.inventory["A1"] = ["Lay's Potato Chips", 0, 4.00]
        >>> ven.purchase_item("A0")
        True
        >>> ven.purchase_item("A1")
        False
        >>> ven.purchase_item("Z2")
        False
        '''
        money = int(input("Please pay here: "))

        while money < self.inventory[id][2]:
            money = money + int(input("Please add more money: "))
        
        if money > self.inventory[id][2]:
            money = money - self.inventory[id][2]
            print("Here is your change of: $%.2f" % money)

    def add_item(self):
        pass            

    def view_inventory(self):
        # Handle dynamic title width
        string_max = 0
        for item in self.inventory.values():
            local_max = max(x) if (x := list(map(len, item))) else 0
            if local_max > string_max:
                string_max = local_max
        string_max += 2 # add at least one space of padding on both sides of the largest string

        inventory_string_len = string_max * 4
        print("=" * inventory_string_len)
        print(" Vending Machine Inventory ".center(inventory_string_len, "="))
        print("=" * inventory_string_len)
        print("SLOT NUMBER".center(string_max, " "), end="")
        print("ITEM NAME".center(string_max, " "), end="")
        print("PRICE".center(string_max, " "), end="")
        print("QUANTITY".center(string_max, " "))
    
        for lst in self.inventory:
            print(str(lst).center(string_max, " "), end="")
            for item in self.inventory[lst]:
                print(str(item).center(string_max, " "), end="")
            print()

    def prompt(self):
        user_input = list(map(str.upper, input("> ").split()))
        print(user_input)
        if user_input[0] in self.commands:
            print(user_input[0] + " was entered!")
        else:
            print(f"{user_input[0]} is not a valid command. For a list of valid commands, please type 'help'.")


myVen = VendingMachine()
while(True):
    myVen.prompt()

print(myVen.inventory)

def _test():
    import doctest
    # doctest.testmod()


if __name__ == "__main__":
    _test()

myVen.inventory["A0"] = ["a", "abcdadfefaefaafeafedafxeadfasdafdaefeafdsafaefads", "aojfoaadjl"]
myVen.inventory["A1"] = ["a", "abcdadfefaefaafeafedafxeadfasdafdaefeafdsafaefads", "aojfoaadjl"]
myVen.view_inventory()
# {id: [name, quantity, price]}