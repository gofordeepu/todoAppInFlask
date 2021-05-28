# importing modules
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
# Defining Schema
class Todo(db.Model):
  sno=db.Column(db.Integer,primary_key=True)
  title=db.Column(db.String(200),nullable=False)
  desc=db.Column(db.String(500),nullable=False)
  date_created=db.Column(db.DateTime,default=datetime.utcnow)
  
  def __repr__(self) -> str:
    return f"{self.sno} - {self.title}"
  # inserting and displaying todo
@app.route('/',methods=['GET','POST'])
def showTodo():
  if request.method=='POST':
    title=request.form['title']
    desc=request.form['desc']
    todo=Todo(title=title,desc=desc)
    db.session.add(todo)
    db.session.commit()
  allTodo=Todo.query.all()
  return render_template('Index.html',allTodo=allTodo)

# deleting todo
@app.route('/delete/<int:sno>')
def deleteTodo(sno):
  todo=Todo.query.filter_by(sno=sno).first()
  db.session.delete(todo)
  db.session.commit()
  allTodo=Todo.query.all()
  return render_template('Index.html',allTodo=allTodo)
#main program
if __name__=="__main__":
  app.run(debug=True,port=3333)
