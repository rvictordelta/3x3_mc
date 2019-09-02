import random
import operator
from statistics import median


class Card:
    def __init__(self, suit, kind, val):
        self.suit = suit
        self.kind = kind
        self.val = val

    def show(self):
        print(f'{self.kind} of {self.suit}')


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in ['Spades', 'Clubs', 'Diamonds', 'Hearts']:
            for kind_val in [['A', 14], ['2', 2], ['3', 3], ['4', 4], ['5', 5], ['6', 6], ['7', 7], ['8', 8], ['9', 9],
                             ['10', 10], ['J', 11], ['Q', 12], ['K', 13]]:
                self.cards.append(Card(suit, kind_val[0], kind_val[1]))

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def show(self):
        for c in self.cards:
            c.show()

    def drawCard(self):
        return self.cards.pop()

    def median(self):
        return median([c.val for c in self.cards])

    def cardsBelow(self, val):
        return sum([1 for c in self.cards if c.val < val])

    def cardsAbove(self, val):
        return sum([1 for c in self.cards if c.val > val])


# gameplay functions
def minmax_card(cards, minmax):
    values = [c.val for c in cards]
    if minmax.lower() == 'min':
        return min(enumerate(values), key=operator.itemgetter(1))
    elif minmax.lower() == 'max':
        return max(enumerate(values), key=operator.itemgetter(1))
    else:
        return -1, -1


def compare_cards(base, draw, call):
    if call == 'higher' and draw.val > base.val:
        return True
    elif call == 'lower' and draw.val < base.val:
        return True
    else:
        return False


def play():
    # create and shuffle deck
    deck = Deck()
    deck.shuffle()

    # deal game board
    board = [deck.drawCard() for i in range(9)]

    # play
    while len(board) > 0 and len(deck.cards) > 0:
        # decide which card to make what call on
        board_high_card_index, board_high_card_value = minmax_card(board, 'max')
        cards_below_highest = deck.cardsBelow(board_high_card_value)

        board_low_card_index, board_low_card_value = minmax_card(board, 'min')
        cards_above_lowest = deck.cardsAbove(board_low_card_value)

        if cards_above_lowest > cards_below_highest:
            board_selected_card_index, call = board_low_card_index, 'higher'
        else:
            board_selected_card_index, call = board_high_card_index, 'lower'

        # do it!
        reveal_card = deck.drawCard()
        result = compare_cards(board[board_selected_card_index], reveal_card, call)
        if result:
            # good call!
            board[board_selected_card_index] = reveal_card
        else:
            # bad call..
            del board[board_selected_card_index]
        # loop

    if len(board) == 0:
        return 0
    if len(deck.cards) == 0:
        return 1
    else:
        print('ERROR game not over')
        return -1


def run_sim():
    wins = 0
    for i in range(10000):
        wins += play()
    return wins


print(run_sim())

