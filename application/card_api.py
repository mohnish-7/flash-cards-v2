from flask_restful import Resource
from flask_restful import fields, marshal_with
from application.database import db
from application.models import User, Decks, Cards
from application.validation import NotFoundError, BusinessValidationError
from flask_restful import reqparse
from application.misc import *

card_fields = {
    "card_id" : fields.Integer,
    "card_title" : fields.String,
    "card_content" : fields.String,
}

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('card_title')
create_user_parser.add_argument('card_content')
create_user_parser.add_argument('card_id')
create_user_parser.add_argument('deck_name')
create_user_parser.add_argument('deck_id')
create_user_parser.add_argument('username')
create_user_parser.add_argument('new_card_content')


update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument('new_content')
update_user_parser.add_argument('card_title')
update_user_parser.add_argument('deck_id')
class CardAPI(Resource):


    @marshal_with(card_fields)
    def get(self, card_id):

        print('\nIn CardAPI GET Method\n')
        # querying the database
        card = db.session.query(Cards).filter(Cards.card_id == card_id).first()

        if card:
            #return valid user json
            return card
        else:
            # return 404 error
            raise NotFoundError(404)


    @marshal_with(card_fields)
    def put(self):
        try:
            print('\nIn CardAPI PUT Method\n')
            card_title = update_user_parser.parse_args().get("card_title", None)
            new_content = update_user_parser.parse_args().get("new_content", None)
            deck_id = update_user_parser.parse_args().get("deck_id", None)
            if card_title is None:
                raise BusinessValidationError(status_code=400, error_code="BE101", error_msg="Card Name/Title is required")
            if new_content is None:
                raise BusinessValidationError(status_code=400, error_code="BE101", error_msg="new_content required")

            cards = []
            deck = db.session.query(Decks).filter(Decks.deck_id == deck_id).one()
            all_cards = db.session.query(Cards).filter(Cards.card_title == card_title).all()
            for c in all_cards:
                if deck in c.deck:
                    cards.append(c)
            if len(cards) > 0:
                for card in cards:
                    card.card_content = new_content
                    db.session.add(card)
                    db.session.commit()
                return cards, 200
            else:
                raise BusinessValidationError(status_code=400, error_code="BE102", error_msg="Card doesn't exist.")


        except:
            # return 404 error
            raise
            raise NotFoundError(404)

    @marshal_with(card_fields)
    def delete(self):

        print('\nIn CardAPI DELETE Method\n')
        args = create_user_parser.parse_args()
        card_title = args.get("card_title", None)
        deck_id = args.get("deck_id", None)

        try:
            cards = []
            deck = db.session.query(Decks).filter(Decks.deck_id == deck_id).one()
            all_cards = db.session.query(Cards).filter(Cards.card_title == card_title).all()
            for c in all_cards:
                if deck in c.deck:
                    cards.append(c)
            if len(cards) > 0:
                for card in cards:
                    delete_card(card.card_title,deck_id)
                return cards, 200
            else:
                return []

            return card,200

        except:
            # return 400 error
            raise BusinessValidationError(status_code=400, error_code="BE102", error_msg="Card doesn't exist")



    @marshal_with(card_fields)
    def post(self):

        print('\nIn CardAPI POST Method\n')
        args = create_user_parser.parse_args()
        username = args.get("username", None)
        deck_id = args.get("deck_id", None)
        card_title = args.get("card_title", None)
        card_content = args.get("card_content", None)

        if card_title is None:
            raise BusinessValidationError(status_code=400, error_code="BE101", error_msg="card_title is required")



        try:
            decks = []
            cards = []
            user = db.session.query(User).filter(User.username == username).one()
            deck = db.session.query(Decks).filter(Decks.deck_id == deck_id).one()
            new_card = Cards(card_title=card_title, card_content=card_content)
            new_card.deck.append(deck)
            db.session.add(new_card)
            db.session.commit()

            return new_card,201

        except:
            raise BusinessValidationError(status_code=400, error_code="BE102", error_msg="deck_name doesn't exist")
