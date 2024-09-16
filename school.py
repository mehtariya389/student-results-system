# Name: Riya Mehta
# Student ID: s3973715

# Heighest Level attemped: HD


# In-code Analysis: why you introduce a particular function/method, why you choose to use a while loop instead of other loops, why you choose a particular data type to store the data information

# Code Analysis: 
# 1. I started by writing the algorithm for the result class, then the course and student class.
# 2. I then wrote the code for the result class.
# 3. After completing the pass level I edited my algorithm for the course class to include the modified course data.
# 4. Challenge 1: No entries printing in the results table. (Resolved by striping the spaces in the course IDs in the results dictionary.)
# 5. Challenge 2: Formatting table borders.
# 6. Challenge 3: Saving the output in the results file entered in the command file. (Resolved by using results_file as an argument in the methods.)
# 7. Challenge 4: Saving the output using methods from the results class. (Resolved)

# References: Course modules and https://www.lucidchart.com/pages/uml-class-diagram (for class diagram)

import sys
import os
import datetime

# Course class:
# 1. Takes the data from the course file and first creates a list of courses IDs.
# 2. If course IDs do not start with either COSC, ISYS or MATH then it will display an error message and exit.
# 2. Create a dictionary with the course data.
# 3. Define the method to find the total number of courses.
# 4. Define the method nfinish to calculate the number of students who finished the course.
#   a. Takes the results dictionary and course as an argument.
#   b. The number of students who finished a particular course i.e. the number of scores that are not '--' or ' '.
# 5. Define the method nongoing to calculate the number of students who are still doing a particular course.
#   a. Takes the results dictionary and course_id as an argument.
#   b. The number of students who are still doing the course i.e. the number of scores that are '--'.
# 6. Define the method avg_score to calculate the average score of the students who finished a particular course.
#   a. Takes the results dictionary as an argument.
#   b. The average score of the students who finished the course i.e. the sum of the scores divided by the number of students who finished the course.
# 7. Define the method course information to display course information in a table with courseid, name, type, credit, semester, average, nfinish and nongoing.
# 8. Define the method course summary to display the most difficult core course and the most difficult elective course.
#   a. Takes the results dictionary as an argument.
#   b. Finds and prints most difficult core course is the core course by calculating the lowest average score.
#   c. Finds and prints most difficult elective course is the elective course by calculating the lowest average score.


