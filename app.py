# from crypt import methods

from flask import Flask, redirect ,render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    title =  db.Column(db.String(200) , nullable=False)
    desc = db.Column(db.String(500) , nullable=False)
    date_created = db.Column(db.DateTime , default=datetime.utcnow)

    def __repr__ (self)->str:
        return f"{self.sno} - {self.title}"


@app.route('/',methods=['GET' , 'POST'])
def todofunc():
    if(request.method == 'POST'):
        title = request.form['title']
        desc= request.form['desc']
        todo = Todo(title=title , desc = desc)
       
        db.session.add(todo)
        db.session.commit()
    allTodos = Todo.query.all()
    print(allTodos)
    return render_template('index.html' ,allTodo = allTodos )


@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.filter_by(sno = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    if(request.method == 'POST'):
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno = id).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno = id).first()
    return render_template('update.html' , todo = todo)

if __name__ == '__main__':
    app.run(debug=True ,port=8000)
