from flask import jsonify, Blueprint

from flask.ext.restful import Resource, Api , reqparse, inputs

import models


class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required=True,
            help='No todo title provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'url',
            required=True,
            help='No todo URL provided',
            location=['form', 'json'],
            type=inputs.url # check the input type
        )
        super().__init__()

    def get(self):
        todos = [marshal((todo), todo_fields)
                   for todo in models.Todo.select()]
        return jsonify({'todos': [{'title': 'Python Basics'}]})


    def post(self):
        args = self.reqparse.parse_args()
        course = models.Todo.create(**args)  # save the date to the database
        return jsonify({'Todos': [{'title': 'Python Basics'}]})


class Todo(Resource):
    def get(self, id):
        return jsonify({'title': 'Python Basics'})

    def put(self, id):
        return jsonify({'title': 'Python Basics'})

    def delete(self, id):
        return jsonify({'title': 'Python Basics'})

todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)
api.add_resource(
    TodoList,
    '/api/v1/todos',
    endpoint='todos'
)
api.add_resource(
    Todo,
    '/api/v1/todos/<int:id>',
    endpoint='todo'
)
