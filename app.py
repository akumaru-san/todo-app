from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Table(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    text = db.Column(db.String(1000),nullable=False)

    def __repr__(self) -> str:
        return self.name


@app.route('/')
def home():
    tb = Table.query.all()
    print(tb)
    return render_template('home.html',data=tb)

@app.route('/add/',methods=['POST'])
def add():
    
    if request.method=='POST':
        name = request.form['name']
        full = request.form['full']

    table = Table(name=name,text=full)

    try:
        db.session.add(table)
        db.session.commit()
    except:
        return "Something went wrong!"

    return redirect(url_for('home'))

@app.route('/del/<int:id>')
def delete(id):
    task_to_delete = Table.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error while deleting that task'

@app.route('/edit/<int:pk>')
def edit(pk):
    task_to_edit = Table.query.get_or_404(pk)
    
    return render_template('edit.html',data=task_to_edit)

@app.route('/edit/<int:pk>/done',methods=['POST','GET'])
def done(pk):
    task = Table.query.get_or_404(pk)
    if request.method=='POST':

        task.name = request.form['name']
        task.text = request.form['full']

        
    try:
        db.session.commit()
        return redirect('/')
    except:
        return "Something went wrong!"


if __name__=='__main__':
    app.run(debug=True)