from flask import Flask ,render_template, url_for, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from datetime import datetime 
import os

app = Flask(__name__) 
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' 
db = SQLAlchemy(app) 
ma = Marshmallow(app)

#Classs for the todo list 
class Todo(db.Model): 
    id = db.Column(db.Integer, primary_key =True) 
    content = db.Column(db.String(200),nullable=False) 
    date_created = db.Column(db.DateTime, default=datetime.utcnow) 

    def __init__(self, content): 
        self.content = content

    def __repr__(self): 
        return '<Task %r>' % self.id

class TaskSchema(ma.Schema):
  class Meta:
    fields = ('id', 'content', 'date_created')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

#Adding a task through the form 
@app.route('/',methods=['POST','GET']) 
def index(): 
    if request.method == 'POST': 
        task_content = request.form['content1'] 
        new_task = Todo(content=task_content) 

        try: 
            db.session.add(new_task) 
            db.session.commit()
            return redirect('/')
        except: 
            return 'Fuck, Adding task didnt work' 

    else : 
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks = tasks)  

#Deleting a task though the form 
@app.route('/delete/<int:id>', methods=['POST','GET']) 
def delete(id): 
    task_to_delete = Todo.query.get_or_404(id) 

    try: 
        db.session.delete(task_to_delete) 
        db.session.commit() 
        return redirect('/')
    except: 
        return 'Couldnt delete that task, rip'

#Updating a task through the form 
@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id): 
    task = Todo.query.get_or_404(id) 

    if request.method == 'POST': 
        task.content = request.form['content1']  

        try: 
            db.session.commit() 
            return redirect('/') 
        except:
            'oops task didnt update' 
    else: 
        return render_template('update.html',task=task)

#Post request for adding a task
@app.route('/task', methods=['POST'])
def add_task():
    content = request.json['content']
    new_task = Todo(content)
    try:
        db.session.add(new_task)
        db.session.commit()
        return task_schema.jsonify(new_task) 
    except: 
        return new_task

#Get request for one task 
@app.route('/task/<int:id>', methods=['GET'])
def get_task(id):
    task = Todo.query.get(id)
    try:
        return task_schema.jsonify(task)
    except:
        return task

#Get request for all tasks 
@app.route('/task', methods=['GET'])
def get_products():
    all_tasks = Todo.query.all()
    result = tasks_schema.dump(all_tasks)
    try: 
        return tasks_schema.jsonify(result)
    except: 
        return 'Unforunate, but there was a problem with getting all the data, most unfortunate...'

#Delete request for deleting a task 
@app.route('/task/<int:id>', methods=['DELETE'])
def delete_task(id):
    task_to_delete = Todo.query.get(id)
    try: 
        db.session.delete(task_to_delete)
        db.session.commit()
        return task_schema.jsonify(task_to_delete) 
    except: 
        return 'Deleting failed QQ'

#Put request for updating a task 
@app.route('/task/<int:id>', methods=['PUT'])
def update_task(id):
    task_to_update = Todo.query.get(id)
    content = request.json['content']

    task_to_update.content = content
    try: 
        db.session.commit()
        return task_schema.jsonify(task_to_update) 
    except: 
        return task_to_update 

if __name__ == "__main__": 
    app.run(debug=True)

