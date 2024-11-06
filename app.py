from flask import Flask, render_template, request, redirect, url_for, session
from database import Database
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        
        if user_type == 'faculty':
            return redirect(url_for('login_faculty'))
        elif user_type == 'student':
            return redirect(url_for('login_student'))
        else:
            return render_template('login.html', message='Invalid user type')
    
    return render_template('login.html')

@app.route('/menu')
def menu():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('menu.html')

@app.route('/add_exam', methods=['GET', 'POST'])
def add_exam():
    if not session.get('logged_in'):
        return redirect(url_for('login_faculty'))
    if request.method == 'POST':
        try:
            exam_date = request.form['exam_date']
            exam_time = request.form['exam_time']  # Adding exam_time
            room_number = request.form['room_number']
            roll_number = request.form['roll_number']
            invigilator = request.form['invigilator_teacher']
            subject_code = request.form['subject_code']  # Adding subject_code
            branch = request.form['branch']
            semester = request.form['semester']
            regular_student_count = request.form['regular_student_count']
            back_student_count = request.form['back_student_count']
            Database.insert_exam(exam_date, exam_time, room_number, roll_number, invigilator, subject_code, branch, semester, regular_student_count, back_student_count)
            return redirect(url_for('add_exam'))
        except KeyError:
            return render_template('add_exam.html', error_message='Please fill out all fields')
    return render_template('add_exam.html')


@app.route('/exam_records', methods=['GET', 'POST'])
def exam_records():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        search_criteria = request.form['search_criteria']
        search_value = request.form['search_value']
        
        if search_criteria == 'invigilator_teacher':
            search_results = Database.search_exam_by_teacher(search_value)
        elif search_criteria == 'exam_date':
            search_results = Database.search_exam_by_date(search_value)
        elif search_criteria == 'branch':
            search_results = Database.search_exam_by_branch(search_value)
        elif search_criteria == 'semester':
            search_results = Database.search_exam_by_semester(search_value)
        else:
            search_results = []  # Default case
        
        return render_template('exam_records.html', exams=[], search_results=search_results)
    
    exams = Database.get_all_exams()  
    return render_template('exam_records.html', exams=exams, search_results=None)


@app.route('/register_faculty', methods=['GET', 'POST'])
def register_faculty():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        # Add validation and error handling as needed
        
        Database.insert_faculty_user(username, email, password)  # Insert faculty user into database
        return redirect(url_for('login_faculty'))  # Redirect to login page after successful registration
    return render_template('register_faculty.html')

@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        # Add validation and error handling as needed
        
        Database.insert_student_user(username, email, password)  # Insert student user into database
        return redirect(url_for('login_student'))  # Redirect to student login page after successful registration
    return render_template('register_student.html')

@app.route('/login_faculty', methods=['GET', 'POST'])
def login_faculty():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Database.get_faculty_user_by_username(username)
        
        if user and user['password'] == password:
            session['logged_in'] = True
            session['user_type'] = 'faculty'
            return redirect(url_for('menu'))
        else:
            return render_template('login_faculty.html', message='Invalid username or password')
    return render_template('login_faculty.html')

@app.route('/login_student', methods=['GET', 'POST'])
def login_student():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Database.get_student_user_by_username(username)
        
        if user and user['password'] == password:
            session['logged_in'] = True
            session['user_type'] = 'student'
            return redirect(url_for('exam_records'))
        else:
            return render_template('login_student.html', message='Invalid username or password')
    return render_template('login_student.html')


@app.route('/add_student_details', methods=['GET', 'POST'])
def add_student_details():
    if request.method == 'POST':
        name = request.form.get('name')
        roll_number = request.form.get('roll_number')
        branch = request.form.get('branch')
        semester = request.form.get('semester')
        batch = request.form.get('batch')

        # Validate form data
        if not (name and roll_number and branch and semester and batch):
            return render_template('add_student_details.html', error_message='Please fill out all fields')

        # Insert student details into the database
        Database.insert_student_details(name, roll_number, branch, semester, batch)

    return render_template('add_student_details.html')




@app.route('/add_teacher_details', methods=['GET', 'POST'])
def add_teacher_details():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        invigilator_teacher = request.form.get('invigilator_teacher')
        branch = request.form.get('branch')
        
        if Database.insert_teacher_details(employee_id, invigilator_teacher, branch):
            return redirect(url_for('add_teacher_details'))  # Redirect to homepage after successful insertion
        else:
            return render_template('add_teacher_details.html', error_message='Failed to insert teacher details')
    
    return render_template('add_teacher_details.html')


@app.route('/faculty_student_details', methods=['GET', 'POST'])
def faculty_student_details():
    if request.method == 'POST':
        # Handle form submission
        search_query_student = request.form.get('search_student_roll')
        search_query_teacher = request.form.get('search_teacher_invigilator')

        if search_query_student:
            student_details = Database.search_student_details_by_roll_number(search_query_student)
            teacher_details = Database.get_all_teacher_details()
            return render_template('faculty_student_details.html', all_students=student_details, all_teachers=teacher_details)
        
        if search_query_teacher:
            teacher_details = Database.search_teacher_details_by_invigilator(search_query_teacher)
            student_details = Database.get_all_student_details()
            return render_template('faculty_student_details.html', all_students=student_details, all_teachers=teacher_details)
    
    # Fetch all student and teacher details if no search query is provided
    all_students = Database.get_all_student_details()
    all_teachers = Database.get_all_teacher_details()
    return render_template('faculty_student_details.html', all_students=all_students, all_teachers=all_teachers)


if __name__ == '__main__':
    app.run(debug=True)
