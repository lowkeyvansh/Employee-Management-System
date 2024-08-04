from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    position = db.Column(db.String(150), nullable=False)
    salary = db.Column(db.Float, nullable=False)

class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=150)])
    position = StringField('Position', validators=[DataRequired(), Length(min=2, max=150)])
    salary = DecimalField('Salary', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')

db.create_all()

@app.route('/')
def home():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        new_employee = Employee(name=form.name.data, position=form.position.data, salary=form.salary.data)
        db.session.add(new_employee)
        db.session.commit()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_employee.html', form=form)

@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    if form.validate_on_submit():
        employee.name = form.name.data
        employee.position = form.position.data
        employee.salary = form.salary.data
        db.session.commit()
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('edit_employee.html', form=form, employee=employee)

@app.route('/delete_employee/<int:id>', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
