from random import shuffle, randint
import json


class Deck(object):

    def __init__(self, num):
        self.cards = []
        self.numCards = 52 * num
        for i in range(self.numCards):
            self.cards.append(Card(i))

    def shuffle_deck(self):
        shuffle(self.cards)

    def deal_card(self):
        if self.numCards > 0:
            self.numCards = self.numCards - 1
            return self.cards.pop()
        else:
            return None

    def cut_deck(self):
        if self.numCards > 0:
            for i in range(randint(0, self.numCards)):
                self.cards.insert(0, self.cards.pop())
        else:
            None

    def get_size(self):
        return len(self.cards)

    def is_empty(self):
        return (self.numCards == 0)

    def __str__(self):
        for i in self.cards:
            return "%s" % '\n'.join(map(str, self.cards))


class Card(object):

    def __init__(self, num):

        self.cardTup = ()
        value = num % 13
        if value == 0:
            value = 13
        suitNumber = num / 13
        if suitNumber == 0:
            suit = 'clubs'
        elif suitNumber == 1:
            suit = 'diamonds'
        elif suitNumber == 2:
            suit = 'hearts'
        elif suitNumber == 3:
            suit = 'spades'
        else:
            suit = 'ERROR'
        self.cardTup = (value, suit)

    def get_value(self):
        return self.cardTup[0]

    def get_suit(self):
        return self.cardTup[1]

    def equals_value(self, otherCard):
        return (self.cardTup[0] == otherCard.cardTup[0])

    def equals_suit(self, otherCard):
        return (self.cardTup[1] == otherCard.cardTup[1])

    def __str__(self):
        if self.cardTup[0] == 1:
            return ('Ace of %s' % (self.cardTup[1]))
        elif self.cardTup[0] == 11:
            return ('Jack of %s' % (self.cardTup[1]))
        elif self.cardTup[0] == 12:
            return ('Queen of %s' % (self.cardTup[1]))
        elif self.cardTup[0] == 13:
            return ('King of %s' % (self.cardTup[1]))
        elif self.cardTup[0] == 14:
            return (self.cardTup[1])
        else:
            return ('%s of %s' % (self.cardTup[0], self.cardTup[1]))


class Game(object):

    def __init__(self, user_name):
        self.game = {}
        self.game['main'] = user_name

    """minp, maxp, and num must be of type int
    ValueError handling done in this method for only num"""
    def new_game(self, num, minp, maxp):
        try:
            self.num_opponents = int(num)
        except ValueError:
            raise ValueError
        if minp <= self.num_opponents <= maxp:
            for i in range(self.num_opponents):
                temp = Player()
                self.game['player%s' % i] = temp
        else:
            raise ValueError
    # finish this ----------
    def play_opponent(self, pos, pile, target):
        self.game[pos].put_card_in_pile()

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def deal_cards(self, deck):
        while deck.is_empty() != True:
            for i in self.game:
                self.game[i].draw_card_from_deck(deck)


class Hand(object):

    def __init__(self):
        self.card_hand = []

    def add_card(self, card):
        self.card_hand.append(card)

    def remove_card(self, pos):
        temp = self.card_hand[pos]
        del(self.card_hand[pos])
        return temp

    def sort_by_value(self):
        self.card_hand.sort()

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def __str__(self):
        for i in self.card_hand:
            return '%s' % '\n'.join(map(str, self.card_hand))


class Pile(object):

    def __init__(self):
        self.cardPile = []

    def add_card(self, card):
        self.cardPile.append(card)

    def remove_card(self):
        temp = cardPile.pop()
        return temp

    def remove_cards(self, num):
        removed = []
        for i in range(num):
            removed.append(self.cardPile.pop())
        return removed

    def get_size(self):
        return len(self.cardPile)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def __str__(self):
        for i in self.cardPile:
            return '%s' % '\n'.join(map(str, self.cardPile))


class Player(object):

    def __init__(self):
        self.hand = Hand()

    def draw_card_from_deck(self, deck):
        temp = deck.deal_card()
        self.hand.add_card(temp)

    def put_card_in_pile(self, pile, pos):
        temp = self.hand.remove_card(pos)
        pile.add_card(temp)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def call_bs(self, pile, num, target):
        j = 0
        for i in range(num):
            if pile[i].equals_value(target):
                j = j + 1
            else:
                return False
        if j == num:
            return True
