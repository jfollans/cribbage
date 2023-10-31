from Deck import Deck
from Card import Card
import random, itertools

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

    def play_hand(self):

        print(self.dealer, "is dealing and will receive the crib.")
        self.deal()

        self.play_pegging()

        if self.dealer == "player":
            self.score_ai_hand()
            self.score_player_hand()
            self.score_crib()
            self.dealer = "ai"

        elif self.dealer == "ai":
            self.score_player_hand()
            self.score_ai_hand()
            self.score_crib()
            self.dealer = "player"
        else:
            print("This line was reached in error. self.dealer was set incorrectly")
        

    def play_pegging(self):


        print("")
        # have the dealer and player alternate playing cards
        # we need to check for:
        #   pairs / 3 / 4+ of a kind played in a row
        #   runs played, either in or out of order
        #   15's
        #   31's

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

        # while there are still cards left to play
        while len(player_hand) > 0 or len(ai_hand) > 0:

            if active_player == "ai" and len(ai_hand)>0:
                
                # pop a random card off the AI hand and add it to the played cards
                ai_played_card = ai_hand.pop(random.randint(0, len(ai_hand)-1))
                print("\nAI played", ai_played_card)
                played_cards.append(ai_played_card)

            if active_player == "player":
                print("\nRemaining player hand:")
                print([str(item) for item in player_hand])
                print("Select the index of the card to play:")
                played_index = input()

                player_played_card = player_hand.pop(int(played_index)) 
                print("Player played", player_played_card)
                played_cards.append(player_played_card)


                pass


            running_sum += played_cards[-1].get_numeric_value()
            print("Running total:", running_sum)

            # SCORE HAND

            # Set which player goes next
            if active_player == "player":
                active_player = "ai"
            elif active_player == "ai":
                active_player = "player"

        pass



    def score_crib(self):
        print("\nScoring crib for", self.dealer)
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

    def deal(self):

        self.deck.shuffle()

        # deal 6 cards to player and AI
        for i in range(0, 12):
            if i % 2 == 0:
                self.playerhand.append(self.deck.shuffled.pop(0))
            else:
                self.aihand.append(self.deck.shuffled.pop(0))

        print([str(item) for item in self.playerhand])

        # AI picks two random cards for crib
        self.crib.append(self.aihand.pop(random.randint(0, 5)))
        self.crib.append(self.aihand.pop(random.randint(0, 4)))

        # player picks two cards for crib
        print("Pick the index of the first card to add to the crib, starting at 0:")
        ind = input()
        self.crib.append(self.playerhand.pop(int(ind)))

        print("")
        print([str(item) for item in self.playerhand])
        print("Pick the index of the second card to add to the crib, starting at 0:")
        ind = input()
        self.crib.append(self.playerhand.pop(int(ind)))

        # pick starter card
        self.starter.append(self.deck.shuffled.pop(0))

    def score_hand(self, hand):

        score = 0

        # add starter card to scoring pool
        scoring_pool = hand
        scoring_pool.append(self.starter[0])


        # check for pairs / three of a kind / four of a kind
        # create a dictionary for each rank, add one to the value for each of a card the hand has
        multiple_dict = dict()
        for card in scoring_pool:
            if card.rank not in multiple_dict:
                multiple_dict[card.rank] = 1
            else:
                multiple_dict[card.rank] += 1


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


        # check for 15s
        values_for_15s = list()
        num_15s = 0
        for card in scoring_pool:
            values_for_15s.append(card.get_numeric_value())


        # loop through combinations of all possible lengths
        for l in range(2, len(values_for_15s)):
            combs = itertools.combinations(values_for_15s, l)
            for i in combs:
                total = sum(i)      # check if this combination sums to 15
                if total == 15:
                    score = score + 2   # if so, add 2 to the score
                    num_15s += 1
                    
        if num_15s != 0:
            print(num_15s, "x 15s!")
            pass


        # check for runs
        run = self._check_for_runs(scoring_pool)
        if run[0] != 0:
            score = score + run[0]
            print(run[1], "\bx run of", run[2], "scored", run[0], "points!")

        # check for 4 or 5 (or more) of a suit
        suit_dict = dict()
        for card in scoring_pool:
            if card.suit not in suit_dict:
                suit_dict[card.suit] = 1
            else:
                suit_dict[card.suit] += 1
        print("Suit dict:", suit_dict)

        # print scoring pool and score
        print([str(item) for item in scoring_pool])
        print("Score: ", score)

        return score

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
    G.play_hand()
