from flask import Flask,session,g,render_template, request, redirect, url_for, flash
import os
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
from datetime import datetime
import sqlalchemy
from sqlalchemy import text,desc
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from inflection import camelize
import sys

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db =SQLAlchemy(app)

app.secret_key=os.urandom(24)

class Car(db.Model):
    car_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    sales = db.relationship('Sales', backref='car', lazy=True)

    def __repr__(self) -> str:
        return '<Car %r>' % self.car_id

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    sales = db.relationship('Sales', backref='customer', lazy=True)
    def __repr__(self) -> str:
        return '<Customer %r>' % self.customer_id

class Showroom(db.Model):
    showroom_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.manager_id'), nullable=False)
    sales = db.relationship('Sales', backref='showroom', lazy=True)
    def __repr__(self) -> str: 
        return '<Showroom %r>' % self.showroom_id

class Manager(db.Model):
    manager_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password=db.Column(db.String(80), nullable=False)
    showroom = db.relationship('Showroom', backref='manager', lazy=True)
    salary = db.Column(db.Integer, nullable=False)
    def __repr__(self) -> str: 
        return '<Manager %r>' % self.manager_id

class Sales(db.Model):
    sales_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.car_id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    showroom_id = db.Column(db.Integer, db.ForeignKey('showroom.showroom_id'), nullable=False)
    date = db.Column(db.DateTime(80), default=datetime.utcnow)
    amount = db.Column(db.Integer, nullable=False)
    def __repr__(self) -> str:
        return '<Sales %r>' % self.sales_id

with app.app_context():
    db.create_all()
    print("Created all tables successfully")

@app.before_request
def before_request():
    g.username = None
    if 'username' in session:
        g.username = session['username']

@app.route("/dropsession", methods=["GET", "POST"])
def dropsession():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['username'] == 'admin': 
            session.pop('username', None)
            if request.form['password'] == 'password':
                session['username'] = request.form['username']
                return redirect(url_for('home'))
    return render_template('index.html')

@app.route("/home", methods=['GET', 'POST'])
def home():
    if g.username:
        if request.method == 'POST':
            form_type = request.form['form_type']
            if form_type == 'view_database':
                return redirect(url_for('viewdb_fun'))
            elif form_type == 'info':
                return redirect(url_for('info'))
            elif form_type == 'sell':
                return redirect(url_for('sell'))
            elif form_type == 'Queries':
                return redirect(url_for('home'))
            else:
                # Handle unexpected form type
                pass
        else:
            return render_template('home.html',username=session['username'])
    else:
        return redirect(url_for('index'))

@app.route("/home/viewdb", methods=['GET', 'POST'])
def viewdb_fun():
    if g.username:
        tablename = ""
        if request.method == 'POST':
            tablename = request.form['tablename']
            return redirect(url_for('viewdb_fun_table', tablename=tablename, username=session['username']))
        return render_template('viewdb.html', tablename=tablename,username=session['username'])
    return redirect(url_for('index'))

@app.route("/home/viewdb/<tablename>", methods=['GET'])
def viewdb_fun_table(tablename):
    if g.username:
        table = db.engine.execute(f'SELECT * FROM {tablename}')
        return render_template('viewdb.html', tablename=table,username=session['username'],displayname=tablename)
    return redirect(url_for('index'))

@app.route("/home/<tablename>/create", methods=['GET', 'POST'])
def create_record(tablename):
    if g.username:
        table_class = getattr(sys.modules[__name__], tablename.capitalize())
        if request.method == 'POST':
            data = request.form.to_dict()
            new_record = table_class(**data) 
            db.session.add(new_record)
            db.session.commit()
            return redirect(url_for('viewdb_fun_table', tablename=tablename, username=session['username']))
        columns = table_class.__table__.columns.keys()
        return render_template('create_record.html', tablename=tablename, columns=columns,username=session['username'])
    return redirect(url_for('index'))

@app.route("/home/<tablename>/update/<int:id>", methods=['GET', 'POST'])
def update_record(tablename, id):
    if g.username:
        tablename=tablename.capitalize()
        model,record,columns = get_model(tablename, id)
        print("MODEL: ", model)
        print("RECORD: ", record)
        print("COLUMNS: ", columns)
        if request.method == 'POST':
            if request.form.get('form_type') == 'update':
                return render_template('update_record.html', tablename=tablename, record=record,id=id, columns=columns, username=session['username'])
            elif request.form.get('_method')=='PUT':
                data = request.form.to_dict()
                for key, value in data.items():
                    setattr(record, key, value)
                db.session.commit()
                return redirect(url_for('viewdb_fun_table', tablename=tablename, username=session['username']))
    return redirect(url_for('index'))
def get_model(tablename,id):
    if(tablename=='Car'):
        model=Car
        record = Car.query.filter_by(car_id=id).first()
        columns = Car.__table__.columns.keys()
        return model, record , columns
    elif(tablename=='Customer'):
        model=Customer
        record = Customer.query.filter_by(customer_id=id).first()
        columns = Customer.__table__.columns.keys()
        return model, record , columns
    elif(tablename=='Showroom'):
        model=Showroom
        record = Showroom.query.filter_by(showroom_id=id).first()
        columns = Showroom.__table__.columns.keys()
        return model, record , columns
    elif(tablename=='Sales'):
        model=Sales
        record = Sales.query.filter_by(sales_id=id).first()
        columns = Sales.__table__.columns.keys()
        return model, record , columns
    elif(tablename=='Manager'):
        model=Manager
        record = Manager.query.filter_by(manager_id=id).first()
        columns = Manager.__table__.columns.keys()
        return model, record , columns

