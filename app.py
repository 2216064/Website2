import os
import logging
import random
import string
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# Initialise Flask app
app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

# Ensure the instance directory and upload folders exist
instance_dir = os.path.join(os.path.dirname(__file__), 'instance')
uploads_dir = os.path.join(app.config['STATIC_FOLDER'], 'uploads')
os.makedirs(instance_dir, exist_ok=True)
os.makedirs(uploads_dir, exist_ok=True)

# Path to the database file
database_path = os.path.join(instance_dir, 'database.db')
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.urandom(24)

# Flask-Mail configuration
app.config["MAIL_SERVER"] = "smtp.example.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "2216064@leedstrinity.ac.uk"
app.config["MAIL_PASSWORD"] = "Livingstone£22"
app.config["MAIL_DEFAULT_SENDER"] = "2216064@leedstrinity.ac.uk"

mail = Mail(app)
db = SQLAlchemy(app)

# Initialise logger
logging.basicConfig(level=logging.INFO)

class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    UserType = db.Column(db.String(50), nullable=False)
    FullName = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    PhoneNumber = db.Column(db.String(20), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    PhotoURL = db.Column(db.String(255), nullable=True)
    CVURL = db.Column(db.String(255), nullable=True)
    KeySkills = db.Column(db.String(255), nullable=True)
    EmployerWebsite = db.Column(db.String(255), nullable=True)

    def __init__(self,
                 UserType,
                 FullName,
                 Email,
                 Password,
                 PhoneNumber,
                 PhotoURL=None,
                 CVURL=None,
                 KeySkills=None,
                 EmployerWebsite=None):
        self.UserType = UserType
        self.FullName = FullName
        self.Email = Email
        self.Password = Password
        self.PhoneNumber = PhoneNumber
        self.PhotoURL = PhotoURL
        self.CVURL = CVURL
        self.KeySkills = KeySkills
        self.EmployerWebsite = EmployerWebsite


class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, email, token):
        self.email = email
        self.token = token


@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Unhandled Exception: {e}", exc_info=True)
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500


# Helper functions
def email_exists(email):
    return User.query.filter_by(Email=email).first() is not None


def generate_token(length=20):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def send_password_reset_email(email, token):
    try:
        reset_link = url_for("reset_password", token=token, _external=True)
        msg = Message(subject="Password Reset", recipients=[email])
        msg.body = f"Click the following link to reset your password: {reset_link}"
        mail.send(msg)
    except Exception as e:
        logging.error(f"Failed to send email to {email}: {e}")


def update_password(email, new_password):
    user = User.query.filter_by(Email=email).first()
    if user:
        user.Password = generate_password_hash(new_password)
        db.session.commit()


@app.route("/index")
def index():
    return render_template("index.html")  # Render the index.html template
    
@app.route("/platform")
def platform():
    return render_template("platform.html")  # Render the platform.html template

