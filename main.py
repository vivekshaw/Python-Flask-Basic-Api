from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# initliazing our flask app, SQLAlchemy and Marshmallow
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1:3306/dmart'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


# this is our database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_no = db.Column(db.String(100))
    password = db.Column(db.String(200))

    def __init__(self, phone_no, password):
        self.phone_no = phone_no
        self.password = password



class UserSchema(ma.Schema):
    class Meta:
        fields = ("phone_no", "password")


post_schema = UserSchema()
posts_schema = UserSchema(many=True)


# adding a post
@app.route('/login', methods=['POST'])
def add_post():
    phone_no = request.json['phone_no']
    password = request.json['password']

    user = User(phone_no, password)
    db.session.add(user)
    db.session.commit()

    return post_schema.jsonify(user), 201


# getting posts
@app.route('/get', methods=['GET'])
def get_post():
    all_posts = User.query.all()
    result = posts_schema.dump(all_posts)

    return jsonify(result), 200


# getting particular post
@app.route('/user/<id>/', methods=['GET'])
def post_details(id):
    post = User.query.get(id)
    return post_schema.jsonify(post)


# updating post
@app.route('/post_update/<id>/', methods=['PUT'])
def post_update(id):
    post = User.query.get(id)

    title = request.json['title']
    description = request.json['description']
    author = request.json['author']

    post.title = title
    post.description = description
    post.author = author

    db.session.commit()
    return post_schema.jsonify(post)


# deleting post
@app.route('/post_delete/<id>/', methods=['DELETE'])
def post_delete(id):
    post = User.query.get(id)
    db.session.delete(post)
    db.session.commit()

    return post_schema.jsonify(post)


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    res = jsonify(message)
    res.status_code = 404
    return res


if __name__ == "__main__":
    app.run(debug=True)