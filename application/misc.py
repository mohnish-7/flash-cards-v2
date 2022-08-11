# -------------------------------------------------------------------------------------------------------------------------------------- #

#														Miscallaneous Functions

# -------------------------------------------------------------------------------------------------------------------------------------- #

from application.database import db
from application.models import User,Decks,Cards,UserDecks,DeckCards
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os
from main import cache

basedir = os.path.abspath(os.path.dirname(__file__))
SQLITE_DB_DIR = os.path.join(basedir,'../db_directory')

engine = create_engine('sqlite:///'+os.path.join(SQLITE_DB_DIR,'flashcards.sqlite3'))



# ------------------------------------------------- To Check if User Account exists -----------------------------------------------------#

def user_exists(u_name,pwd):

	with Session(engine, autoflush=False) as session:

		session.begin()

		try:

			c = session.query(User).filter(User.username == u_name).one()
			u_id = c.id

		except:

			c = None

		if c == None:
			return False

		else:
			if c.password == pwd:
				return True
			else:
				return 'wrongpassword'



# --------------------------------------------------- To Check if Decks exists ----------------------------------------------------------#

def deck_exists(u_name,d_name):

	with Session(engine, autoflush=False) as ssn:

			ssn.begin()

			try:

				user = ssn.query(User).filter(User.username == u_name).one()
				deck_list = ssn.query(Decks).filter(Decks.deck_name == d_name).all()

				for d in deck_list:

					try:

						obj = ssn.query(UserDecks).filter(UserDecks.user_id == user.id).filter(UserDecks.deck_id == d.deck_id).one()

						if obj != None:
							return True

					except:
						continue

				return False

			except:

				print('Something went wrong.')

				return False



# ----------------------------------------------------- To Check if Card exists ---------------------------------------------------------#

def card_exists(c_name,d_id):

	with Session(engine, autoflush=False) as session:

			session.begin()

			try:

				card_list = session.query(Cards).filter(Cards.card_title == c_name).all()

				for c in card_list:

					try:

						obj = session.query(DeckCards).filter(DeckCards.deck_id == d_id).filter(DeckCards.card_id == c.card_id).one()

						if obj != None:
							return True

					except:
						continue

				return False


			except:

				print('Something went wrong.')

				return False



# --------------------------------------------------------- To Create a new User --------------------------------------------------------#

def create_new_user(new_username,new_name,new_email,new_password):

	with Session(engine, autoflush=False) as session:

		session.begin()

		try:

			if session.query(User).filter(User.username == new_username).count() > 0:

				return False

			else:

				new_user = User(username=new_username,name=new_name,email=new_email,password=new_password)
				session.add(new_user)

		except:

			print('Something went wrong.')

			return False

		else:

			print('Commit successful.')
			session.commit()

			return True



# -------------------------------------------------------- To create a new Deck ---------------------------------------------------------#

def create_new_deck(new_deck,user_name):

		with Session(engine, autoflush=False) as session:

			session.begin()

			try:

				user = session.query(User).filter(User.username == user_name).one()
				new = Decks(deck_name=new_deck,score=0,last_review='NA',num=0)
				new.owner.append(user)
				session.add(new)

			except:

				print('Something went wrong.')

				return False

			else:

				print('Commit successful.')
				session.commit()
				return True



# ---------------------------------------------------------- To create a new Card -------------------------------------------------------#

def create_new_card(new_card_title,new_card_content,d_id):

	with Session(engine, autoflush=False) as session:

			session.begin()

			try:

				deck_obj = session.query(Decks).filter(Decks.deck_id == d_id).one()
				new = Cards(card_title=new_card_title, card_content=new_card_content)
				new.deck.append(deck_obj)
				session.add(new)

			except:

				print('Something went wrong.')

				return False

			else:

				print('Commit successful.')
				session.commit()
				return True



# --------------------------------------------------------- To delete a Card ------------------------------------------------------------#

def delete_card(c_name,d_id):

	with Session(engine, autoflush=False) as session:

			session.begin()

			try:
				card_list = session.query(Cards).filter(Cards.card_title == c_name).all()

				for c in card_list:

					try:

						del_obj = session.query(DeckCards).filter(DeckCards.deck_id == d_id).filter(DeckCards.card_id == c.card_id).one()
						card_to_del = del_obj

					except:

						continue

					session.delete(del_obj)

				for c in card_list:

					try:
						del_obj = session.query(DeckCards).filter(DeckCards.deck_id == d_id).filter(DeckCards.card_id == c.card_id).one()
						card_to_del = session.query(Cards).filter(Cards.card_id == del_obj.card_id).one()

					except:

						continue

					session.delete(card_to_del)

			except:

				print('Something went wrong.')

				return False

			else:

				print('Commit successful.')
				session.commit()

				return True



