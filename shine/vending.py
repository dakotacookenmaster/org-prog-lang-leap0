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
        >>> ven.purchase_item('A1")
        False
        >>> ven.purchse_item("Z2")
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
            local_max = 0 # if x := list(map(len, item)).empty()
            if local_max > string_max:
                string_max = local_max

        print("=" * (string_max // 2))
        for item in self.inventory:
            print(self.inventory[item])

    def prompt(self):
        pass


myVen = VendingMachine() 
print(myVen.inventory)

def _test():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    _test()

myVen.inventory["A0"] = ["a", "abcdadfefaefads", "ajfoejaojfoaj9ejaojfoaadjl"]
myVen.view_inventory()
# {id: [name, quantity, price]}