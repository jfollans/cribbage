import itertools
from Card import Card
from HandScorer import HandScorer

valid_strategies = ["random", "greedy"]

class AI:

    def __init__(self):

        self.strategy = "greedy"

        pass

    def choose_crib_discards(self, hand):

        if self.strategy == "greedy":

            # loop through all possible pairs of cards to discard
            combs = itertools.combinations(hand, 4)
            max_score = -1
            H = HandScorer()
            current_chosen_hand = list()

            for subhand in combs:
                hand_score = H.scorehand(subhand)

                if hand_score > max_score:
                    max_score = hand_score
                    current_chosen_hand = subhand

            # now we have a list of 4 cards that maximizes the score
            # pop those 4 cards from the original hand to find the 2 cards to send to the crib

            for c in current_chosen_hand:
                hand.pop(c)
            cards_for_crib = hand

            print("Hand:")
            print([str(c) for c in current_chosen_hand])
            print("To crib:")
            print([str(c) for c in hand])

            return current_chosen_hand, cards_for_crib


        cards_for_crib = list()
        cards_for_crib.append(hand.pop(0))
        cards_for_crib.append(hand.pop(0))

        return hand, cards_for_crib
    
