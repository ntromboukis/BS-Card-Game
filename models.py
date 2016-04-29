from random import shuffle, randint
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb
# from bs_game import *


class Card(ndb.Model):
    card = ndb.StringProperty()


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    hand = ndb.StructuredProperty(Card, repeated=True)


class Player(ndb.Model):
    hand = ndb.StructuredProperty(Card, repeated=True)


class Game(ndb.Model):
    """Game object"""
    num_opponents = ndb.IntegerProperty(required=True)
    game_over = ndb.BooleanProperty(required=True, default=False)
    num_decks = ndb.IntegerProperty(default = 1)
    user = ndb.KeyProperty(required=True, kind='User')
    opponents = ndb.StructuredProperty(Player, repeated=True)

    @classmethod
    def new_game(cls, user, num_o, num_d):
        if num_o < 1:
            raise ValueError('Number of opponents must be greater then 1')
        # for every 7 players an additional deck is added.
        if num_o > 7:
            num_decks += num_o / 7

        game = Game(user=user,
                    game_over=False,
                    num_opponents=num_o,
                    num_decks=num_d)

        for i in range(num_o):
            # need to create new player objects and store them in ndb
            temp = Player()
            game.opponents = temp

    def to_form(self, message):
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.num_opponents = self.num_opponents
        form.hand = self.hand
        form.game_over = self.game_over
        form.message = message
        return form

    def end_game(self, won=False):
        self.game_over = True
        self.put()
        score = Score(user=self.user, date=date.today(), won=won, points=100)
        score.put()


class Score(ndb.Model):
    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    points = ndb.IntegerProperty(required=True)

    def to_form(self):
        return ScoreForm(user_name=self.user.get().name, won=self.won,
                     date=str(self.date), points=self.points)


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    hand = messages.StringField(2, required=True)
    game_over = messages.BooleanField(3, required=True)
    message = messages.StringField(4, required=True)
    user_name = messages.StringField(5, required=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_name = messages.StringField(1, required=True)
    num_o = messages.IntegerField(2, default=1)
    num_d = messages.IntegerField(3, default=1)


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    points = messages.IntegerField(4, required=True)


class MakeMoveForm(messages.Message):
    """Used to make a move in an existing game"""
    move = messages.IntegerField(1, required=True)


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)






