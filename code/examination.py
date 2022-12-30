import pandas as pd
import os
from rich.console import Console
import numpy as np
import ast
from rich.table import Table
import matplotlib.pyplot as plt

from common import get_dir

console = Console()
DATA_DIR=get_dir()

def create_exam_menu():
    console.print('[dark_goldenrod][bold]To View Students with Letter Marks Press:[/] 1[/]')
    console.print('[dark_goldenrod][bold]To View Scores of All Students Press:[/] 2[/]')
    console.print('[dark_goldenrod][bold]To View Course Wise Scatter Plot Press:[/] 3[/]')
    console.print('[dark_goldenrod][bold]To Go To Main Menu  Press:[/] 0[/]')
def display_letter_marks():
    course_df = pd.read_csv(os.path.join(DATA_DIR,'course.csv'))
    student_df = pd.read_csv(os.path.join(DATA_DIR,'student.csv'))
    table = Table(title="Letter Marks Table")
    table.add_column("Course Name", style="cyan", no_wrap=True)
    table.add_column("Student Roll Number", style="magenta")
    for i in range(len(course_df)):
        course_name = course_df.at[i,'Name']
        marks_dict = ast.literal_eval(course_df.at[i,'Marks Obtained'])
        for student_id in marks_dict:
            if float(marks_dict[student_id]) > 80:
                student_mask = student_df['Student Id'] == student_id
                student_pos = np.flatnonzero(student_mask)
                indx = student_pos[0]
                student_roll = student_df.at[indx,'Class Roll Number']
                table.add_row(course_name,str(student_roll))

    console.print(table)

def display_exam_statistics():
    # Get all batch names
    batch_df = pd.read_csv(os.path.join(DATA_DIR,'batch.csv'))
    student_df = pd.read_csv(os.path.join(DATA_DIR,'student.csv'))
    batches = []
    for i in range(len(batch_df)):
        batches.append(batch_df.at[i,"Batch ID"])
    course_df = pd.read_csv(os.path.join(DATA_DIR,'course.csv'))
    for i in range(len(course_df)):
        xplot = []
        yplot = []
        for batch in batches:
            course_total = 0
            student_count = 0
            marks_dict = ast.literal_eval(course_df.at[i,'Marks Obtained'])
            for student_id in marks_dict:
                # Check if the student belongs to this batch
                student_mask = student_df['Student Id'] == student_id
                student_pos = np.flatnonzero(student_mask)
                indx = student_pos[0]
                student_batch = student_df.at[indx,'Batch Name']
                if student_batch == batch:
                    course_total += float(marks_dict[student_id])
                    student_count += 1
            if student_count != 0:
                yplot.append(batch)
                xplot.append(course_total/student_count)
                plt.scatter(xplot,yplot)
    plt.show()


 
    print('To be implemented')
def view_exam_performance():
    student_df = pd.read_csv(os.path.join(DATA_DIR,'student.csv'))
    course_df = pd.read_csv(os.path.join(DATA_DIR,'course.csv'))
    table = Table(title="Exam Performance")
    table.add_column("Student Id", style="cyan", no_wrap=True)
    table.add_column("Percentage", style="magenta")
    for i in range(len(student_df)):
        student_id = student_df.at[i,'Student Id']
        course_count = 0
        marks = 0
        for j in range(len(course_df)):
            marks_dict = ast.literal_eval(course_df.at[j,'Marks Obtained'])
            if student_id in marks_dict:
                course_count = course_count + 1
                marks = marks + float(marks_dict[student_id])
        if not course_count == 0:
            student_percentage = marks/course_count
        else:
            student_percentage = 0
        table.add_row(student_id,str(student_percentage)+'%')
    console.print(table)
def process_exam():
    create_exam_menu()
    exam_choice = input('Enter Your Choice: ')
    while not exam_choice == '0':
        if exam_choice == '1':
            display_letter_marks()
        elif exam_choice == '2':
            view_exam_performance()
        elif exam_choice == '3':
            display_exam_statistics()
        create_exam_menu()
        exam_choice = input('Enter Your Choice: ')
