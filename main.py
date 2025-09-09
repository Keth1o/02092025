import sqlite3

conn = sqlite3.connect("university.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    major TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT NOT NULL,
    instructor TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS enrollments (
    student_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    PRIMARY KEY (student_id, course_id)
);
""")
conn.commit()
conn.close()


def add_student():
    name = input("Введіть ім'я студента: ")
    age = int(input("Введіть вік: "))
    major = input("Введіть спеціальність: ")

    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age, major) VALUES (?, ?, ?)", (name, age, major))
    conn.commit()
    conn.close()
    print("Студента додано!")


def add_course():
    course_name = input("Введіть назву курсу: ")
    instructor = input("Введіть ім'я викладача: ")

    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO courses (course_name, instructor) VALUES (?, ?)", (course_name, instructor))
    conn.commit()
    conn.close()
    print("Курс додано!")

def view_students():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    print("Список студентів:")
    for row in rows:
        print(f"ID: {row[0]}, Ім'я: {row[1]}, Вік: {row[2]}, Спеціальність: {row[3]}")

def view_courses():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    rows = cursor.fetchall()
    conn.close()

    print("Список курсів:")
    for row in rows:
        print(f"ID: {row[0]}, Назва: {row[1]}, Викладач: {row[2]}")

def enroll_student():
    view_students()
    student_id = int(input("Введіть ID студента: "))
    view_courses()
    course_id = int(input("Введіть ID курсу: "))

    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
        conn.commit()
        print("Студента зареєстровано на курс!")
    except sqlite3.IntegrityError:
        print("Студент вже зареєстрований на цей курс!")
    finally:
        conn.close()

def students_in_course():
    view_courses()
    course_id = int(input("Введіть ID курсу: "))

    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT s.id, s.name, s.major
    FROM students s
    JOIN enrollments e ON s.id = e.student_id
    WHERE e.course_id = ?
    """, (course_id,))
    rows = cursor.fetchall()
    conn.close()

    print("Студенти на курсі:")
    for row in rows:
        print(f"ID: {row[0]}, Ім'я: {row[1]}, Спеціальність: {row[2]}")

def menu():
    while True:
        print("Університет")
        print("1. Додати студента")
        print("2. Додати курс")
        print("3. Переглянути студентів")
        print("4. Переглянути курси")
        print("5. Зареєструвати студента на курс")
        print("6. Список студентів на курсі")
        print("7. Вийти")

        choice = input("Ваш вибір: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            add_course()
        elif choice == "3":
            view_students()
        elif choice == "4":
            view_courses()
        elif choice == "5":
            enroll_student()
        elif choice == "6":
            students_in_course()
        elif choice == "7":
            print("Вихід з програми")
            break
        else:
            print("Спробуйте ще раз.")