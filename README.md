# Student Results System

## Overview
This project implements a Student Results System, designed to manage and analyze academic results for students across various courses. The system is capable of processing student data, course information, and individual results to generate comprehensive reports and statistics.

## Features
- Load and validate student, course, and result data from files
- Generate detailed student information reports
- Produce course information and statistics
- Calculate and display overall results summary
- Identify top-performing students in undergraduate and postgraduate categories
- Determine the most challenging courses for core and elective subjects

## Class Structure
The system is composed of four main classes:
1. `Student`: Manages student-related data and calculations
2. `Course`: Handles course information and statistics
3. `Result`: Processes and stores the overall results data
4. `ResultSystem`: Orchestrates the entire system and handles file I/O

## How to Use
1. Prepare your input files:
   - `student_file`: Contains student information
   - `course_file`: Contains course details
   - `result_file`: Contains individual student results for each course

2. Run the program using the command:
   ```
   python school.py result_file course_file student_file
   ```

3. The system will generate various reports:
   - Student Information
   - Student Summary (Best PG and UG students)
   - Course Information
   - Course Summary (Most difficult core and elective courses)
   - Results Table
   - Results Summary

## Requirements
- Python 3.x

## Input File Formats
- All input files should be in CSV format
- `student_file`: StudentID, Name, Type (UG/PG), Mode (FT/PT for PG)
- `course_file`: CourseID, Type (C/E), Name, Credit Points, Semester
- `result_file`: StudentID, CourseID, Score

## Error Handling
The system includes various error checks:
- File existence verification
- Empty file detection
- Invalid course/student ID validation
- Score validity checks

## Future Improvements
- Implement a graphical user interface
- Add database support for data persistence
- Introduce more advanced statistical analysis features

## Author
Riya Mehta (Student ID: s3973715)