@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            email = request.form.get("username", "").strip()
            password = request.form.get("password", "").strip()
            user_type = request.form.get("user_type")

            user = User.query.filter_by(Email=email, UserType=user_type).first()
            if user and check_password_hash(user.Password, password):
                session["user_id"] = user.UserID
                session["user_type"] = user.UserType
                if user.UserType == "Student":
                    return jsonify({
                        "status": "success",
                        "redirect_url": url_for("student_dashboard")
                    })
                elif user.UserType == "Employer":
                    return jsonify({
                        "status": "success",
                        "redirect_url": url_for("employer_dashboard")
                    })
            return jsonify({
                "status": "error",
                "message": "Invalid username or password. Please try again."
            }), 401

        return render_template("login.html")
    except Exception as e:
        logging.error(f"Error in login: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500


@app.route("/logout")
def logout():
    try:
        session.clear()
        return jsonify({"status": "success", "redirect_url": url_for("login")})
    except Exception as e:
        logging.error(f"Error in logout: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500


@app.route("/student_dashboard")
def student_dashboard():
    try:
        if "user_id" in session and session["user_type"] == "Student":
            return render_template("student_dashboard.html")
        else:
            return redirect(url_for("login"))
    except Exception as e:
        logging.error(f"Error in student_dashboard: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500


@app.route("/employer_dashboard")
def employer_dashboard():
    try:
        if "user_id" in session and session["user_type"] == "Employer":
            user = User.query.get(session["user_id"])
            return render_template("employer_dashboard.html", user=user)
        else:
            return jsonify({
                "status": "error",
                "redirect_url": url_for("login")
            }), 401
    except Exception as e:
        logging.error(f"Error in employer_dashboard: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500


@app.route("/register_student", methods=["GET", "POST"])
def register_student():
    logging.info("Register Student Endpoint: START")

    if request.method == "POST":
        name = request.form.get("studentFullName", "").strip()
        email = request.form.get("studentContactEmail", "").strip()
        password = request.form.get("password", "").strip()
        phone_number = request.form.get("studentContactPhone", "").strip()
        key_skills = request.form.get("studentKeySkills", "").strip()
        student_photo = request.files.get("studentPhoto")
        student_cv = request.files.get("studentCv")

        if not name or not email or not password or not phone_number:
            return render_template("registerStudent.html", error="All fields are required.")

        if User.query.filter_by(Email=email).first():
            return render_template("login.html", error="An account already exists with this email. Please login instead.")

        # Handle photo upload
        photo_path = None
        if student_photo and student_photo.filename:  # Ensure filename is not None
            photo_filename = secure_filename(student_photo.filename)
            photo_path = os.path.join(app.config['STATIC_FOLDER'], 'uploads', photo_filename)
            student_photo.save(photo_path)

        # Handle CV upload
        cv_path = None
        if student_cv and student_cv.filename:  # Ensure filename is not None
            cv_filename = secure_filename(student_cv.filename)
            cv_path = os.path.join(app.config['STATIC_FOLDER'], 'uploads', cv_filename)
            student_cv.save(cv_path)

        new_user = User(UserType="Student",
                        FullName=name,
                        Email=email,
                        Password=generate_password_hash(password),
                        PhoneNumber=phone_number,
                        KeySkills=key_skills,
                        PhotoURL=photo_path,
                        CVURL=cv_path)

        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html', message="Registration successful. Please login.")

    return render_template("registerStudent.html")


@app.route("/register_employer", methods=["GET", "POST"])
def register_employer():
    logging.info("Register Employer Endpoint: START")
    if request.method == "POST":
        name = request.form.get("employerCompanyName", "").strip()
        email = request.form.get("employerContactEmail", "").strip()
        password = request.form.get("password", "").strip()
        phone_number = request.form.get("employerContactPhone", "").strip()
        employer_website = request.form.get("employerWebsite", "").strip()
        employer_photo = request.files.get("employerPhoto")
        if not name or not email or not password or not phone_number or not employer_website:
            return render_template("registerEmployer.html", error="All fields are required.")
        if User.query.filter_by(Email=email).first():
            return render_template("login.html", error="An account already exists with this email. Please login instead.")
        # Handle photo upload
        photo_path = None
        if employer_photo and employer_photo.filename:  # Ensure filename is not None
            photo_filename = secure_filename(employer_photo.filename)
            photo_path = os.path.join(app.config['STATIC_FOLDER'], 'uploads', photo_filename)
            employer_photo.save(photo_path)
        new_user = User(UserType="Employer",
                        FullName=name,
                        Email=email,
                        Password=generate_password_hash(password),
                        PhoneNumber=phone_number,
                        EmployerWebsite=employer_website,
                        PhotoURL=photo_path)
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html', message="Registration successful. Please login.")
    return render_template("registerEmployer.html")


@app.route("/api/student_details")
def api_student_details():
    try:
        if "user_id" in session and session["user_type"] == "Student":
            user = User.query.get(session["user_id"])
            if user:
                user_data = {
                    "PhotoURL": user.PhotoURL or "static/images/default-profile.png",
                    "FullName": user.FullName,
                    "Email": user.Email,
                    "PhoneNumber": user.PhoneNumber,
                    "KeySkills": user.KeySkills or "Not provided",
                    "CVURL": user.CVURL or "#"
                }
                return jsonify(user_data)
            return jsonify({
                "status": "error",
                "message": "User not found"
            }), 404
        return jsonify({"status": "error", "message": "Unauthorised"}), 401
    except Exception as e:
        logging.error(f"Error in api_student_details: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

@app.route("/api/employer_details")
def api_employer_details():
    try:
        if "user_id" in session and session["user_type"] == "Employer":
            user = User.query.get(session["user_id"])
            if user:
                user_data = {
                    "PhotoURL": user.PhotoURL or "static/images/default-profile.png",
                    "CompanyName": user.FullName,
                    "ContactEmail": user.Email,
                    "ContactPhone": user.PhoneNumber,
                    "CompanyWebsiteURL": user.EmployerWebsite or "#"
                }
                return jsonify(user_data)
            return jsonify({"status": "error", "message": "User not found"}), 404
        return jsonify({"status": "error", "message": "Unauthorised"}), 401
    except Exception as e:
        logging.error(f"Error in api_employer_details: {e}", exc_info=True)
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    try:
        if request.method == "POST":
            email = request.form.get("email", "").strip()
            if not email_exists(email):
                return jsonify({
                    "status": "error",
                    "message": "Email address not found. Please enter a valid email address."
                }), 404

            session["email"] = email
            token = generate_token()
            new_token = PasswordResetToken(email=email, token=token)
            db.session.add(new_token)
            db.session.commit()
            send_password_reset_email(email, token)
            return jsonify({
                "status": "success",
                "redirect_url": url_for("login")
            })

        return render_template("forgot_password.html")
    except Exception as e:
        logging.error(f"Error in forgot_password: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = session.get("email")
        if not email:
            return jsonify({
                "status": "error",
                "message": "Session expired or invalid request."
            }), 403

        token_entry = PasswordResetToken.query.filter_by(email=email, token=token).first()
        if not token_entry:
            return jsonify({
                "status": "error",
                "message": "Invalid or expired token."
            }), 403

        if datetime.utcnow() > token_entry.timestamp + timedelta(hours=1):
            db.session.delete(token_entry)
            db.session.commit()
            return jsonify({
                "status": "error",
                "message": "Token expired."
            }), 403

        if request.method == "POST":
            new_password = request.form.get("new_password", "").strip()
            if new_password:
                update_password(email, new_password)
                db.session.delete(token_entry)
                db.session.commit()
                return jsonify({
                    "status": "success",
                    "redirect_url": url_for("login")
                })
            return jsonify({
                "status": "error",
                "message": "New password is required."
            }), 400

        return render_template("reset_password.html", token=token)
    except Exception as e:
        logging.error(f"Error in reset_password: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

@app.route("/student_edit", methods=["GET"])
def student_edit():
    if "user_id" in session and session["user_type"] == "Student":
        student = User.query.get(session["user_id"])
        return render_template("student_edit.html", student=student)
    return redirect(url_for("login"))

@app.route("/employer_edit", methods=["GET"])
def employer_edit():
    if "user_id" in session and session["user_type"] == "Employer":
        employer = User.query.get(session["user_id"])
        return render_template("employer_edit.html", employer=employer)
    return redirect(url_for("login"))

@app.route("/update_student_profile", methods=["POST"])
def update_student_profile():
    if "user_id" in session and session["user_type"] == "Student":
        student = User.query.get(session["user_id"])

        if not student:
            return jsonify({"status": "error", "message": "Student not found."}), 404

        student.FullName = request.form.get("studentFullName", "").strip()
        student.Email = request.form.get("studentContactEmail", "").strip()
        student.PhoneNumber = request.form.get("studentContactPhone", "").strip()
        student.KeySkills = request.form.get("studentKeySkills", "").strip()

        # Handle photo upload
        student_photo = request.files.get("studentPhoto")
        if student_photo and student_photo.filename:
            photo_filename = secure_filename(student_photo.filename)
            photo_path = os.path.join(app.config['STATIC_FOLDER'], 'uploads', photo_filename)
            student_photo.save(photo_path)
            student.PhotoURL = photo_path

        db.session.commit()
        return redirect(url_for("student_dashboard"))
    return redirect(url_for("login"))

@app.route("/update_employer_profile", methods=["POST"])
def update_employer_profile():
    if "user_id" in session and session["user_type"] == "Employer":
        employer = User.query.get(session["user_id"])

        if not employer:
            return jsonify({"status": "error", "message": "Employer not found."}), 404

        employer.FullName = request.form.get("employerCompanyName", "").strip()
        employer.Email = request.form.get("employerContactEmail", "").strip()
        employer.PhoneNumber = request.form.get("employerContactPhone", "").strip()
        employer.EmployerWebsite = request.form.get("employerWebsite", "").strip()

        # Handle photo upload
        employer_photo = request.files.get("employerPhoto")
        if employer_photo and employer_photo.filename:
            photo_filename = secure_filename(employer_photo.filename)
            photo_path = os.path.join(app.config['STATIC_FOLDER'], 'uploads', photo_filename)
            employer_photo.save(photo_path)
            employer.PhotoURL = photo_path

        db.session.commit()
        return redirect(url_for("employer_dashboard"))
    return redirect(url_for("login"))

# Define Job model
class Job(db.Model):
    __tablename__ = 'job'  # Ensure correct table name used
    JobID = db.Column(db.Integer, primary_key=True)
    EmployerID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    Title = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Location = db.Column(db.String(255), nullable=False)
    Salary = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, EmployerID, Title, Description, Location, Salary=None):
        self.EmployerID = EmployerID
        self.Title = Title
        self.Description = Description
        self.Location = Location
        self.Salary = Salary


@app.route("/api/jobs", methods=["GET"])
def list_jobs():
    jobs = Job.query.all()
    return jsonify([{
        "JobID": job.JobID,
        "Title": job.Title,
        "Description": job.Description,
        "Location": job.Location,
        "Salary": job.Salary,
        "is_active": job.is_active
    } for job in jobs])


@app.route("/api/employer_jobs", methods=["GET"])
def employer_jobs():
    if "user_id" in session and session["user_type"] == "Employer":
        jobs = Job.query.filter_by(EmployerID=session["user_id"]).all()
        return jsonify([{
            "JobID": job.JobID,
            "Title": job.Title,
            "Description": job.Description,
            "Location": job.Location,
            "Salary": job.Salary,
            "is_active": job.is_active
        } for job in jobs])
    return jsonify({"status": "error", "message": "Unauthorised"}), 401


@app.route("/api/add_job", methods=["POST"])
def add_job():
    if "user_id" in session and session["user_type"] == "Employer":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        location = request.form.get("location", "").strip()
        salary = request.form.get("salary", "").strip()

        if not title or not description or not location:
            return jsonify({"status": "error", "message": "All fields are required."}), 400

        new_job = Job(EmployerID=session["user_id"], Title=title, Description=description, Location=location, Salary=salary)
        db.session.add(new_job)
        db.session.commit()
        return jsonify({"status": "success"}), 201
    return jsonify({"status": "error", "message": "Unauthorised"}), 401


@app.route("/api/close_job/<int:job_id>", methods=["POST"])
def close_job(job_id):
    if "user_id" in session and session["user_type"] == "Employer":
        job = Job.query.get(job_id)
        if job and job.EmployerID == session["user_id"]:
            job.is_active = False
            db.session.commit()
            return jsonify({"status": "success"}), 200
        return jsonify({"status": "error", "message": "Job not found or unauthorised."}), 404
    return jsonify({"status": "error", "message": "Unauthorised"}), 401


@app.route("/api/search_jobs", methods=["GET"])
def search_jobs():
    try:
        title = request.args.get("title", "").strip()
        location = request.args.get("location", "").strip()

        query = Job.query

        # Apply filters conditionally and check for attribute errors
        if title:
            query = query.filter(Job.Title.ilike(f"%{title}%"))
        if location:
            query = query.filter(Job.Location.ilike(f"%{location}%"))

        jobs = query.all()

        job_list = [{
            "JobID": job.JobID,
            "Title": job.Title,
            "Description": job.Description,
            "Location": job.Location,
            "Salary": job.Salary,
            "is_active": job.is_active
        } for job in jobs]

        return jsonify(job_list)
    except AttributeError as e:
        logging.error(f"Attribute error in search_jobs: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Internal server error due to attribute error"
        }), 500
    except Exception as e:
        logging.error(f"Error in search_jobs: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(host='0.0.0.0', port=5000)  # Running on all interfaces
