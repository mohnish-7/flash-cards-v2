# -------------------------------------------------------------------------------------------------------------------------------------- #
#															Controllers
# -------------------------------------------------------------------------------------------------------------------------------------- #

from flask import current_app as app
from flask import render_template, request, redirect
from application.models import User,Decks,Cards
from random import shuffle
from application.misc import *
from flask_security import login_required
from flask_login import current_user
from flask_login import LoginManager
from application import tasks
from main import cache


# -------------------------------------------------- Initializing Global Variables ----------------------------------------------------- #

u_name = None
current_deck_id = None
n = 0
card_no = 0

# print('\n\n','Page refreshed.........','\n\n')

# --------------------------------------------------------------- Login ---------------------------------------------------------------- #

# ------------------------------------------------------------- Registration ----------------------------------------------------------- #

@app.route('/register',methods=['GET','POST'])
def register():
	try:
		return render_template('register.html')
	except:
		 return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')



# --------------------------------------------------------------- Dashboard ------------------------------------------------------------ #

@app.route('/',methods=['GET','POST'])
@login_required
def dashboard():

	global u_name,n,card_no
	n = 0
	card_no = 0
	u_name = current_user.username
	usr = User.query.filter(User.username == u_name).one()
	grps = Decks.query.filter(Decks.owner.any(username=u_name))
	n_decks = num_of_decks(u_name)

	if n_decks == 0:

		return render_template('dashboard.html',decks=grps,usr_name=usr.username,n_decks=n_decks,flag=1)

	else:

		return render_template('dashboard.html',decks=grps,usr_name=usr.username)




# ------------------------------------------------------ Searching for a Deck ---------------------------------------------------------- #

@app.route('/deck_search',methods=['GET','POST'])
@login_required
def deck_search():

	try:

		global u_name

		if request.method == 'GET':

			if u_name == None:
				return render_template('logout.html')

			return render_template('deck_search.html',u_name=u_name)

	except:
		raise

		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')


# ------------------------------------------------------ Creating a New Deck ----------------------------------------------------------- #

@app.route('/new_deck',methods=['GET','POST'])
@login_required
def new_deck():

	try:

		global u_name

		if request.method == 'GET':

			if u_name == None:
				return render_template('logout.html')

			return render_template('new_deck.html',u_name=u_name)

	except:

		 return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')



# ------------------------------------------------------- Displaying a Card ------------------------------------------------------------ #

@app.route('/cards/<d_id>',methods=['GET','POST'])
@login_required
def cards(d_id):

	try:

		global current_deck_id,card_no
		current_deck_id = d_id

		if u_name == None:
			return render_template('logout.html')

		d = Decks.query.filter(Decks.deck_id == d_id).one()
		flashcards = flash_cards(d_id)
		#shuffle(flashcards)
		num_of_cards = len(flashcards)

		if card_no == num_of_cards and num_of_cards != 0:

			return redirect('/results')

		elif num_of_cards == 0:

			return render_template('cards.html',card=None,dn=d.deck_name,n_cards=num_of_cards,flag=1)

		else:

			return render_template('cards.html', card=flashcards[card_no], dn=d.deck_name, d_id=d.deck_id,flag=0)


	except:
		raise
		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')



# ------------------------------------------------------ Displaying all Card ----------------------------------------------------------- #

@app.route('/all_cards/<d_id>',methods=['GET','POST'])
@login_required
def all_cards(d_id):

	try:

		global current_deck_id
		current_deck_id = d_id

		if u_name == None:
			return render_template('logout.html')

		d = Decks.query.filter(Decks.deck_id == d_id).one()
		cards = flash_cards(d_id)
		num_of_cards = len(cards)
		flashcards = Cards.query.filter(Cards.deck.any(deck_id=d_id))

		return render_template('all_cards.html', cards=flashcards, dn=d.deck_name,n_cards=num_of_cards)

	except:
		raise
		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')



# -------------------------------------------------------- Creating a new Card --------------------------------------------------------- #

@app.route('/new_card',methods=['GET','POST'])
@login_required
def new_card():

	try:

		global current_deck_id

		if request.method == 'GET':

			if u_name == None:
					return render_template('logout.html')

			return render_template('new_card.html',u_name=u_name,d_id=current_deck_id)

	except:

		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')



