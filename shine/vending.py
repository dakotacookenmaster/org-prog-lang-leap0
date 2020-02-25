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
        '''
        keys = self.inventory.keys()

        if id in keys:
            
            if id != []:
                print("This item costs: " + id[2])
                money = input("Please pay here: ")
                if money == id[2]:

        else:
            print("Invalid Choice")
            return False
        
        pass

    def view_inventory(self):
        pass

    def prompt(self):
        pass

myVen = VendingMachine() 
print(myVen.inventory)
# {id: [name, quantity, price]}