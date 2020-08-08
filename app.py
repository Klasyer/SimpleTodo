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

@app.route('/delete/<int:id>', methods=['POST','GET']) 
def delete(id): 
    task_to_delete = Todo.query.get_or_404(id) 

    try: 
        db.session.delete(task_to_delete) 
        db.session.commit() 
        return redirect('/')
    except: 
        return 'Couldnt delete that task, rip'

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

@app.route('/task', methods=['POST'])
def add_task():
  content = request.json['content']

  new_task = Todo(content)

  db.session.add(new_task)
  db.session.commit()

  return task_schema.jsonify(new_task) 

@app.route('/task/<int:id>', methods=['GET'])
def get_task(id):
    task = Todo.query.get(id)
    if task is 
    try:
        return task_schema.jsonify(task)
    except:
        return task

if __name__ == "__main__": 
    app.run(debug=True)

