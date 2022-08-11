from flask_restful import Resource
from flask_restful import fields, marshal_with
from application.database import db
from application.models import User, Decks
from application.validation import NotFoundError, BusinessValidationError
from flask_restful import reqparse

user_fields = {
    "id" : fields.Integer,
    "username" : fields.String,
    "name" : fields.String,
    "email" : fields.String
}

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username')
create_user_parser.add_argument('name')
create_user_parser.add_argument('email')

update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument('name')

class UserAPI(Resource):


    @marshal_with(user_fields)
    def get(self, username):
        print('\nIn UserAPI GET Method\n')

        # querying the database
        user = db.session.query(User).filter(User.username == username).first()

        if user:
            #return valid user json
            return user
        else:
            # return 404 error
            raise NotFoundError(404)


    @marshal_with(user_fields)
    def put(self,username):

        print('\nIn UserAPI PUT Method\n')
        new_name = update_user_parser.parse_args().get("name", None)
        user = db.session.query(User).filter(User.username == username).first()

        if user:
            user.name = new_name
            db.session.add(user)
            db.session.commit()
            return user, 200

        else:
            # return 404 error
            raise NotFoundError(404)


    def delete(self, username):

        print('\nIn UserAPI DELETE Method\n')
        user = db.session.query(User).filter(User.username == username).first()

        if user:
            if Decks.query.filter(Decks.owner.any(username=username)).first():
                raise BusinessValidationError(status_code=400, error_code='BE105', error_msg='author still has decks')
            else:
                db.session.delete(user)
                db.session.commit()

        else:
            # return 404 error
            raise NotFoundError(404)



    @marshal_with(user_fields)
    def post(self):

        print('\nIn UserAPI POST Method\n')
        args = create_user_parser.parse_args()
        username = args.get("username", None)
        name = args.get("name", None)
        email = args.get("email", None)

        if username is None:
            raise BusinessValidationError(status_code=400, error_code="BE101", error_msg="username is required")

        if email is None:
            raise BusinessValidationError(status_code=400, error_code="BE102", error_msg="email is required")

        if "@" not in email:
            raise BusinessValidationError(status_code=400, error_code="BE103", error_msg="invalid email")

        if name is None:
            raise BusinessValidationError(status_code=400, error_code="BE101", error_msg="name is required")

        if db.session.query(User).filter(User.username == username).first():
            raise BusinessValidationError(status_code=400, error_code="BE104", error_msg="user already exists")

        new_user = User(username=username, email=email, name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201