class Course:
    def __init__(self, filename):
        self.course_ids = self.load_courses(filename)
        self.courses_data = self.load_courses_data(filename)

    def load_courses(self, filename):
        course_ids = []
        with open(filename, 'r') as file:
            for line in file:
                course_data = line.strip().split(',')
                course_id = course_data[0].strip()
                course_ids.append(course_id)
        self.course_ids = course_ids
        return course_ids
    
    def is_valid_course_id(self):
        for course in self.course_ids:
            if not (course.startswith('COSC') or course.startswith('ISYS') or course.startswith('MATH')):
                return False
        return True

    def load_courses_data(self, filename):
        courses = {}
        with open(filename, 'r') as file:
            for line in file:
                course_data = line.strip().split(',')
                course_id = course_data[0].strip()
                course_type = course_data[1].strip()
                course_name = course_data[2].strip()
                credit_points = course_data[3].strip()
                if len(course_data) == 5:
                    semester = course_data[4].strip()
                else:
                    semester = 'All'
                courses[course_id] = {
                    'course_type': course_type,
                    'course_name': course_name,
                    'credit_point': credit_points,
                    'semester': semester
                }
        self.courses_data = courses
        return courses

    def total_courses(self):
        return len(self.course_ids)

    def nfinish(self, results, course):
        count = 0
        for student, scores in results.items():
            if course in scores and scores[course] not in ('--', ' '):
                count += 1
        return count

    def nongoing(self, results, course_id):
        count = 0
        for student, scores in results.items():
            if course_id in scores and scores[course_id] == '--':
                count += 1
        return count

    def avg_score(self, results, course):
        sum_scores = 0
        count = 0
        for student, scores in results.items():
            if course in scores and scores[course] not in ('--', ' '):
                sum_scores += float(scores[course])
                count += 1
        if count == 0:
            return 0
        return round(sum_scores / count, 2)

    def most_difficult_core_course(self, results):
        min_avg_score = float('inf')
        most_difficult_core_course = ''
        for course in self.course_ids:
            if self.courses_data[course]['course_type'] == 'C':
                avg_score = self.avg_score(results, course)
                if avg_score < min_avg_score:
                    min_avg_score = avg_score
                    most_difficult_core_course = course
        return most_difficult_core_course, min_avg_score

    def most_difficult_elective_course(self, results):
        min_avg_score = float('inf')
        most_difficult_elective_course = ''
        for course in self.course_ids:
            if self.courses_data[course]['course_type'] == 'E':
                avg_score = self.avg_score(results, course)
                if avg_score < min_avg_score:
                    min_avg_score = avg_score
                    most_difficult_elective_course = course
        return most_difficult_elective_course, min_avg_score

    def course_information(self, results, results_file):
        header = "{:<10} {:<10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}".format(
            "CourseID", "Name", "Type", "Credit", "Semester", "Average", "NFinish", "NOngoing"
        )
        header_border = '-' * len(header)

        output = []
        output.append("COURSE INFORMATION")

        course_data = {}  # Dictionary to store course data

        # Collect course data
        for course in self.course_ids:
            course_type = self.courses_data[course]['course_type']
            average = self.avg_score(results, course)

            if course_type not in course_data:
                course_data[course_type] = []

            course_data[course_type].append((course, average))

        # Sort and display course information for each course type
        for course_type in sorted(course_data.keys()):
            output.append(header_border)
            output.append(header)
            output.append(header_border)

            sorted_data = sorted(course_data[course_type], key=lambda x: x[1], reverse=True)

            for course, average in sorted_data:
                course_id = course
                name = self.courses_data[course]['course_name']
                credit = self.courses_data[course]['credit_point']
                semester = self.courses_data[course]['semester']
                nfinish = self.nfinish(results, course)
                nongoing = self.nongoing(results, course)

                row = "{:<10} {:<10} {:>10} {:>10} {:>10} {:>10.2f} {:>10} {:>10}".format(
                    course_id, name, course_type, credit, semester, average, nfinish, nongoing
                )
                output.append(row)

            output.append("")  # Add an empty line after each course type section
        
        output = '\n'.join(output)
        Result.set_output(output)  # Set the output in the Result class
        Result.save_results(results_file, output)  # Call the save_results() method without the 'output' argument

        print(output)


    def course_summary(self, results):
        print("COURSE SUMMARY")
        most_difficult_core_course, core_avg = self.most_difficult_core_course(results)
        most_difficult_elective_course,  elective_avg = self.most_difficult_elective_course(results)

        print(f"The most difficult core course is {most_difficult_core_course} with average score {core_avg}.")
        print(f"The most difficult elective course is {most_difficult_elective_course} with average score {elective_avg}.")




# Student class:
# 1. Takes the data from the student file and creates a list of students.
# 2. If student ID doesn’t start with the letter S then it will display an error message and exit.
# 2. Define the method to find the total number of students.
# 3. Create a dictionary with the student data.
#   a. The key is the student id.
#   b. The value is a list with the student name, student type and  if the student type is UG, then mode is appended as FT otherwise read the mode from the student file.
# 4. Define the method to check if a student satisfies the minimum enrollment requirements.
#   a. Takes the results dictionary as an argument.
#   b. If the studend mode is full time i.e. FT:
#       i.  Counts the number of courses the student does not have a score ' '.
#       ii. If the count is less than 4, then append '(!)' to the student name.
#   c. If the student mode is part time i.e. PT:
#       i.  Counts the number of courses the student does not have a score ' '.
#       ii. If the count is less than 2, then append '(!)' to the student name.
# 5. Define the method nfinish to calculate the number of courses a student has finished.
#   a. Takes the results dictionary and student_ID as an argument.
#   b. The number of courses finished i.e. the number of scores that are not '--' or ' '.
# 6. Define the method nongoing to calculate the number of courses a student is still doing.
#   a. Takes the results dictionary and student_ID as an argument.  
#   b. The number of courses still doing i.e. the number of scores that are '--'.
# 7. Define the method avg_score to calculate the average score of the student.
#   a. Takes the results dictionary and student_ID as an argument.
#   b. The average score of the student i.e. the sum of the scores divided by the number of courses finished.
# 8. Define the method GPA to calculate the GPA of the student.
#   a. Takes the results dictionary, course_ID and student_ID as an argument.
#   b. Check if the score is not '--' or ' '.
#   c. If the score is not '--' or ' ' then:
#       i. If the score is >=79.5 then GPA = 4.0.
#       ii. If the score is >=69.5 and <79.5 then GPA = 3.
#       iii. If the score is >=59.5 and <69.5 then GPA = 2.
#       iv. If the score is >=49.5 and <59.5 then GPA = 1.
#       v. If the score is <49.5 then GPA = 0.
#   d. If the score is '--' or ' ' then GPA = 0.
# 9. Define the method avg_GPA to calculate the average GPA of the student.
#   a. Takes the results dictionary and student_ID as an argument.
#   b. The average GPA of the student i.e. the sum of the GPAs divided by the number of courses finished.
# 10. Define the method WGPA to calculate the weighted GPA of the student.
#   a. Takes the results dictionary, courses dictionary and student_ID as an argument.
#   b. The weighted GPA of the student i.e. the sum of the GPAs multiplied by the credit points divided by the credit points of finished courses.
# 11. Define the method best_pg_student to find the pg student with the highest average GPA and return the student ID and the average GPA.
# 12. Define the method best_ug_student to find the ug student with the highest average GPA and return the student ID and the average GPA.
# 13. Define the method student_information to display student information in a table with studentid, name, type, mode, average, GPA, nfinish and nongoing.
# 14. Define the method student_summary to display the best pg student and the best ug student.


