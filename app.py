from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure database (SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------- Database Model -------------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll = db.Column(db.String(50), nullable=False)
    student_class = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'

# ------------------- Routes -------------------

# Home page – show all students
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Add new student
@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    roll = request.form['roll']
    student_class = request.form['student_class']
    email = request.form['email']

    new_student = Student(name=name, roll=roll, student_class=student_class, email=email)
    db.session.add(new_student)
    db.session.commit()

    return redirect(url_for('index'))

# Delete student
@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

# Edit student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.roll = request.form['roll']
        student.student_class = request.form['student_class']
        student.email = request.form['email']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', student=student)

# ------------------- Static Pages -------------------

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('services.html')

# ------------------- Run Server -------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # ✅ Auto-create tables if not exist
    app.run(debug=True)
