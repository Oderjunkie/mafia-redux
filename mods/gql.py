from graphene import ObjectType, Mutation, String, Schema, Int, Field, List, JSONString
from mods.setupflask import app, client
from flask_graphql import GraphQLView
from mods.utilities import randString
import bcrypt

class User(ObjectType):
    '''Represents a YAMR account.'''
    id = String(required=True)
    username = String(required=True)
    wins = Int()
    losses = Int()

class SelfUser(ObjectType):
    '''Represents your YAMR account.'''
    id = String(required=True)
    username = String(required=True)
    wins = Int()
    losses = Int()
    token = String(required=True)

class Room(ObjectType):
    '''Represents a Room.'''
    id = String(required=True)
    name = String(required=True)
    setup = JSONString(required=True)
    events = JSONString(required=True)

class RootQuery(ObjectType):
    user = Field(
        List(User),
        id=String(required=False, default_value=None),
        username=String(required=False, default_value=None)
    )
    room = Field(
        List(Room),
        id=String(required=False, default_value=None),
        name=String(required=False, default_value=None)
    )
    unlistedroomcount = Int(required=True)

    def resolve_user(root, info, id=None, username=None):
        # [field.name.value for field in info.field_asts[0].selection_set.selections]
        # return [User(username='Otesunki', id=1337)]
        query = {'userid': id} if id else {'username': username} if username else {}
        projection = {'_id': 0, 'userhash': 0}
        return [User(id=user['userid'],
                     username=user['username'],
                     wins=user['wins'],
                     losses=user['losses']) for user in \
                client.mafiaredux.users.find(query, projection)]
    
    def resolve_room(root, info, id=None, name=None, setup=None, events=None):
        query = {'roomid': id} if id else {'name': name} if name else {}
        query = {'listed': True, **query}
        projection = {'_id': 0, 'listed': 0}
        return [Room(id=room['roomid'],
                     name=room['name'],
                     setup=room['setup'],
                     events=room['events']) for room in \
                client.mafiaredux.rooms.find(query, projection)]
    
    def resolve_unlistedroomcount(root, info):
        return client.mafiaredux.rooms.count_documents({'listed': False})

class MakeUser(Mutation):
    class Arguments:
        username = String()
        password = String()
    
    self = Field(lambda: SelfUser)
    error = String(required=False)
    
    def mutate(root, info, username, password):
        if client.mafiaredux.users.count_documents({'username': username}):
            return MakeUser(self=None, error='That username is taken.')
        userid = randString(30)
        userhash = bcrypt.hashpw(password.encode('latin-1'), bcrypt.gensalt())
        client.mafiaredux.users.insert_one({
            'username': username,
            'userid': userid,
            'userhash': userhash,
            'wins': 0,
            'losses': 0
        })
        usertoken = randString(30)
        client.mafiaredux.cookies.insert_one({
            'token': usertoken,
            'id': userid
        })
        return MakeUser(self=SelfUser(id=id, username=username, wins=0, losses=0, token=usertoken), error=None)

class RootMutation(ObjectType):
    make_user = MakeUser

schema = Schema(
    query=RootQuery,
    mutation=RootMutation
)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True
))

# app.add_url_rule('/graphql/batch', view_func=GraphQLView.as_view(
#     'graphql',
#     schema=schema,
#     batch=True
# ))