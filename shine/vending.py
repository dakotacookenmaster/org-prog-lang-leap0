# LEAP 0: *Shine*
# CPTR-405-A: Organization of Programming Languages
# filename: vending.py
# Programmed by:
#   Dakota Cookenmaster
#   Michael Yoon
# Last edit: 02/25/2020

class VendingMachine():
    def __init__(self):
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

        >>> purchase_item('A0')

        '''
        keys = self.inventory.keys()

        if id in keys:
            
            if self.inventory[id] != []:
                print("This item costs: " + self.inventory[id[2]])
                self.request_currency(id)
                print("Here is your " + self.inventory[id[0]])
                self.inventory[id[1]] = self.inventory[id[1]] - 1
                return True
            
            else:
                print("No longer in stock")
                return False

        else:
            print("Invalid Choice")
            return False
        

    def request_currency(self, id):
        '''Will continually request money until the price is met. Will return change if there is any
        '''
        money = int(input("Please pay here: "))

        while money < self.inventory[id[2]]:
            money = money + int(input("Please add more money: "))
        
        if money > self.inventory[id[2]]:
            money = money - self.inventory[id[2]]
            print("Here is your change of: $" + money)


                
        

    def view_inventory(self):
        pass

    def prompt(self):
        pass


myVen = VendingMachine() 
print(myVen.inventory)

def _test():
    import doctest
    doctest.testmod()

    {A0: }


if __name__ == "__main__":
    _test()

# {id: [name, quantity, price]}