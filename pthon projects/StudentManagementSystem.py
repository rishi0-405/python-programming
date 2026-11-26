import json
import os
from datetime import datetime
FILE_NAME = "students.json"


# DATA MANAGEMENT

def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_data(students):
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)


#  GRADE CALCULATION 

def calculate_percentage(marks):
    if not marks:
        return 0

    total = sum(marks.values())
    maximum = len(marks) * 100

    return round((total / maximum) * 100, 2)


def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"


#  STUDENT OPERATIONS 

def add_student(students):
    student_id = input("Enter Student ID: ")

    if student_id in students:
        print("Student ID already exists!")
        return

    name = input("Enter Student Name: ")
    age = int(input("Enter Age: "))
    course = input("Enter Course: ")

    subjects = ["Python", "Maths", "English", "Data Structures"]

    marks = {}

    for subject in subjects:
        while True:
            try:
                score = float(input(f"Enter {subject} marks: "))

                if 0 <= score <= 100:
                    marks[subject] = score
                    break

                print("Marks must be between 0 and 100.")

            except ValueError:
                print("Enter a valid number.")

    students[student_id] = {
        "name": name,
        "age": age,
        "course": course,
        "marks": marks,
        "attendance": 0,
        "total_classes": 0,
        "created_at": str(datetime.now().date())
    }

    save_data(students)
    print("Student added successfully!")


def display_students(students):
    if not students:
        print("No student records found.")
        return

    print("\n========== STUDENT LIST ==========")

    for student_id, details in students.items():
        print("\nStudent ID:", student_id)
        print("Name:", details["name"])
        print("Age:", details["age"])
        print("Course:", details["course"])


def search_student(students):
    search = input("Enter Student ID or Name: ").lower()

    found = False

    for student_id, details in students.items():
        if (search == student_id.lower()
                or search in details["name"].lower()):

            print("\nStudent Found!")
            print("ID:", student_id)
            print("Name:", details["name"])
            print("Course:", details["course"])
            print("Marks:", details["marks"])

            found = True

    if not found:
        print("Student not found.")


def update_student(students):
    student_id = input("Enter Student ID to update: ")

    if student_id not in students:
        print("Student not found.")
        return

    student = students[student_id]

    print("1. Update Name")
    print("2. Update Age")
    print("3. Update Course")
    print("4. Update Marks")

    choice = input("Choose option: ")

    if choice == "1":
        student["name"] = input("New Name: ")

    elif choice == "2":
        student["age"] = int(input("New Age: "))

    elif choice == "3":
        student["course"] = input("New Course: ")

    elif choice == "4":
        for subject in student["marks"]:
            score = float(input(f"{subject} marks: "))

            if 0 <= score <= 100:
                student["marks"][subject] = score
            else:
                print("Invalid marks.")
                return

    else:
        print("Invalid option.")
        return

    save_data(students)
    print("Record updated successfully!")


def delete_student(students):
    student_id = input("Enter Student ID: ")

    if student_id in students:
        confirm = input("Are you sure? (yes/no): ")

        if confirm.lower() == "yes":
            del students[student_id]
            save_data(students)
            print("Student deleted.")

    else:
        print("Student not found.")


#  ACADEMIC REPORTS 

def student_report(students):
    student_id = input("Enter Student ID: ")

    if student_id not in students:
        print("Student not found.")
        return

    student = students[student_id]
    marks = student["marks"]

    percentage = calculate_percentage(marks)
    grade = calculate_grade(percentage)

    print("\n========== REPORT CARD ==========")
    print("Name:", student["name"])
    print("Student ID:", student_id)

    for subject, score in marks.items():
        print(subject, ":", score)

    print("Total Marks:", sum(marks.values()))
    print("Percentage:", percentage, "%")
    print("Grade:", grade)

    attendance = student["attendance"]
    total = student["total_classes"]

    if total > 0:
        attendance_percentage = (attendance / total) * 100
    else:
        attendance_percentage = 0

    print("Attendance:", round(attendance_percentage, 2), "%")


def class_topper(students):
    if not students:
        print("No records available.")
        return

    topper_id = None
    highest_percentage = -1

    for student_id, student in students.items():
        percentage = calculate_percentage(student["marks"])

        if percentage > highest_percentage:
            highest_percentage = percentage
            topper_id = student_id

    topper = students[topper_id]

    print("\n========== CLASS TOPPER ==========")
    print("Name:", topper["name"])
    print("Student ID:", topper_id)
    print("Percentage:", highest_percentage)


