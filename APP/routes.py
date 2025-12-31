from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user,login_required,current_user, logout_user
from APP import app,db,bcrypt
from APP.models import Admin, Student
from APP.utils import add_new_student

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    role = request.args.get('role')

    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('student'))
    
    
    if role in ('admin','student'):
        if  request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            remember = True if request.form.get('remember') else False

            if role == 'admin':
                admin = Admin.query.filter_by(email=email).first()
                if admin and bcrypt.check_password_hash(admin.password, password):
                    login_user(admin, remember=remember)
                    flash('Login successful!', 'success')
                    return redirect(url_for('admin'))
                else:
                    flash('Invalid email or password.', 'danger')
            
            if role == 'student':
                student = Student.query.filter_by(email=email).first()
                if student and bcrypt.check_password_hash(student.password, password):
                    login_user(student, remember=remember)
                    flash('Login successful!', 'success')
                    return redirect(url_for('student'))
                else:
                    flash('Invalid email or password.', 'danger')

    else:
        return redirect(url_for('start'))

    return render_template('login_trial.html', role=role)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('start'))

@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        return redirect(url_for('student'))
    return render_template('admin_base.html')


@app.route('/admin/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    if current_user.role != 'admin':
        return redirect(url_for('student'))
    Class = request.form.get('class','12')
    Section= request.form.get('section','A')
    if request.method == 'POST':
        email = request.form.get('email')
        name= request.form.get('name')
        contact = request.form.get('contact')
        dob_str = request.form.get('date_of_birth')
        adm_no_str = request.form.get('admission_no')
        class_section=Class+'-'+Section
        
        add_new_student(adm_no_str,email,dob_str,name,contact,class_section)
            
        
    return render_template('admin_add_student.html',Class=Class,Section=Section)

@app.route('/student')
@login_required
def student():
    if current_user.role != 'student':
        return redirect(url_for('admin'))
    return "<h1>Student Page</h1>"