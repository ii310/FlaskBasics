from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__, static_folder='static') 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/isilinci/Desktop/projects/FlaskBasics/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Task {self.id}>'

@app.route('/', methods= ['POST','GET']) #Addimg two methods post and get
def index():
    error_message = None
    
    if request.method == 'POST':
        task_content = request.form['content'].strip()
        
        if not task_content:
            error_message = "There is no task written! Please try again"
        else:
            new_task = Todo(content = task_content)
        
            try: 
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except: 
                error_messsage= "Task could not be added due to an issue."
               
    
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', tasks=tasks, error_message=error_message)  # Pass tasks to template
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return' Task can not be deleted due to a issue '
    
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()  # Save changes
            return redirect('/')
        except:
            return 'There was an issue updating the task'
    return render_template('update.html', task=task) 
        
    
    
    
if __name__ == "__main__":
    with app.app_context(): 
        db.create_all()  
    app.run(debug=True)
    
    
    