def class_statistics(students):
    if not students:
        print("No student records.")
        return

    percentages = [
        calculate_percentage(s["marks"])
        for s in students.values()
    ]

    average = sum(percentages) / len(percentages)

    passed = sum(1 for p in percentages if p >= 40)
    failed = len(percentages) - passed

    print("\n========== CLASS STATISTICS ==========")
    print("Total Students:", len(students))
    print("Class Average:", round(average, 2), "%")
    print("Passed:", passed)
    print("Failed:", failed)


# ATTENDANCE MANAGEMENT 

def mark_attendance(students):
    student_id = input("Enter Student ID: ")

    if student_id not in students:
        print("Student not found.")
        return

    student = students[student_id]

    student["total_classes"] += 1

    status = input("Present or Absent (P/A): ").upper()

    if status == "P":
        student["attendance"] += 1
        print("Present marked.")

    elif status == "A":
        print("Absent marked.")

    else:
        student["total_classes"] -= 1
        print("Invalid attendance status.")
        return

    save_data(students)


def attendance_report(students):
    if not students:
        print("No records found.")
        return

    print("\n========== ATTENDANCE REPORT ==========")

    for student_id, student in students.items():
        total = student["total_classes"]
        present = student["attendance"]

        percentage = (present / total * 100) if total else 0

        print(
            student["name"],
            "| Present:", present,
            "| Classes:", total,
            "| Attendance:", round(percentage, 2), "%"
        )


# SEARCH AND FILTER 

def students_by_grade(students):
    grade = input("Enter Grade to search: ").upper()

    found = False

    for student_id, student in students.items():
        percentage = calculate_percentage(student["marks"])
        student_grade = calculate_grade(percentage)

        if student_grade == grade:
            print(student_id, student["name"], percentage)
            found = True

    if not found:
        print("No students found in this grade.")


def sort_students(students):
    sorted_students = sorted(
        students.items(),
        key=lambda item: calculate_percentage(item[1]["marks"]),
        reverse=True
    )

    print("\n========== RANK LIST ==========")

    for rank, (student_id, student) in enumerate(
        sorted_students, start=1
    ):
        percentage = calculate_percentage(student["marks"])

        print(
            rank,
            student["name"],
            "-",
            percentage,
            "%"
        )


# EXPORT REPORT 

def export_report(students):
    filename = "class_report.txt"

    with open(filename, "w") as file:
        file.write("STUDENT PERFORMANCE REPORT\n")
        file.write("=" * 40 + "\n")

        for student_id, student in students.items():
            percentage = calculate_percentage(
                student["marks"]
            )

            grade = calculate_grade(percentage)

            file.write("\nName: " + student["name"])
            file.write("\nID: " + student_id)
            file.write("\nPercentage: " + str(percentage))
            file.write("\nGrade: " + grade)
            file.write("\n" + "-" * 30 + "\n")

    print("Report exported to", filename)


# MAIN MENU

def main():
    students = load_data()

    while True:
        print("\n")
        print("=" * 45)
        print("       STUDENT MANAGEMENT SYSTEM")
        print("=" * 45)

        print("1. Add Student")
        print("2. Display All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Generate Student Report")
        print("7. Find Class Topper")
        print("8. Class Statistics")
        print("9. Mark Attendance")
        print("10. Attendance Report")
        print("11. Search Students by Grade")
        print("12. Sort Students by Performance")
        print("13. Export Class Report")
        print("14. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_student(students)

        elif choice == "2":
            display_students(students)

        elif choice == "3":
            search_student(students)

        elif choice == "4":
            update_student(students)

        elif choice == "5":
            delete_student(students)

        elif choice == "6":
            student_report(students)

        elif choice == "7":
            class_topper(students)

        elif choice == "8":
            class_statistics(students)

        elif choice == "9":
            mark_attendance(students)

        elif choice == "10":
            attendance_report(students)

        elif choice == "11":
            students_by_grade(students)

        elif choice == "12":
            sort_students(students)

        elif choice == "13":
            export_report(students)

        elif choice == "14":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice. Try again.")


#  PROGRAM EXECUTION 

if __name__ == "__main__":
    main()





# to RUN =    python student_management.py