class Student:
    def __init__(self, filename):
        self.students = self.load_students(filename)
        self.students_data = self.load_students_data(filename)


    def load_students(self, filename):
        students = []
        with open(filename, 'r') as file:
            for line in file:
                student = line.strip().split(',')
                students.append(student[0])
        return students
    
    def is_valid_student_id(self):
        for student in self.students:
            if not student.startswith('S'):
                return False
        return True
    
    def load_students_data(self, filename):
        student_info = {}
        with open(filename, 'r') as file:
            for line in file:
                student_data = line.strip().split(',')
                student_id = student_data[0].strip()
                student_name = student_data[1].strip()
                student_type = student_data[2].strip()
                if student_type == 'UG':
                    student_mode = 'FT'
                else:
                    student_mode = student_data[3].strip()
                student_info[student_id] = [student_name, student_type, student_mode]
        return student_info

    def total_students(self):
        return len(self.students)
    
    def check_enrollment(self, results):
        for student, scores in results.items():
            if self.students_data[student][2] == 'FT':
                count = 0
                for score in scores.values():
                    if score != ' ':
                        count += 1
                if count < 4:
                    self.students_data[student][0] += '(!)'
            else:
                count = 0
                for score in scores.values():
                    if score != ' ':
                        count += 1
                if count < 2:
                    self.students_data[student][0] += '(!)'

    def nfinish(self, results, student_id):
        count = 0
        for course, scores in results[student_id].items():
            if scores not in ('--', ' '):
                count += 1
        return count
    
    def nongoing(self, results, student_id):
        count = 0
        for course, scores in results[student_id].items():
            if scores == '--':
                count += 1
        return count
    
    def avg_score(self, results, student_id):
        sum_scores = 0
        count = 0
        for course, scores in results[student_id].items():
            if scores not in ('--', ' '):
                sum_scores += float(scores)
                count += 1
        if count == 0:
            return 0
        return round(sum_scores / count, 2)
    
    def GPA(self, results, course_id, student_id):
        score = results[student_id][course_id]
        if score not in ('--', ' '):
            if float(score) >= 79.5:
                return 4.0
            elif float(score) >= 69.5:
                return 3.0
            elif float(score) >= 59.5:
                return 2.0
            elif float(score) >= 49.5:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0
        
    def avg_GPA(self, results, student_id):
        sum_GPA = 0
        count = 0
        for course, scores in results[student_id].items():
            if scores not in ('--', ' '):
                sum_GPA += self.GPA(results, course, student_id)
                count += 1
        if count == 0:
            return 0
        return round(sum_GPA / count, 2)
    
    def WGPA(self, results, courses, student_id):
        sum_GPA = 0
        sum_credit_points = 0
        for course, scores in results[student_id].items():
            if scores not in ('--', ' '):
                sum_GPA += self.GPA(results, course, student_id) * int(courses[course]['credit_point'])
                sum_credit_points += int(courses[course]['credit_point'])
        if sum_credit_points == 0:
            return 0
        return round(sum_GPA / sum_credit_points, 2)

    
    def best_pg_student(self, results):
        max_avg_GPA = 0
        best_pg_student = ''
        for student in self.students:
            if self.students_data[student][1] == 'PG':
                avg_GPA = self.avg_GPA(results, student)
                if avg_GPA > max_avg_GPA:
                    max_avg_GPA = avg_GPA
                    best_pg_student = student
        return best_pg_student, max_avg_GPA
    
    def best_ug_student(self, results):
        max_avg_GPA = 0
        best_ug_student = ''
        for student in self.students:
            if self.students_data[student][1] == 'UG':
                avg_GPA = self.avg_GPA(results, student)
                if avg_GPA > max_avg_GPA:
                    max_avg_GPA = avg_GPA
                    best_ug_student = student
        return best_ug_student, max_avg_GPA
    
    def student_information(self, results, courses, results_file):
        header = "{:<10} {:<10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}".format(
            "StudentID", "Name", "Type", "Mode", "GPA(100)", "GPA(4)", "WGPA(4)", "NFinish", "NOngoing"
        )
        header_border = '-' * len(header)

        output = []
        output.append("STUDENT INFORMATION")

        student_data = {}  # Dictionary to store student data

        # Collect student data
        for student in self.students:
            student_type = self.students_data[student][1]
            wgpa = self.WGPA(results, courses, student)

            if student_type not in student_data:
                student_data[student_type] = []

            student_data[student_type].append((student, wgpa))

        # Sort and display student information for each student type
        for student_type in sorted(student_data.keys()):
            output.append(header_border)
            output.append(header)
            output.append(header_border)
        
            sorted_data = sorted(student_data[student_type], key=lambda x: x[1], reverse=True)

            for student, wgpa in sorted_data:
                student_id = student
                name = self.students_data[student][0]
                mode = self.students_data[student][2]
                average = self.avg_score(results, student)
                gpa = self.avg_GPA(results, student)
                nfinish = self.nfinish(results, student)
                nongoing = self.nongoing(results, student)

                row = "{:<10} {:<10} {:>10} {:>10} {:>10.2f} {:>10.2f} {:>10.2f} {:>10} {:>10}".format(
                    student_id, name, student_type, mode, average, gpa, wgpa, nfinish, nongoing
                )
                output.append(row)

            output.append("")  # Add an empty line after each student type section
        
        output = '\n'.join(output)
        Result.set_output(output)  # Set the output in the Result class
        Result.save_results(results_file, output)  # Call the save_results() method without the 'output' argument

        print(output)

    def student_summary(self, results):
        print("STUDENT SUMMARY")
        best_pg_student, pg_avg_GPA = self.best_pg_student(results)
        best_ug_student, ug_avg_GPA = self.best_ug_student(results)

        print(f"The best PG student is {best_pg_student} with average GPA {pg_avg_GPA}.")
        print(f"The best UG student is {best_ug_student} with average GPA {ug_avg_GPA}.")

