from Game import Game
from Card import Card

G = Game()

hand = list()
hand.append(Card("1", "H"))
hand.append(Card("1", "H"))
hand.append(Card("2", "H"))
hand.append(Card("3", "H"))

hand.append(Card("5", "H"))
hand.append(Card("6", "H"))
hand.append(Card("7", "H"))

print([str(item) for item in hand])

G._check_for_runs(hand)
