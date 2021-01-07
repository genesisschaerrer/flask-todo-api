from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS 
from flask_heroku import Heroku
import os


app=Flask(__name__)
CORS(app)
heroku = Heroku(app)
DATABASE_URL = os.eviron.get("DATABASE_URL")

#this lets python know exactly where this file lives.
basedir = os.path.abspath(os.path.dirname(__file__))
#We are creating a new key value pair in the config dictionary(object)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean)

    def __init__(self, title, done):
        self.title = title
        self.done = done

class TodoSchema(ma.Schema):
    class Meta: 
        fields = ("id", "title", "done")

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

#Get 
@app.route("/todos", methods=["GET"])
def get_todo():
    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)

    return jsonify(result)

#Post 
@app.route("/todo", methods=["POST"])
def add_todo():
    title = request.json["title"]
    done = request.json["done"]

    new_todo = Todo(title, done)

    db.session.add(new_todo)
    db.session.commit()

    todo = Todo.query.get(new_todo.id)
    return todo_schema.jsonify(todo)

#Patch
@app.route("/todo/<id>", methods=["PATCH"])
def update_todo(id):
    todo = Todo.query.get(id)

    new_done = request.json["done"]

    todo.done = new_done

    db.session.commit()
    return todo_schema.jsonify(todo)

#Delete
@app.route("/todo/delete/<id>", methods=["DELETE"])
def delete_todo(id):
    record = Todo.query.get(id)

    db.session.delete(record)
    db.session.commit()

    return jsonify({"message": "Deleted Item"})

if __name__ == "__main__":
    app.run(debug=True)