# --------------------------------------------------------- To delete a Deck ------------------------------------------------------------#

def delete_deck(d_name,u_name):

	with Session(engine, autoflush=False) as ssn:

			ssn.begin()

			try:

				user = ssn.query(User).filter(User.username == u_name).one()
				deck_list = ssn.query(Decks).filter(Decks.deck_name == d_name).all()

				for d in deck_list:

					try:

						cd_list = ssn.query(DeckCards).filter(DeckCards.deck_id == d.deck_id).all()

						for cd in cd_list:

							card_list = ssn.query(Cards).filter(Cards.card_id == cd.card_id).all()
							ssn.delete(cd)

						for c in card_list:

							delete_card(c.card_title,d.deck_id)

						del_obj = ssn.query(Decks).filter(Decks.deck_id == d.deck_id).filter(Decks.owner.any(id = user.id)).one()

					except:

						continue

					ssn.delete(del_obj)

				for d in deck_list:

					try:

						del_obj = ssn.query(UserDecks).filter(UserDecks.user_id == user.id).filter(UserDecks.deck_id == d.deck_id).one()
						deck_to_del = ssn.query(Decks).filter(Decks.deck_id == del_obj.deck_id).one()
					except:

						continue

					ssn.delete(del_obj)
					ssn.delete(deck_to_del)

			except:

				print('Something went wrong.')

				return False

			else:

				print('Commit successful.')
				ssn.commit()

				return True



# ----------------------------------------------------------- To edit a Deck ------------------------------------------------------------#

def edit_deck(d_name,u_name,new_d_name):

	with Session(engine, autoflush=False) as ssn:

			ssn.begin()

			try:

				user = ssn.query(User).filter(User.username == u_name).one()
				deck_list = ssn.query(Decks).filter(Decks.deck_name == d_name).filter().all()

				for d in deck_list:

					try:

						obj = ssn.query(UserDecks).filter(UserDecks.user_id == user.id).filter(UserDecks.deck_id == d.deck_id).one()

					except:

						continue

					if obj != None:

						edit_obj = ssn.query(Decks).filter(Decks.deck_id == obj.deck_id).one()

					edit_obj.deck_name = new_d_name

			except:

				print('Something went wrong.')

				return False

			else:

				print('Commit successful.')
				ssn.commit()

				return True



# --------------------------------------------------------- To search for a Deck --------------------------------------------------------#
# @cache.memoize(50)
@cache.cached(timeout=60, key_prefix='deck_search')
def search(u_name,d_name):


	with Session(engine, autoflush=False) as ssn:

			ssn.begin()

			try:

				all_decks = []
				user = ssn.query(User).filter(User.username == u_name).one()
				deck_list = ssn.query(Decks).filter(Decks.deck_name == d_name).all()


				for d in deck_list:

					try:

						obj = ssn.query(UserDecks).filter(UserDecks.user_id == user.id).filter(UserDecks.deck_id == d.deck_id).one()

					except:

						continue

					if obj != None:

						dk = ssn.query(Decks).filter(Decks.deck_id == obj.deck_id).one()
						all_decks.append(dk)

				return all_decks


			except:

				print('Something went wrong.')

				return False



# ------------------------------------------------------- To update a Deck score --------------------------------------------------------#

def update_score(d_id,points,n):

	from datetime import datetime
	import pytz

	with Session(engine, autoflush=False) as session:

			session.begin()

			try:

				points = float(points)
				deck = session.query(Decks).filter(Decks.deck_id == d_id).one()

				if n == 1:

					old_score = 0

				else:

					old_score = float(deck.score)

				new_score = (old_score + points)
				deck.score = str(new_score)

				ct = str(datetime.now(pytz.timezone('Asia/Kolkata')))
				ct = ct[:-16]
				deck.last_review = ct[:10]+' ,'+ct[10:]

				deck.num = n

			except:

				print('Something went wrong.')

				return False

			else:

				print('Commit successful.')
				session.commit()

				return True



# ------------------------------------------------- To retrieve all Cards as a list -----------------------------------------------------#