# Result class:
# 1. Reads the from three files specified in the command line arguments, namely result file, course file and student file.
# 2. If result file is empty then it will display an error message and exit.
# 3. If the scores in the result file is not a number or missing or ' ' then it will display an error message and exit.
# 4. If the number of arguements is 3:
#   a.  If the any(all) file(s) is(are) not found, it will display an error message and exit.
#   b.  If the file(s) is(are) found: 
#       i. Reads the student file and creates a list of students using the attributes of the student class.
#       ii. Reads the course file and creates a list of courses using the attributes of the course class.
#       iii. Reads the result file and creates a disctionary as follows:
#           1. The key is the student id.
#           2. The value is the list of scores of the student in each course.
#           2. Find the student id in the result file:
#               a. Using the list of courses, check if the student has taken the course.
#               b. If the student has taken the course:
#                   i.  If the student has a score in the result file then applend the score.
#                   ii. If the student does not have a score in the result file then append '--'.
#               c. If the student has not taken the course then append ' '.  
# 5. Define the method pass rate:
#   a. Takes the results dictionary as an argument.
#   b. Finds the pass scores i.e. the number of scores greater than or equal to 49.5.
#   c. Finds the total number of available scores i.e. the number of scores that are not '--' or ' '.
#   d. Calculates the pass rate = (pass scores/total number of available scores) * 100.
# 6. Displays the results dictionary in the form of a table.
#   a. The student IDs are aligned to the right.
#   b. The course IDs and scores are aligned to the left.
# 7. Displays the results summary.
#   a. Finds the total number of students using the student class.
#   b. Finds the total number of courses using the course class.
#   c. Prints the total number of students and courses.
#   d. Prints the pass rate using the pass rate method.

