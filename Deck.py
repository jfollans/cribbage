from Card import Card
import random


class Deck:

    def __init__(self):

        suits = ["H", "D", "S", "C"]
        ranks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

        self.available_cards = list()

        for s in suits:
            for r in ranks:
                self.available_cards.append(Card(r, s))

        self.shuffled = self.shuffle()


    def shuffle(self):
        temp = list()
        tempdeck = self.available_cards.copy()

        for i in range(0, len(self.available_cards)):
            temp.append( tempdeck.pop( random.randint( 0, len(tempdeck)-1 ) ) )

        return temp
