from flask_restful import Resource, reqparse

from models.user_util import UserModel

# will get data from POSTMAN and insert into sqlite3 database(users table) for authentication purpose
class UserRegister(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('username',
                       type=str,
                       required=True,
                       help="Username should not be Blank"
                       )
    parse.add_argument('password',
                       type=str,
                       required=True,
                       help="Password should not be Blank"
                       )

# when run POSTMAN POST /register it will call this method through app.pyv
    def post(self):

        data = UserRegister.parse.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"Message": "A user with that username already exists"}, 400

        user = UserModel(**data) #(dta['username'], data['password']) = **data (we are unpacking)
        user.save_to_db()

        return {'Message': 'User Register Successfully /users/post'}, 201
