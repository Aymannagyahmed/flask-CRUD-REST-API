# Import Flask app
from flask import Flask, jsonify, redirect, flash, request
# Import Restfull needs
from flask_restful import Api, Resource, abort
# Configure Log Module
import logging
# Import DB handler, Todo Class
from models import db, Todo
logging.basicConfig(filename='./flask.logs', level=logging.DEBUG,
                    format=" %(asctime)s %(message)s %(levelname)s")
# Configure Flask app
todo_flask_app = Flask(__name__)
# Configure Restful APi
todo_api = Api(todo_flask_app)
# Configure Secret Key
todo_flask_app.config['SECRET_KEY'] = '0zx5c34as65d4654&%^#$#$@'

# Configure Database
todo_flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
todo_flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
@todo_flask_app.route('/test',methods=['GET'])
# --------------------------
# Restful
# --------------------------

class TodoRUD(Resource):
    def get(self, **kwargs):
        # Get TOdo id from request
        todo_id = kwargs.get('todo_id')
        # Get Todo object

        task = Todo.query.get(todo_id)
        if not task:
            abort(404, message='Not Found')
        data = {
            'id': task.id,
            'name': task.name,
            'priority': task.priority,
            'description': task.description,
            'finished': task.finished
        }

        return data, 200
    def delete(self, *args, **kwargs):
        # Get Todo id from request
        todo_id = kwargs.get('todo_id')
        # Get Todo object
        todo_obj = Todo.query.get(todo_id)
        db.session.delete(todo_obj)  # delete query
        db.session.commit()
        return {'message': 'Deleted Successfully'}, 200

    def patch(self, **kwargs):
        # Get Todo id from request
        todo_id = kwargs.get('todo_id')
        # Get Todo object
        todo_obj = Todo.query.get(todo_id)
        db.session.add(todo_obj)  # insert query inside the db
        db.session.commit()
        return {'message': 'Todo Updated Successfully'}, 200
    
class TodoLC(Resource):
    def post(self):
        try:
            data = {
                'name': request.form.get('name'),
                'priority': request.form.get('priority'),
                'description': request.form.get('description'),
                'finished': False
            }

            todo_obj = Todo(**data)  # create object of Todo
            db.session.add(todo_obj)  # insert query inside the db
            db.session.commit()  # commit to db

            return {'message': 'Task Created Successfully'}, 201
        except Exception as e:
            abort(500, message='Internal Server Error')

    def get(self):
        try:
            todo_objects = Todo.query.filter().all()

            limit = request.args.get('limit')
            my_new_list = []

            for task in todo_objects:
                data = {
                    'id': task.id,
                    'name': task.name,
                    'priority': task.priority,
                    'description': task.description,
                    'finished': task.finished
                }
                my_new_list.append(data)
            if limit:
                my_new_list = my_new_list[:int(limit)]

            return my_new_list

        except Exception as e:
            abort(500, message="Internal Server Error {}".format(e))

# Register The TodoLC Resource class
todo_api.add_resource(TodoLC, '/api/v1/todo')
# Register TodoRud Resource class
todo_api.add_resource(TodoRUD, '/api/v1/todo/<int:todo_id>')
# Attach Sqlalchemy to app
db.init_app(todo_flask_app)
# Create Database Tables
@todo_flask_app.before_first_request
def initiate_data_base_tables():
    db.create_all()
# Run Server
todo_flask_app.run(port=5080, debug=True)
