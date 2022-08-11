from flask_restful import Resource
from flask_restful import fields, marshal_with
from application.database import db
from application.models import User, Decks
from application.validation import NotFoundError, BusinessValidationError
from flask_restful import reqparse
from application.misc import *
from main import cache

deck_fields = {
    "deck_id" : fields.Integer,
    "deck_name" : fields.String,
    "score" : fields.String,
    "last_review" : fields.String,
    "num" : fields.Integer
}

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username')
create_user_parser.add_argument('deck_name')


update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument('deck_name')
update_user_parser.add_argument('new_name')

class DeckAPI(Resource):


    @marshal_with(deck_fields)
    @cache.cached(timeout=30, key_prefix='deck_api_get')
    # @cache.memoize(50)
    def get(self, username):
        print('\n In DeckAPI GET Method\n')
        # querying the database
        # deck = db.session.query(Decks).filter(Decks.deck_name == deck_name).first()
        decks = Decks.query.filter(Decks.owner.any(username=username))
        if len(list(decks)) > 0:
            #return valid user json
            return list(decks)
        else:
            # return 404 error
            return []


    @marshal_with(deck_fields)
    @cache.memoize(10)
    def put(self):

        print('\n In DeckAPI PUT Method\n')
        deck_name = update_user_parser.parse_args().get("deck_name", None)
        new_name = update_user_parser.parse_args().get("new_name", None)
        if new_name is None:
            raise BusinessValidationError(status_code=400, error_code="BE101", error_msg="new_name required")
        if deck_name is None:
            raise BusinessValidationError(status_code=400, error_code="BE101", error_msg="deck_name required")
        deck = db.session.query(Decks).filter(Decks.deck_name == deck_name).first()

        if deck:
            deck.deck_name = new_name
            db.session.add(deck)
            db.session.commit()
            return deck, 200

        else:
            # return 404 error
            raise NotFoundError(404)

    @marshal_with(deck_fields)
    def delete(self):

        print('\n In DeckAPI DELETE Method\n')
        args = create_user_parser.parse_args()
        username = args.get("username", None)
        deck_name = args.get("deck_name", None)

        try:
            decks = []
            user = db.session.query(User).filter(User.username == username).one()
            all_decks = db.session.query(Decks).filter(Decks.deck_name == deck_name).all()
            for d in all_decks:
                if user in d.owner:
                    decks.append(d)

            for d in decks:
                delete_deck(d.deck_name,username)
            return decks, 200

        except:
            # return 400 error
            raise #BusinessValidationError(status_code=400, error_code="BE102", error_msg="Deck doesn't exist")



    @marshal_with(deck_fields)
    def post(self):

        print('\n In DeckAPI POST Method\n')
        args = create_user_parser.parse_args()
        deck_name = args.get("deck_name", None)
        username = args.get("username", None)

        if username is None:
            raise BusinessValidationError(status_code=400, error_code="BE101", error_msg="username is required")

        if deck_name is None:

            raise BusinessValidationError(status_code=400, error_code="BE101", error_msg="deck_name is required")

        try:
            user = db.session.query(User).filter(User.username == username).one()
            new_deck = Decks(deck_name=deck_name,score=0,last_review='NA',num=0)
            new_deck.owner.append(user)
            db.session.add(new_deck)
            db.session.commit()

            return new_deck, 201

        except:
            raise BusinessValidationError(status_code=400, error_code="BE102", error_msg="username doesn't exist")