# ------------------------------------------------------ Deleting a Card --------------------------------------------------------------- #

@app.route('/delete_card',methods=['GET','POST'])
@login_required
def del_card():

	try:

		global current_deck_id

		if request.method == 'GET':

			if u_name == None:
				return render_template('logout.html')

			return render_template('delete_card.html',deck_id=current_deck_id)

	except:

		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')



# ---------------------------------------------------------- Deleting a Deck ----------------------------------------------------------- #

@app.route('/delete_deck',methods=['GET','POST'])
@login_required
def del_deck():

	try:

		global u_name

		if request.method == 'GET':

			if u_name == None:

				return render_template('logout.html')

			return render_template('delete_deck.html',u_name=u_name)

	except:

		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')



# ---------------------------------------------------------- Editing a Deck ------------------------------------------------------------ #

@app.route('/change_deck_name',methods=['GET','POST'])
@login_required
def change_deck_name():

	try:

		global u_name

		if request.method == 'GET':

			if u_name == None:
				return render_template('logout.html')

			return render_template('edit_deck.html')


	except:
		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')

# ---------------------------------------------------------- Editing a Card ------------------------------------------------------------ #

@app.route('/change_card_content',methods=['GET','POST'])
@login_required
def change_card_name():

	try:

		global current_deck_id

		if request.method == 'GET':

			if u_name == None:
				return render_template('logout.html')

			return render_template('edit_card.html',d_id=current_deck_id)


	except:
		raise
		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')


# -------------------------------------------------------- Score Calculation ----------------------------------------------------------- #

@app.route('/score/<p>',methods=['GET','POST'])
@login_required
def score_calc(p):

	try:

		global n,current_deck_id,card_no

		if request.method == 'GET':

			if u_name == None:
				return render_template('logout.html')

		else:
			n += 1
			card_no += 1
			status = update_score(current_deck_id,p,n)

			if status:

				return redirect('/cards/'+str(current_deck_id))

	except:

		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')



# ---------------------------------------------------------- Displaying Results -------------------------------------------------------- #

@app.route('/results',methods=['GET','POST'])
@login_required
def results():

	try:

		global current_deck_id
		d_id = current_deck_id
		d = Decks.query.filter(Decks.deck_id == d_id).one()

		return render_template('results.html',score=d.score)

	except:

		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')

# ---------------------------------------------------------- Displaying Results -------------------------------------------------------- #

@app.route('/report',methods=['GET','POST'])
@login_required
def generate_report():

	try:
		global u_name,n,card_no
		n = 0
		card_no = 0
		u_name = current_user.username
		usr = User.query.filter(User.username == u_name).one()
		grps = Decks.query.filter(Decks.owner.any(username=u_name)).all()
		print('\n',grps,'\n')
		n_decks = num_of_decks(u_name)

		if n_decks == 0:
			print('Inside Controllers')
			tasks.generate_report.delay(usr_name=usr.username,n_decks=n_decks,flag=1)
			#return render_template('report.html',decks=grps,usr_name=usr.username,n_decks=n_decks,flag=1)

		else:
			print('Inside Controllers')
			tasks.generate_report.delay(usr_name=usr.username,n_decks=n_decks,flag=0)
			#return render_template('report.html',decks=grps,usr_name=usr.username)
			return render_template('success.html')

	except:
		return render_template('failure.html')

# ------------------------------------------------------------ X_____x_____X ----------------------------------------------------------- #

# @app.route('/test',methods=['GET','POST'])
# def test():
# 	job = tasks.daily_reminder.delay()
# 	return str(job),200

@app.route('/test',methods=['GET','POST'])
def test():
	global u_name,n,card_no
	n = 0
	card_no = 0
	u_name = current_user.username
	usr = User.query.filter(User.username == u_name).one()
	grps = Decks.query.filter(Decks.owner.any(username=u_name)).all()
	print('\n',grps,'\n')
	n_decks = num_of_decks(u_name)

	if n_decks == 0:
		return render_template('report.html',decks=grps,usr_name=usr.username,n_decks=n_decks,flag=1)

	else:
		return render_template('report.html',decks=grps,usr_name=usr.username)
