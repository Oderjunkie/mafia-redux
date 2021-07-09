from graphene import ObjectType, Mutation, String, Schema, Int, Field, List
from mods.setupflask import app, client
from flask_graphql import GraphQLView

class User(ObjectType):
    '''Represents a YAMR account.'''
    id = String(required=True)
    username = String(required=True)
    wins = Int()
    losses = Int()

class Room(ObjectType):
    '''Represents a Room.'''
    id = String(required=True)
    name = String(required=True)

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
    
    def resolve_room(root, info, id=None, username=None):
        query = {'roomid': id} if id else {'name': username} if username else {}
        query = {'listed': True, **query}
        projection = {'_id': 0, 'listed': 0}
        return [Room(id=room['roomid'],
                     name=room['name']) for room in \
                client.mafiaredux.rooms.find(query, projection)]
    
    def resolve_unlistedroomcount(root, info):
        return client.mafiaredux.rooms.count_documents({'listed': False})

# class RootMutation(Mutation):
#     pass

schema = Schema(
    query=RootQuery#,
    #mutation=RootMutation
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