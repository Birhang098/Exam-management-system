import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class Database:
    @staticmethod
    def insert_faculty_user(username, email, password):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()
            query = "INSERT INTO faculty_users (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, email, password))
            connection.commit()
            return True  # Indicates successful insertion
        except Error as e:
            print("Error inserting faculty user:", e)
            return False  # Indicates insertion failure
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def insert_student_user(username, email, password):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()
            query = "INSERT INTO student_users (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, email, password))
            connection.commit()
            return True  # Indicates successful insertion
        except Error as e:
            print("Error inserting student user:", e)
            return False  # Indicates insertion failure
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_faculty_user_by_username(username):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM faculty_users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            return user
        except Error as e:
            print("Error fetching faculty user:", e)
            return None
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_student_user_by_username(username):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM student_users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            return user
        except Error as e:
            print("Error fetching student user:", e)
            return None
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_all_exams():
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM exam"
            cursor.execute(query)
            exams = cursor.fetchall()
            return exams
        except Error as e:
            print("Error fetching exam records:", e)
            return []
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def insert_exam(exam_date, exam_time, room_number, roll_number, invigilator, subject_code, branch, semester, regular_student_count, back_student_count):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()
            query = "INSERT INTO exam (exam_date, exam_time, room_number, roll_number, invigilator_teacher, subject_code, branch, semester, regular_student_count, back_student_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (exam_date, exam_time, room_number, roll_number, invigilator, subject_code, branch, semester, regular_student_count, back_student_count))
            connection.commit()
            return True  # Indicates successful insertion
        except Error as e:
            print("Error inserting exam record:", e)
            return False  # Indicates insertion failure
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def search_exam_by_teacher(invigilator_teacher):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM exam WHERE invigilator_teacher = %s"
            cursor.execute(query, (invigilator_teacher,))
            exams = cursor.fetchall()
            return exams
        except Error as e:
            print("Error searching exam records:", e)
            return []
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def search_exam_by_date(exam_date):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM exam WHERE exam_date = %s"
            cursor.execute(query, (exam_date,))
            results = cursor.fetchall()
            return results
        except Error as e:
            print("Error searching for exams by date:", e)
            return []
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def search_exam_by_branch(branch):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM exam WHERE branch = %s"
            cursor.execute(query, (branch,))
            results = cursor.fetchall()
            return results
        except Error as e:
            print("Error searching for exams by branch:", e)
            return []
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def search_exam_by_semester(semester):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM exam WHERE semester = %s"
            cursor.execute(query, (semester,))
            results = cursor.fetchall()
            return results
        except Error as e:
            print("Error searching for exams by semester:", e)
            return []
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def insert_faculty_details(invigilator_teacher, branch):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()
            query = "INSERT INTO faculty_details (invigilator_teacher, branch) VALUES (%s, %s)"
            cursor.execute(query, (invigilator_teacher, branch))
            connection.commit()
            return True
        except Error as e:
            print(f"Error inserting faculty details: {e}")
            return False
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def insert_student_details(name, roll_number, branch, semester, batch):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()
            query = "INSERT INTO students_details (name, roll_number, branch, semester, batch) VALUES (%s, %s, %s, %s, %s)"
            values = (name, roll_number, branch, semester, batch)
            cursor.execute(query, values)
            connection.commit()
            return True
        except Error as e:
            print(f"Error inserting student details: {e}")
            return False
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()


    @staticmethod
    def insert_teacher_details(employee_id, invigilator_teacher, branch):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()
            query = "INSERT INTO teachers_details (employee_id, invigilator_teacher, branch) VALUES (%s, %s, %s)"
            cursor.execute(query, (employee_id, invigilator_teacher, branch))
            connection.commit()
            return True
        except Error as e:
            print(f"Error inserting teacher details: {e}")
            return False
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()


    @staticmethod
    def get_all_student_details():
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM students_details"
            cursor.execute(query)
            student_details = cursor.fetchall()
            return student_details
        except Error as e:
            print(f"Error fetching all student details: {e}")
            return None
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()


    @staticmethod
    def search_student_details_by_roll_number(roll_number):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM students_details WHERE roll_number = %s"
            cursor.execute(query, (roll_number,))
            student_details = cursor.fetchall()
            return student_details
        except Error as e:
            print(f"Error searching student details by roll number: {e}")
            return None
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()



    @staticmethod
    def get_all_teacher_details():
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM teachers_details"
            cursor.execute(query)
            teacher_details = cursor.fetchall()
            return teacher_details
        except Error as e:
            print(f"Error fetching all teacher details: {e}")
            return None
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

                

    @staticmethod
    def search_teacher_details_by_invigilator(invigilator_name):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM teachers_details WHERE invigilator_teacher = %s"
            cursor.execute(query, (invigilator_name,))
            teacher_details = cursor.fetchall()
            return teacher_details
        except Error as e:
            print(f"Error searching teacher details by invigilator: {e}")
            return None
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()