def flash_cards(d_id):

	with Session(engine, autoflush=False) as session:

		session.begin()

		card_list = session.query(Cards).filter(Cards.deck.any(deck_id=d_id)).all()

		return card_list



# ---------------------------------------------------- To get the number of Decks -------------------------------------------------------#

def num_of_decks(u_name):

	with Session(engine, autoflush=False) as session:

		session.begin()

		user = session.query(User).filter(User.username == u_name).one()
		deck_list = session.query(UserDecks).filter(UserDecks.user_id == user.id).all()

		return len(deck_list)


# ---------------------------------------------------- Mailing Functions -------------------------------------------------------#

def mailing_list():
	from datetime import datetime
	with Session(engine, autoflush=False) as session:

		session.begin()
		now = datetime.now()
		today_date = now.strftime("%d/%m/%Y")
		today_date = today_date.split('/')
		today_date = ''.join(today_date)
		mail_list = []
		all_users = session.query(User).all()
		for user in all_users:
			all_decks = Decks.query.filter(Decks.owner.any(username=user.username)).all()
			# print(all_decks)
			for deck in all_decks:
				reviewed = deck.last_review[0:10].split('-')
				reviewed.reverse()
				reviewed = ''.join(reviewed)
				# print(deck.deck_name,reviewed,today_date)
				if reviewed != today_date:
					mail_list.append(user)

		return mail_list

def send_email(to_address, subject, message, content="text", attachment_file=None):
	import smtplib
	import datetime
	from email.mime.text import MIMEText
	from email.mime.multipart import MIMEMultipart
	from email.mime.base import MIMEBase
	from email import encoders

	SMPTP_SERVER_HOST = "localhost"
	SMPTP_SERVER_PORT = 1025
	SENDER_ADDRESS = "mohnishgmail.com"
	SENDER_PASSWORD = ""

	msg = MIMEMultipart()
	msg["From"] = SENDER_ADDRESS
	msg["To"] = to_address
	msg["Subject"] = subject

	if content == "html":
		msg.attach(MIMEText(message, "html"))
	else:
		msg.attach(MIMEText(message, "plain"))

	if attachment_file:
		with open(attachment_file, "rb") as attachment:
			part = MIMEBase("application", "octet-stream")
			part.set_payload(attachment.read())

		encoders.encode_base64(part)

		part.add_header("Content-Disposition", f"attachment; filename= {attachment_file}")
        # Add the attchment to msg
		msg.attach(part)

	s = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    # s.starttls()
	s.login(SENDER_ADDRESS, SENDER_PASSWORD)
	s.send_message(msg)
	s.quit()
	return True


def format_message(template_file, data={}):
	from flask import render_template
	return render_template(template_file,data=data)

def send(data):
    message = format_message("reminder_email.html", data=data)
    # this can be a seaprate task
    send_email(
        to_address=data.email,
        subject="Daily Reminder from FLASHCARDS Web App",
        message=message,
        content="html"
    )

def send_daily_reminder(user_list):

	for user in user_list:
		send(user)


# ---------------------------------------------------- Generating a Report and emailing it-------------------------------------------------------#

def send_report(data,msg=None,atch=None):

    # this can be a seaprate task
    send_email(
        to_address=data.email,
        subject="Summary Report from FLASHCARDS Web APP",
        message=msg,
        content="html",
		attachment_file=atch,
    )

def format_report(template_file, decks, usr_name, n_decks, flag=0):

	from flask import render_template
	print('Inside format_report')
	return render_template(template_file,decks=decks,usr_name=usr_name,n_decks=n_decks,flag=flag)

def create_pdf_report(data, u_name, n_decks, f):
	from flask import render_template, redirect
	from weasyprint import HTML
	import uuid

	message = format_report("report.html", decks=data, usr_name=u_name, n_decks=n_decks, flag=f)
	html = HTML(string=message)
	file_name =  str(u_name)+"'s_report"+ ".pdf"
	html.write_pdf(target=file_name)
	print('\n'+file_name+' has been saved.\n')
	return message, file_name


def email_report(all_decks, username, n, flag):

	print('Inside Email_Report')
	msg, f_name = create_pdf_report(data=all_decks, u_name=username, n_decks=n, f=flag)
	user = db.session.query(User).filter(User.username == username).one()
	send_report(user,msg,f_name)



# ------------------------------------------------------------- X____X____X -------------------------------------------------------------#
