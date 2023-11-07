from Deck import Deck
from Card import Card
from HandScorer import HandScorer
import random, itertools
import time



class Game:

    def __init__(self):

        self.deck = Deck()
        self.H = HandScorer()
        
        self.playerhand = list()
        self.aihand = list()

        self.crib = list()
        self.starter = list()

        self.player_score = 0
        self.ai_score = 0

        self.dealer = "player"
        self.event_delay = 2

    def deal(self):

        self.deck.shuffle()

        self.playerhand = list()
        self.aihand = list()

        # deal 6 cards to player and AI
        for i in range(0, 12):
            if i % 2 == 0:
                self.playerhand.append(self.deck.shuffled.pop(0))
            else:
                self.aihand.append(self.deck.shuffled.pop(0))

        #print([str(item) for item in self.playerhand])

        # AI picks two random cards for crib
        self.crib.append(self.aihand.pop(random.randint(0, 5)))
        self.crib.append(self.aihand.pop(random.randint(0, 4)))

        # player picks two cards for crib
        #print("Pick the index of the first card to add to the crib, starting at 0:")

        # decide the first card to get rid of
        print()
        self.printhand(self.playerhand, True)
        print("Pick the index of the first card to add to the crib, starting at 0:")
        while True:
            try:
                ind = input()
                ind = ind
                if int(ind) not in range(0, len(self.playerhand)):
                    raise ValueError
                break

            except:
                print("invalid card selected")
        print()
        self.crib.append(self.playerhand.pop(int(ind)))
        
        # decide the second card to get rid of
        self.printhand(self.playerhand, True)
        print("Pick the index of the second card to add to the crib, starting at 0:")
        while True:
            try:
                ind = input()
                ind = ind
                if int(ind) not in range(0, len(self.playerhand)):
                    raise ValueError
                break

            except:
                print("invalid card selected")
        print()
        self.crib.append(self.playerhand.pop(int(ind)))

        # Clear the starter card, pick a starter card
        self.starter = list()
        self.starter.append(self.deck.shuffled.pop(0))

    def play_hand(self):

        print(self.dealer, "is dealing and will receive the crib.")
        self.deal()

        self.play_pegging2()

        if self.dealer == "player":
            self.score_ai_hand()
            time.sleep(self.event_delay)
            self.score_player_hand()
            time.sleep(self.event_delay)
            self.score_crib()
            time.sleep(self.event_delay)
            self.dealer = "ai"

        elif self.dealer == "ai":
            self.score_player_hand()
            time.sleep(self.event_delay)
            self.score_ai_hand()
            time.sleep(self.event_delay)
            self.score_crib()
            time.sleep(self.event_delay)
            self.dealer = "player"
        else:
            print("This line was reached in error. self.dealer was set incorrectly")

        print()
        print(f"Player score: {self.player_score}")
        print(f"AI score: {self.ai_score}")

    def play_is_possible(self, hand, sum):
        # check if it is possible to play at least one card from the given hand at the given pegging sum.

        is_possible = False
        possible_cards = list()

        for card in hand:
            if card.get_numeric_value() + sum <= 31:
                # if a card is playable, set is_possible to true
                is_possible = True
                # and add that card to the list of playable cards
                possible_cards.append(card)

        # if there were no possible cards, we return False, [None]
        return is_possible, possible_cards

    def printhand(self, hand, print_indices, startercard=False):
        if print_indices:
            i = 0
            for card in hand:
                if print_indices:
                    print(i, ": ", str(card))
                i += 1
        else:
            print([str(c) for c in hand])
            
        if startercard:
            print("Starter card: ", str(self.starter[0]))

    def play_pegging2(self):
        print("")

        # have the dealer and player alternate playing cards
        # we need to check for:
        #   runs played, either in or out of order

        # create copies of the player and AI hands so that we don't alter the actual hand when we pop off the stack
        player_hand = self.playerhand.copy()
        ai_hand = self.aihand.copy()

        # have the correct player start pegging (the one who did not deal)
        if self.dealer == "player":
            active_player = "ai"
        if self.dealer == "ai":
            active_player = "player"

        running_sum = 0
        played_cards = list()

        # keep looping as long as there are cards to play
        while len(player_hand)>0 or len(ai_hand)>0:

            # check if either player can legally play
            ai_poss, temp = self.play_is_possible(ai_hand, running_sum)
            player_poss, temp = self.play_is_possible(player_hand, running_sum)

            #if (not ai_poss) and (not player_poss) and running_sum != 31:
            if (not ai_poss) and (not player_poss):
                print("Neither the AI or player have valid cards to play")
                
                # give 1 for last points
                print(f"One for last!")

                if active_player == "player":
                    self.ai_score += 1

                elif active_player == "ai":
                    self.player_score += 1

                # if neither player can play, reset the sum and list of played cards
                running_sum = 0
                played_cards = list()

            else:

                print("Running total:", running_sum, "\n")
                
                # if at least one player can play, enter the card playing code

                # process the AI playing a card
                if active_player == "ai" and len(ai_hand)>0:
                    
                    # find the list of cards the AI could play
                    possible, playable_cards = self.play_is_possible(ai_hand, running_sum)

                    # It the AI can play, play a random valid card
                    if(possible):
                        ai_played_card = playable_cards.pop(random.randint(0, len(playable_cards)-1))
                        ai_hand.remove(ai_played_card)
                        print("\nAI played", ai_played_card)
                        played_cards.append(ai_played_card)
                        running_sum += ai_played_card.get_numeric_value()

                    else:
                        print("AI could not play.\n")
                        pass

                    time.sleep(self.event_delay)
                
                if active_player == "player" and len(player_hand)>0:
                    possible, playable_cards = self.play_is_possible(player_hand, running_sum)

                    if(possible):
                        print("Player hand cards that are valid plays:")
                        self.printhand(playable_cards, True)
                        print("Select the index of the card to play:")

                        while True:
                            try:
                                played_index = input()
                                if int(played_index) not in range(0, len(playable_cards)):
                                    raise ValueError
                                break

                            except:
                                print("invalid card selected")
                        print()
                        player_played_card = playable_cards.pop(int(played_index))
                        player_hand.remove(player_played_card)

                        print("Player played", player_played_card, "\n")
                        played_cards.append(player_played_card)

                        running_sum += player_played_card.get_numeric_value()

                    else:
                        print("There are no legal player moves.")
            
                # score hands
                points_for_active_player = self.compute_pegging_points(played_cards)

                # give points, swap players
                if active_player == "player":
                    self.player_score += points_for_active_player
                    active_player = "ai"

                elif active_player == "ai":
                    self.ai_score += points_for_active_player
                    active_player = "player"

    def compute_pegging_points(self, stack):
        points_for_active_player = 0

        # compute running sum
        running_sum = 0
        for c in stack:
            running_sum += c.get_numeric_value()
        
        # check for 15s
        if running_sum == 15:
            points_for_active_player += 2
            print("Fifteen for 2!")

        # check for 31s
        if running_sum == 31:
            points_for_active_player += 2
            print("Thirty-one for 2!")
            running_sum = 0

        # check for n of a kind:
        num_n_of_a_kind = self._check_n_of_a_kind(stack)
        if num_n_of_a_kind >= 2:
            points_for_active_player += (num_n_of_a_kind)*(num_n_of_a_kind-1)
            print(f"{num_n_of_a_kind} of a kind!")

        # check for runs
        points_from_run = self._check_run_in_pegging(stack)
        if points_from_run >= 3:
            print(f"Run of {points_from_run}!")
            points_for_active_player += points_from_run

        return points_for_active_player

    def _check_run_in_pegging(self, stack):

        # take a list of all the cards that have been played
        current_run_length = 0
        # get every sublist of the last N elements of the list

        if len(stack) <= 2:
            return 0

        for i in range(1, len(stack)):
            
            sublist = stack[-i:]

            # sort that sublist by rank
            sorted_ranks = list()
            for c in sublist:
                sorted_ranks.append(c.get_run_value())
            sorted_ranks.sort()

            diffs = list()
            # compute the differences between the elements of sorted_ranks
            for a, b in zip(sorted_ranks[0:-1], sorted_ranks[1:]):
                diffs.append(b-a)

            for elt in diffs:
                if elt != 1:
                    # not a run, we should exit and return the last valid length for a run (even if it is zero)
                    return current_run_length
                
            # if the difference between every element of the SORTED sublist is 1, we have a run of length N
            current_run_length = i

        return current_run_length

    def _check_n_of_a_kind(self, stack):

        n_of_a_kind = 1
        if(len(stack) > 0):
            newest_card = stack[-1]
        else:
            return 0
        # loop through the final n elements of the hand
        for l in range(1, len(stack)):
            
            # Get the last l cards of the hand 
            subhand = stack[(-1-l):-1]
            
            # if they all match, we have n of a kind
            for c in subhand:
                if c.get_run_value() != newest_card.get_run_value():
                    return n_of_a_kind
            n_of_a_kind = l

        return len(stack)

    def score_crib(self):

        print(f"\nScoring {self.dealer} crib...")
        self.printhand(self.crib, False, True)
        new_crib_score = self.H.scorehand(self.crib, self.starter[0])
        print("Crib scored", new_crib_score, "points.")
        if self.dealer == "player":
            self.player_score += new_crib_score
        elif self.dealer == "ai":
            self.ai_score += new_crib_score

    def score_player_hand(self):

        print("\nScoring player hand...")
        self.printhand(self.playerhand, False, True)
        new_player_score = self.H.scorehand(self.playerhand, self.starter[0])
        self.player_score += new_player_score
        print("Player scored", new_player_score, "points this hand.")
        print("Total player score:", self.player_score)

    def score_ai_hand(self):

        print("\nScoring AI hand...")
        self.printhand(self.aihand, False, True)
        new_ai_score = self.H.scorehand(self.aihand, self.starter[0])
        self.ai_score += new_ai_score
        print("AI scored", new_ai_score, "points this hand.")
        print("Total AI score:", self.ai_score)
    
    def score_hand(self, hand):
        score = 0

        # add starter card to scoring pool
        scoring_pool = hand
        scoring_pool.append(self.starter[0])

        self.printhand(scoring_pool, False)

        # check for pairs / three of a kind / four of a kind
        score_for_n_of_a_kind = self.score_n_of_a_kind(scoring_pool)
        score += score_for_n_of_a_kind

        # check for 15s
        score_for_15s = self.score_15s(scoring_pool)
        score += score_for_15s

        # check for runs
        run = self._check_for_runs(scoring_pool)

        if run[0] != 0:
            score = score + run[0]
            print(run[1], "\bx run of", run[2], "scored", run[0], "points!")

        # check for right jack
        for c in scoring_pool[0:-1]:
            if c.rank == "J" and c.suit == scoring_pool[-1].suit:
                print("The right jack!")
                score += 1

        # check for 4 or 5 (or more) of a suit
        points_from_flush = self._check_for_flush(scoring_pool)
        if points_from_flush != 0:
            print(f"Flush {points_from_flush}!")
            score += points_from_flush

        # print the score
        print("Score: ", score)

        return score


if __name__ == "__main__":


    G = Game()
    G.play_hand()


