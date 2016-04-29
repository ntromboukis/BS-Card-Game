import logging
import endpoints
from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue

from models import User, Game, Score
from models import StringMessage, NewGameForm, GameForm, MakeMoveForm,\
    ScoreForms
from utils import get_by_urlsafe

NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(
        urlsafe_game_key=messages.StringField(1),)
MAKE_MOVE_REQUEST = endpoints.ResourceContainer(
    MakeMoveForm,
    urlsafe_game_key=messages.StringField(1),)
USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))

@endpoints.api(name='bs_card_game', version='v1')
class BSGameApi(remote.Service):
  """Game API"""
  @endpoints.method(request_message=USER_REQUEST,
                    response_message=StringMessage,
                    path='user',
                    name='create_user',
                    http_method='POST')
  def create_user(self, request):
    if User.query(User.name == request.user_name).get():
      raise endpoints.ConflictException(
        'A User with that name already exists!')
    user = User(name=request.user_name, email=request.email)
    user.put()
    return StringMessage(message='User {} created!'.format(
      request.user_name))


  @endpoints.method(request_message=NEW_GAME_REQUEST,
                    response_message=GameForm,
                    path='game',
                    name='new_game',
                    http_method='POST')
  def new_game(self, request):
    user = User.query(User.name == request.user_name).get()
    if not user:
      raise endpoints.NotFoundException(
        'A User with that name does not exist!')
    try:
      game = Game.new_game(user.key, request.num_o, request.num_d)
      # maybe add num decks too
    except ValueError:
      raise endpoints.BadRequestException('Max must be greater than min!')
    return game.to_form('Good luck playing BullShit!')



api = endpoints.api_server([BSGameApi])


