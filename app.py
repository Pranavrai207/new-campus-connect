import os
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'campus_connect_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complaints.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- FILE UPLOAD CONFIGURATION ---
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- DATABASE MODELS ---

class Student(db.Model):
    enrollment_no = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50))
    branch = db.Column(db.String(50))
    year = db.Column(db.String(20))
    section = db.Column(db.String(10))
    profile_pic = db.Column(db.String(200), default='default.jpg')

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    enrollment_no = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    admin_comment = db.Column(db.Text, default='')
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize Database
with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/')
def login_page():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    role = request.form.get('role')
    username = request.form.get('username') 
    password = request.form.get('password') 

    if role == 'admin':
        if username == 'admin' and password == 'admin123':
            session['user_role'] = 'admin'
            return redirect('/admin')
        else:
            flash("Invalid Admin Credentials")
            return redirect('/')
    
    elif role == 'student':
        session['user_role'] = 'student'
        session['student_id'] = username
        
        # Check if student exists
        student = Student.query.get(username)
        if not student:
            # --- NEW USER DETECTED ---
            new_student = Student(enrollment_no=username, name=password)
            db.session.add(new_student)
            db.session.commit()
            
            # Set a session flag to trigger the popup later
            session['first_login'] = True
            
        return redirect('/student')

    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# --- STUDENT DASHBOARD ---
@app.route('/student', methods=['GET', 'POST'])
def student_dashboard():
    if session.get('user_role') != 'student':
        return redirect('/')

    current_student = Student.query.get(session['student_id'])
    my_complaints = Complaint.query.filter_by(enrollment_no=session['student_id']).order_by(Complaint.date_posted.desc()).all()
    
    success_flag = False
    
    # --- CHECK FOR FIRST TIME LOGIN ---
    show_setup_modal = False
    if session.get('first_login'):
        show_setup_modal = True
        session.pop('first_login', None) # Remove flag so it doesn't happen next refresh

    if request.method == 'POST':
        cat = request.form.get('category')
        desc = request.form.get('description')
        
        new_complaint = Complaint(
            student_name=current_student.name,
            enrollment_no=current_student.enrollment_no,
            department=current_student.department or 'Not Provided',
            branch=current_student.branch or 'Not Provided',
            category=cat,
            description=desc
        )
        db.session.add(new_complaint)
        db.session.commit()
        
        # Refresh complaints list
        my_complaints = Complaint.query.filter_by(enrollment_no=session['student_id']).order_by(Complaint.date_posted.desc()).all()
        success_flag = True

    return render_template('student.html', 
                           student=current_student,
                           complaints=my_complaints,
                           success=success_flag,
                           show_setup_modal=show_setup_modal) # Pass the flag to HTML

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if session.get('user_role') != 'student':
        return redirect('/')
        
    student = Student.query.get(session['student_id'])
    if student:
        student.department = request.form.get('department')
        student.branch = request.form.get('branch')
        student.year = request.form.get('year')
        student.section = request.form.get('section')
        
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{student.enrollment_no}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                student.profile_pic = unique_filename
        
        db.session.commit()
        flash("Profile updated successfully!", "success")
    
    return redirect('/student')

@app.route('/delete_profile_pic', methods=['POST'])
def delete_profile_pic():
    if session.get('user_role') != 'student':
        return redirect('/')
    
    student = Student.query.get(session['student_id'])
    if student:
        student.profile_pic = 'default.jpg'
        db.session.commit()
        flash("Profile picture removed.", "info")
    
    return redirect('/student')

@app.route('/admin')
def admin_panel():
    if session.get('user_role') != 'admin':
        return redirect('/')
    all_complaints = Complaint.query.order_by(Complaint.date_posted.desc()).all()
    p_count = Complaint.query.filter_by(status='Pending').count()
    r_count = Complaint.query.filter_by(status='Resolved').count()
    return render_template('admin.html', complaints=all_complaints, p_count=p_count, r_count=r_count)

@app.route('/resolve/<int:id>', methods=['POST'])
def resolve(id):
    if session.get('user_role') != 'admin':
        return redirect('/')
    complaint = Complaint.query.get_or_404(id)
    complaint.status = 'Resolved'
    complaint.admin_comment = request.form.get('comment')
    db.session.commit()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)