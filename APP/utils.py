from datetime import datetime
from flask import flash
from APP import db, bcrypt
from APP.models import Student


def add_new_student(
    adm_no_str: int,
    email: str,
    dob_str: str,
    name: str,
    contact: str,
    class_section: str,
):
    # Convert data types
    date_of_birth = datetime.strptime(dob_str, "%Y-%m-%d").date()
    admission_no = int(adm_no_str)
 
    # Generate default password: admission_no@DDMMYYYY
    password = adm_no_str + "@" + date_of_birth.strftime("%d%m%Y")  # 9989@01052008
    default_pw = bcrypt.generate_password_hash(password).decode()

    # Check for duplicates
    email_duplicate = Student.query.filter_by(email=email).first()
    admission_no_duplicate = Student.query.filter_by(admission_no=admission_no).first()

    duplicate_fields = []
    if admission_no_duplicate:
        duplicate_fields.append("Admission number")
    if email_duplicate:
        duplicate_fields.append("Email")

    if duplicate_fields:
        flash("Student details already exist please check: " + " and ".join(duplicate_fields), "danger")
        return None
    

    student = Student(
        admission_no=admission_no,
        email=email,
        password=default_pw,
        name=name,
        contact=contact,
        date_of_birth=date_of_birth,
        class_section=class_section,
    )

    db.session.add(student)
    db.session.commit()

    flash("Student added successfully.", "success")
    return None
