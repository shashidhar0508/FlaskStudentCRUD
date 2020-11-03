from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# 'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'user',
#         'PASSWORD': 'admin@123',
#         'HOST': '192.168.99.100',
#         'PORT': '5432',


app=Flask(__name__)
app.secret_key=("message")

password='admin@123'
postgresurl='postgresql://user:'+password+'@192.168.99.100:5432/postgres'
print("postgresurl : ",postgresurl)
app.config['SQLALCHEMY_DATABASE_URI']=postgresurl
db=SQLAlchemy(app)

class Data(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    eid = db.Column(db.String(100))
    ename=db.Column(db.String(100))
    email=db.Column(db.String(100))
    econtact=db.Column(db.String(100))

    def __init__(self,eid,ename,email,econtact):
        self.eid=eid
        self.ename=ename
        self.email=email
        self.econtact=econtact


@app.route('/')
def index():
    employees_data=Data.query.all()

    return render_template('index.html',employees=employees_data)
    # return "flask app"

@app.route('/insert',methods=['POST'])
def insert():
    if request.method=='POST':
        flash("Record inserted successfully")
        eid =request.form['eid']
        ename =request.form['ename']
        email =request.form['email']
        econtact =request.form['econtact']
        print("employee values : ",eid,ename,email,econtact)

        my_data=Data(eid,ename,email,econtact)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        print("update method my_data : ",my_data)
        my_data.eid = request.form['eid']
        my_data.ename = request.form['ename']
        my_data.email = request.form['email']
        my_data.econtact = request.form['econtact']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('index'))

if(__name__)=="__main__":
    app.run(debug=True)