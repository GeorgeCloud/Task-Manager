from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    # completed = db.Column(db.Integer, default=0) useful for keeping an archive of completed tasks; show only uncompleted tasks
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Task: {self.id}'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return '<h1>Database Issue Adding Task</h1>'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    try:
        task_to_delete = Todo.query.get_or_404(id)
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return '<h1>Failed to delete</h1>'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return '<h1>Failed to update</h1>'
    else:
        return render_template('update.html', task=task_to_update)
        # return redirect(f'/update/{id}')

# @app.route('/about-us')
# def about_us():
#     return render_template('about_us.html')

if __name__ == '__main__':
    app.run(debug=True)