@app.route("/home/<tablename>/delete/<int:id>", methods=['GET', 'POST','DELETE'])
def delete_record(tablename,id):
    if g.username:
        id = request.form.get('id')
        print("*****************************************")
        # print(**tablename)
        print(tablename,type(tablename))
        table_class = getattr(sys.modules[__name__], tablename.capitalize())
        record = table_class.query.get(id)
        db.session.delete(record)
        db.session.commit()
        return redirect(url_for('viewdb_fun_table', tablename=tablename, username=session['username']))
    return redirect(url_for('index'))

@app.route("/home/query1", methods=['GET', 'POST'])
def query1():
    if g.username:
        if request.method == 'POST':
            top_3_expensive_car_models = Car.query.order_by(desc(Car.price)).limit(3)
            # return render_template("most_expensive_models.html", models=models)
            return render_template('query1.html',most_expensive_cars=top_3_expensive_car_models)
        return render_template('home.html')
    return redirect(url_for('index'))

@app.route("/home/query2", methods=['GET', 'POST'])
def query2():
    if g.username:
        if request.method == 'POST':
            top_3_least_car_models = Car.query.order_by(Car.price).limit(3)
            # return render_template("most_expensive_models.html", models=models)
            return render_template('query2.html',least_expensive_cars=top_3_least_car_models)
        return render_template('home.html')
    return redirect(url_for('index'))

@app.route("/home/query3", methods=['GET', 'POST'])
def query3():
    if request.method == 'POST':
        salary_threshold = request.form.get('salary_threshold')
        managers = Manager.query.filter(Manager.salary > salary_threshold).all()
        return render_template('query3.html', managers=managers)
    return render_template('home.html')


@app.route("/home/query4", methods=['GET', 'POST'])
def query4():
    if g.username:
        if request.method == 'POST':
            salary_threshold = request.form.get('salary_threshold')
            managers = Manager.query.filter(Manager.salary < salary_threshold).all()
            return render_template('query4.html', managers=managers)
        return render_template('home.html')
    return redirect(url_for('index'))

@app.route("/home/query5", methods=['GET', 'POST'])
def query5():
    if g.username:
        if request.method == 'POST':
            sorted_customers = db.session.query(Sales.customer_id, Customer.name, db.func.count(Sales.sales_id).label('frequency')).join(Customer, Sales.customer_id == Customer.customer_id).group_by(Sales.customer_id, Customer.name).order_by(db.func.count(Sales.sales_id).desc())
            return render_template('query5.html', customers=sorted_customers)
        return render_template('home.html')
    return redirect(url_for('index'))

@app.route("/home/query6", methods=['GET', 'POST'])
def query6():
    if g.username:
        if request.method == 'POST':
            # highest_selling_car = db.session.query(Car.model, func.count(Sales.sales_id).label('frequency')).join(Sales, Car.car_id == Sales.car_id).group_by(Car.model).order_by(func.count(Sales.sales_id).desc())
            highest_selling_car = db.session.query(Car.car_id, Car.model, func.count(Sales.sales_id).label('frequency')).join(Sales, Car.car_id == Sales.car_id).group_by(Car.model).order_by(func.count(Sales.sales_id).desc()) 

            return render_template('query6.html', cars=highest_selling_car)
        return render_template('home.html')
    return redirect(url_for('index'))

@app.route("/home/query7", methods=['GET', 'POST'])
def query7():
    if g.username:
        if request.method == 'POST':
            sorted_customers = db.session.query(Sales.customer_id, Customer.name, db.func.count(Sales.sales_id).label('frequency')).join(Customer, Sales.customer_id == Customer.customer_id).group_by(Sales.customer_id, Customer.name).order_by(db.func.count(Sales.sales_id).desc())
            return render_template('query7.html', customers=sorted_customers)
        return render_template('home.html')
    return redirect(url_for('index'))

@app.route("/home/info", methods=['GET', 'POST'])
def info():
    if g.username:
        return render_template('info.html',username=session['username'])
    return redirect(url_for('index'))

@app.route("/home/sell", methods=['GET', 'POST'])
def sell():
    if g.username:
        if request.method=='POST':
            car_id = request.form['car_id']
            customer_id = request.form['customer_id']
            showroom_id = request.form['showroom_id']
            date=datetime.now()
            print("Success")
            print("******************")
            record=Car.query.filter_by(car_id=car_id).first()
            record.quantity=record.quantity-1
            amount=record.price
            db.session.commit()
            print(car_id,customer_id,showroom_id,date,amount)
            db.session.add(Sales(car_id=car_id,customer_id=customer_id,showroom_id=showroom_id,date=date,amount=amount))
            db.session.commit()
            return redirect(url_for('viewdb_fun_table', tablename='sales', username=session['username']))
        return render_template('sell.html',username=session['username'])
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)