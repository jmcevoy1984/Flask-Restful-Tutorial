from flask import Flask, abort
from database import db
from models import Task
from flask_restful import Api, Resource, reqparse, fields, marshal_with, marshal

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
api = Api(app)

task_fields = {

    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('task')

}

class TaskListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,
            help = 'No task title provided', location = 'json')
        self.reqparse.add_argument('description', type = str, default = "", location = 'json')
        self.reqparse.add_argument('done', type = bool, location = 'json')
        super(TaskListAPI, self).__init__()
    
    
    def get(self):
        all_tasks = Task.query.all()
        output_tasks = []
        for task in all_tasks:
            output_tasks.append(marshal(task, task_fields))
        return { 'tasks' : output_tasks }, 200

    def post(self):
        args = self.reqparse.parse_args()
        task = Task(args['title'], args['description'], args['done'])
        db.session.add(task)
        db.session.commit()
        return { 'result': True }, 201
        
        
class TaskAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True, help = 'No task title provided',
         location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        self.reqparse.add_argument('done', type = bool, location = 'json')
        super(TaskAPI, self).__init__()
        
    @marshal_with(task_fields)
    def get(self, id):
        if not Task.query.get(id):
            abort(404)
        else:
            task = Task.query.get(id)
        return task, 200

    def put(self, id):
        if not Task.query.get(id):
            abort(404)
        else:
            task = Task.query.get(id)
            args = self.reqparse.parse_args()
            print (args)
            for key, value in args.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            db.session.commit()
        return { 'result': True }, 200

    def delete(self, id):
        if not Task.query.get(id):
            abort(404)
        else:
            db.session.delete(id)
            db.session.commit()
        return { 'result' : True }, 200
        
api.add_resource(TaskListAPI, '/todo/api/v1.0/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/todo/api/v1.0/tasks/<int:id>', endpoint='task') 

@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
