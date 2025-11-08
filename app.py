from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    roll = db.Column(db.String(50))
    student_class = db.Column(db.String(50))
    email = db.Column(db.String(120))

@app.route('/')
def home():
    students = Student.query.all()
    return render_template('index.html', students=students)

# ✅ Create database tables automatically
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
