from Deck import Deck
from Card import Card
import random, itertools
import time



class Game:

    def __init__(self):

        self.deck = Deck()
        
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

        # pick starter card
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

    def printhand(self, hand, print_indices):

        if print_indices:
            i = 0
            for card in hand:
                if print_indices:
                    print(i, ": ", str(card))
                i += 1
        else:
            print([str(c) for c in hand])

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

            if (not ai_poss) and (not player_poss) and running_sum != 31:
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
        new_crib_score = self.score_hand(self.crib)
        print("Crib scored", new_crib_score, "points.")
        if self.dealer == "player":
            self.player_score += new_crib_score
        elif self.dealer == "ai":
            self.ai_score += new_crib_score

    def score_player_hand(self):
        print("\nScoring player hand...")
        new_player_score = self.score_hand(self.playerhand)
        self.player_score += new_player_score
        print("Player scored", new_player_score, "points this hand.")
        print("Total player score:", self.player_score)

    def score_ai_hand(self):
        print("\nScoring AI hand...")
        new_ai_score = self.score_hand(self.aihand)
        self.ai_score += new_ai_score
        print("AI scored", new_ai_score, "points this hand.")
        print("Total AI score:", self.ai_score)

    def score_15s(self, hand):
        # check for 15s
        values_for_15s = list()
        num_15s = 0
        for card in hand:
            values_for_15s.append(card.get_numeric_value())

        score = 0

        # loop through combinations of all possible lengths
        for l in range(2, len(values_for_15s)):
            combs = itertools.combinations(values_for_15s, l)
            for i in combs:
                total = sum(i)      # check if this combination sums to 15
                if total == 15:
                    score = score + 2   # if so, add 2 to the score
                    num_15s += 1
                    
        if num_15s != 0:
            score_strings = [f"Fifteen {2*n}!" for n in range(1, num_15s+1)]
            for s in score_strings: print(s)
            pass

        return score
    
    def score_n_of_a_kind(self, hand):
        # check for pairs / three of a kind / four of a kind
        # create a dictionary for each rank, add one to the value for each of a card the hand has
        multiple_dict = dict()
        for card in hand:
            if card.rank not in multiple_dict:
                multiple_dict[card.rank] = 1
            else:
                multiple_dict[card.rank] += 1

        score = 0
        for item in multiple_dict.values():
            if item == 2:
                score = score + 2
                print("Pair!")
            if item == 3:
                score = score + 6
                print("Three of a kind!")
            if item == 4:
                score = score + 12
                print("Four of a kind!")

        return score

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

        # check for 4 or 5 (or more) of a suit
        points_from_flush = self._check_for_flush(scoring_pool)
        if points_from_flush != 0:
            print(f"Flush {points_from_flush}!")
            score += points_from_flush

        # print the score
        print("Score: ", score)

        return score

    def _check_for_flush(self, scoring_pool):
        # This method assumes that the last card in the scoring pool is the starter card!!

        # check for 4 or 5 (or more) of a suit
        suit_dict = dict()
        
        for card in scoring_pool[0:-1]:
            if card.suit not in suit_dict:
                suit_dict[card.suit] = 1
            else:
                suit_dict[card.suit] += 1

        points_from_flush = 0
        for key in suit_dict:
            if suit_dict[key] == 4 and scoring_pool[-1].suit == key:
                points_from_flush += 5
            elif suit_dict[key] == 4:
                points_from_flush += 4
        
        return points_from_flush

    def _check_for_runs(self, hand):

        no_dupes = set()
        for card in hand:
            no_dupes.add(card.get_run_value())
        
        no_dupes = list(no_dupes)
        no_dupes.sort()

        # calculate the difference between sequential elements
        temp2 = no_dupes[1:]
        temp1 = no_dupes[0:-1]
        diffs = list()

        for a, b in zip(temp1, temp2):
            diff = b - a
            diffs.append(diff)

        diffs.append(-10000) # add a dummy element to the end of the differences to be sure the calculation terminates

        # find all runs of three or more in diffs
        last_was_run = False
        run_indices = list()
        current_run_start = -1
        current_run_end = -1
        for i in range(0, len(diffs)-1):
            
            subarray = diffs[i:i+2]         # loop through all sequential subarrays with length 2. We only need 2 jumps of size 1 to make a run of 3
            
            run = False                     # check if sequential differences are 1
            
            if subarray[0] == 1 and subarray[1] == 1:
                run = True
            
            if run and last_was_run:        # if we're continuing an old run
                current_run_end = i+1
            
            elif run and not last_was_run:  # if we're starting a new run
                current_run_start = i
                last_was_run = True

            elif not run and last_was_run:  # if we're ending an old run
                current_run_end = i
                last_was_run = False
                run_indices.append((current_run_start, current_run_end))
                current_run_start = -1
                current_run_end = -1
            
            else:                           # if this isn't a run and the previous wasn't a run
                pass

        # create a duplicate dictionary
        multiple_dict = dict()
        for card in hand:
            if card.rank not in multiple_dict:
                multiple_dict[card.rank] = 1
            else:
                multiple_dict[card.rank] += 1


        # for each run of 3 or more, score it.
        # a singlet card adds 1 to the run score
        # x-of-a-kind cards add run to the run score, then multiply the multiplier by x
        runs_with_scores = list()
        for run in run_indices:
            
            run_elements = no_dupes[run[0]:run[1]+2]
            #print(run_elements)
            sum = 0
            mult = 1

            for elt in run_elements:
                sum += 1
                if elt == 11:
                    elt = "J"
                if elt == 12:
                    elt = "Q"
                if elt == 13:
                    elt = "K"
                else:
                    elt = str(elt)
                mult *= multiple_dict[elt]
            score = sum*mult

            runs_with_scores.append([score, mult, run_elements])
            #print("For", mult, "\bx run:", run_elements, "we score", score, "points")

        # find the run with the maximum score, return it:
        max_score = 0
        final_mult = -1
        run_for_max_score = []
        for elt in runs_with_scores:
            if elt[0] > max_score:
                max_score = elt[0]
                final_mult = elt[1]
                run_for_max_score = elt[2]

        return [max_score, final_mult, run_for_max_score]


if __name__ == "__main__":


    G = Game()
    
    #hand = list()
    #hand.append(Card(5, "H"))
    #hand.append(Card(5, "H"))
    #hand.append(Card(5, "H"))
    #hand.append(Card(5, "H"))
    #hand.append(Card(5, "D"))
    #print(G._check_for_flush(hand))

    G.play_hand()