class Result:
    def __init__(self, result_file, course_file, student_file):
        self.students = Student(student_file).students
        self.courses = Course(course_file).course_ids
        self.results = self.load_results(result_file)

    def is_empty(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                return False
        return True
    
    def are_scores_valid(self):
        with open(sys.argv[1], 'r') as file:
            for line in file:
                line = line.strip()
                if not line or ',' not in line:
                    continue  # Skip empty lines and lines without comma-separated values

                student_id, course_id, score = line.split(',', maxsplit=2)
                student_id = student_id.strip()
                course_id = course_id.strip()
                score = score.strip()

                if not score:
                    continue  # Skip lines without a score value

                try:
                    float(score)
                except ValueError:
                    return False

        return True


    def load_results(self, filename):
        results = {}
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or ',' not in line:
                    continue
                
                student_id, course_id, score = line.split(',', maxsplit=2)
                if student_id not in results:
                    results[student_id] = {}
                if score:
                    results[student_id][course_id.strip()] = score
                else:
                    results[student_id][course_id.strip()] = '--'
                for course in self.courses:
                    if course not in results[student_id]:
                        results[student_id][course] = ' '

        return results
    

    def pass_rate(self):
        pass_scores = 0
        total_scores = 0
        for student_scores in self.results.values():
            for score in student_scores.values():
                if score != '--' and score != ' ':
                    total_scores += 1
                    if float(score) >= 49.5:
                        pass_scores += 1
        if total_scores == 0:
            return 0
        pass_rate = (pass_scores / total_scores) * 100
        return pass_rate
    
    @staticmethod
    def save_results(results_file, output):
        with open(results_file, "r+") as file:
            content = file.read()
            file.seek(0, 0)  # Move the file pointer to the beginning of the file
            file.write(output + '\n\n' + content)

    @staticmethod
    def set_output(output):
        Result.output = output

    def get_current_datetime(self):
        now = datetime.datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def display_results_table(self, results_file):
        output = []

        output.append(f"Report generated on: {self.get_current_datetime()}")
        output.append("RESULTS")
        header_border = '-' * (11 + 11 * len(self.courses))
        output.append(header_border)
        header = "{:<10}".format("Student")
        for course in self.courses:
            header += "{:>10}".format(course)
        output.append(header)
        output.append(header_border)

        for student, scores in self.results.items():
            student_row = "{:<10}".format(student)

            for course in self.courses:
                student_row += "{:>10}".format(scores.get(course, ""))
            output.append(student_row)
            output.append("")
        
        output = '\n'.join(output)
        self.save_results(results_file, output)

        print(output)


    def display_results_summary(self):
        total_students = len(self.students)
        total_courses = len(self.courses)
        pass_rate = self.pass_rate()

        print("RESULTS SUMMARY")
        print(f"There are {total_students} students and {total_courses} courses.")
        print(f"The average pass rate is {pass_rate}%.")

# Result system class:
# 1. Takes the data from the command line arguments.
# 2. If the number of files is less than 3, it will display an error message and exit.
# 3.  If the any(all) file(s) is(are) not found, it will display an error message ('File_name(s)' not found) and exit.
# 4.  If the file(s) is(are) found proceed to display the information.

class ResultSystem:
    def __init__(self):
        pass

    def main(self):
        if len(sys.argv) != 4:
            print("Usage: python program.py result_file course_file student_file")
            sys.exit(1)

        if not os.path.exists(sys.argv[1]):
            print(f"{sys.argv[1]} not found")
            sys.exit(1)

        if not os.path.exists(sys.argv[2]):
            print(f"{sys.argv[2]} not found")
            sys.exit(1)

        if not os.path.exists(sys.argv[3]):
            print(f"{sys.argv[3]} not found")
            sys.exit(1)

        result_file = sys.argv[1]
        course_file = sys.argv[2]
        student_file = sys.argv[3]


        result = Result(result_file, course_file, student_file)
        

        if result.is_empty(result_file):
            print(f"{result_file} is empty")
            sys.exit(1)

        if not result.are_scores_valid():
            print(f"{result_file} contains invalid scores")
            sys.exit(1)


        course = Course(course_file)

        if not course.is_valid_course_id():
            print(f"{course_file} contains invalid course IDs")
            sys.exit(1)

        student = Student(student_file)

        if not student.is_valid_student_id():
            print(f"{student_file} contains invalid student IDs")
            sys.exit(1)

        student.student_information(result.results, course.courses_data, result_file)
        print()
        student.student_summary(result.results)
        print()
        course.course_information(result.results, result_file)
        print()
        course.course_summary(result.results)
        print()
        result.display_results_table(result_file)
        print()
        result.display_results_summary()

if __name__ == '__main__':
    ResultSystem().main()