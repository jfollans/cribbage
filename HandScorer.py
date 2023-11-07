import itertools
from Card import Card


class HandScorer:


    def __init__(self, hand=None):

        if hand != None:
            assert len(hand) == 4, "Hand does not have length 4, exception!"
            self.hand = hand       
        pass

    
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

    def right_jack(self, scoring_pool):
        
        assert len(scoring_pool) == 5, "Not enough cards to decide right jack."
        
        # check for right jack
        for c in scoring_pool[0:-1]:
            if c.rank == "J" and c.suit == scoring_pool[-1].suit:
                print("The right jack!")
                return 1
        
        return 0

    def scorehand(self, hand, starter=None):
        score = 0

        # add starter card to scoring pool
        scoring_pool = hand
        if(starter != None):
            scoring_pool.append(starter)

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

        if starter != None:
            score += self.right_jack(scoring_pool)

        # print the score
        print("Score: ", score)

        return score
    

if __name__ == "__main__":

    H = HandScorer()

    hand = list()
    hand.append(Card("J", "H"))
    hand.append(Card("5", "D"))
    hand.append(Card("6", "S"))
    hand.append(Card("7", "C"))
    #hand.append(Card("5", "H"))

    print(H.scorehand(hand))
