



class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank + "" + self.suit
    
    def __eq__(self, other):

        if other == None:
            return False

        return self.rank == other.rank and self.suit == other.suit
    
    def get_numeric_value(self):

        if self.rank in ["J", "Q", "K"]:
            return 10
        else:
            return int(self.rank)
        
        print("Error!")
        return -1
    
    def get_run_value(self):
        if self.rank == "J":
            return 11
        if self.rank == "Q":
            return 12
        if self.rank == "K":
            return 13
        else:
            return int(self.rank)
        
        