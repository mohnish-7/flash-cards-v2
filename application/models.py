from application.database import db
from flask_security import UserMixin, RoleMixin

roles_users = db.Table('roles_users',
                            db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                            db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin):

    __tabelname__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Decks(db.Model):

	__tabelname__ = 'decks'
	deck_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	deck_name = db.Column(db.String, nullable=False)
	score = db.Column(db.String)
	last_review = db.Column(db.String)
	num = db.Column(db.Integer)
	owner = db.relationship('User', secondary='user_decks', lazy='subquery')



class UserDecks(db.Model):

	__tabelname__ = 'user_decks'
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
	deck_id = db.Column(db.Integer, db.ForeignKey('decks.deck_id'), primary_key=True, nullable=False)



class Cards(db.Model):

	__tabelname__ = 'cards'
	card_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	card_title = db.Column(db.String, nullable=False)
	card_content = db.Column(db.String, nullable=False)
	deck = db.relationship('Decks', secondary='deck_cards', lazy='subquery')



class DeckCards(db.Model):

	__tabelname__ = 'deck_cards'
	deck_id = db.Column(db.Integer, db.ForeignKey('decks.deck_id'), primary_key=True, nullable=False)
	card_id = db.Column(db.Integer, db.ForeignKey('cards.card_id'), primary_key=True, nullable=False)
