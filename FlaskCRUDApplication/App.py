from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = ("message")

password = 'admin@123'
postgresurl = 'postgresql://user:' + password + '@192.168.99.100:5432/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = postgresurl
db = SQLAlchemy(app)


class employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empid = db.Column(db.String(100))
    empname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phoneno = db.Column(db.String(100))

    def __init__(self, empid, empname, email, phoneno):
        self.empid = empid
        self.empname = empname
        self.email = email
        self.phoneno = phoneno


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eid = db.Column(db.String(100))
    ename = db.Column(db.String(100))
    email = db.Column(db.String(100))
    econtact = db.Column(db.String(100))

    def __init__(self, eid, ename, email, econtact):
        self.eid = eid
        self.ename = ename
        self.email = email
        self.econtact = econtact


@app.route('/')
def index():
    employees_data = employees.query.all()

    return render_template('index.html', employees=employees_data)
    # return "flask app"


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        flash("Record inserted successfully")
        empid = request.form['eid']
        empname = request.form['ename']
        email = request.form['email']
        phoneno = request.form['econtact']

        my_data = employees(empid, empname, email, phoneno)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = employees.query.get(request.form.get('id'))
        my_data.empid = request.form['eid']
        my_data.empname = request.form['ename']
        my_data.email = request.form['email']
        my_data.phoneno = request.form['econtact']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = employees.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('index'))


if (__name__) == "__main__":
    app.run(debug=True)
