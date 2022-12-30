import pandas as pd
import os
from rich.console import Console
import numpy as np
import ast
from common import get_dir
from rich.table import Table
import matplotlib.pyplot as plt


console = Console()
DATA_DIR=get_dir()

def search_course(course_id):
    course_df = pd.read_csv(os.path.join(DATA_DIR,'course.csv'))
    course_mask = course_df['Course ID'] == course_id
    pos = np.flatnonzero(course_mask)
    if len(pos) > 0:
        return pos[0]
    else:
        return -1

def display_course():
    course_df = pd.read_csv(os.path.join(DATA_DIR,'course.csv'))
    table = Table(title="Exam Performance")
    table.add_column("Course ID", style="cyan", no_wrap=True)
    table.add_column("Course Name", style="magenta")
    table.add_column("Marks Obtained", style="green")
    for i in range(len(course_df)):
        course_id = course_df.at[i,'Course ID']
        course_name = course_df.at[i,'Name']
        marks_obtained = course_df.at[i,'Marks Obtained']
        table.add_row(course_id,course_name,marks_obtained)
    console.print(table)
    #print(course_df)
def create_course():
    course_df = pd.read_csv(os.path.join(DATA_DIR,'course.csv'))
    course_id = input('Course Id: ')
    course_name = input('Course Name: ')
    marks_dict = {}
    print('Enter marks of all students, to quit enter 0 for student id')
    student_id = input('Student Id: ')
    while not student_id == '0':
        marks = float(input('Marks Obtained: '))
        marks_dict[student_id] = marks
        student_id = input('Student Id: ')
    new_row = {'Course ID':[course_id],'Name':[course_name],'Marks Obtained':[marks_dict]}
    new_df = pd.DataFrame(new_row)
    whole_df = pd.concat([course_df,new_df],ignore_index = True)
    whole_df.to_csv(os.path.join(DATA_DIR,'course.csv'),index=False)
def show_course_performance():
    course_df = pd.read_csv(os.path.join(DATA_DIR,'course.csv'))
    course_id = input('Course ID: ')
    index_number = search_course(course_id)
    while not index_number >= 0:
        print("Course does not exist, please reenter")
        course_id = input('Course Id: ')
        index_number = search_course(course_id)
    mask = course_df['Course ID'] == course_id
    pos = np.flatnonzero(mask)
    marks_dict = ast.literal_eval(course_df.at[pos[0],'Marks Obtained'])
    table = Table(title="Course Performance")
    table.add_column("Student ID", style="cyan", no_wrap=True)
    table.add_column("Class Roll Number", style="magenta")
    table.add_column("Name", style="blue")
    table.add_column("Marks Obtained", style="green")
    student_df = pd.read_csv(os.path.join(DATA_DIR,'student.csv'))
    for student_id in marks_dict:
        student_mask = student_df['Student Id'] == student_id
        student_pos = np.flatnonzero(student_mask)
        indx = student_pos[0]
        student_roll = student_df.at[indx,'Class Roll Number']
        student_name = student_df.at[indx,'Name']
        student_marks = float(marks_dict[student_id])
        table.add_row(student_id,str(student_roll),student_name,str(student_marks))
    console.print(table)


def show_course_histogram():
    course_df = pd.read_csv(os.path.join(DATA_DIR,'course.csv'))
    course_id = input('Course ID: ')
    index_number = search_course(course_id)
    while not index_number >= 0:
        print("Course does not exist, please reenter")
        course_id = input('Course Id: ')
        index_number = search_course(course_id)
    mask = course_df['Course ID'] == course_id
    pos = np.flatnonzero(mask)
    marks_dict = ast.literal_eval(course_df.at[pos[0],'Marks Obtained'])
    student_grade_list = ['A','B','C','D','E','F']
    A = 0
    B = 0
    C = 0
    D = 0
    E = 0
    F = 0
    for student_id in marks_dict:
        student_marks = float(marks_dict[student_id])
        if student_marks >= 90:
            A = A +1
        elif student_marks >= 80:
            B = B +1
        elif student_marks >= 70:
            C = C + 1
        elif student_marks >= 60:
            D = D + 1
        elif student_marks >= 50:
            E = E +1
        else:
            F = F + 1
    student_grade_count_list = [A,B,C,D,E,F]
    #new_row = {'Student Id':student_id_list,'Grade':student_grade_list}
    #############Histogram##############
    #for i in range(len(student_grade_list)):
    #    j = student_grade_count_list[i]
    #    to_print = ""
    #    while j > 0:
    #        to_print += "-"
    #        j = j - 1
    #    print(student_grade_list[i] + " " + to_print)
    ###################################################
    #############Plotext#####################
    #plt.bar(student_grade_list, student_grade_count_list)
    #plt.title("Course Histogram")
    #plt.show()
    ################################################

    plt.title("Course Histogram")
    
    # Setting the background color of the plot
    # using set_facecolor() method
    plt.bar(student_grade_list, student_grade_count_list)
    plt.show()
def create_dummy_course():
    new_row={'Course ID':['COO1'],'Name':['Python Programming'], 'Marks Obtained':[{'CSC103':90}]}
    new_df = pd.DataFrame(new_row)
    new_df.to_csv(os.path.join(DATA_DIR,'course.csv'),index=False)

def process_course():
    create_course_menu()
    course_choice = input('Enter Your Choice: ')
    while not course_choice == '0':
        if course_choice == '1':
            display_course()
        elif course_choice == '2':
            create_course()
        elif course_choice == '3':
            show_course_performance()
        elif course_choice == '4':
            show_course_histogram()
        create_course_menu()
        course_choice = input('Enter Your Choice: ')

def create_course_menu():
    console.print('[yellow][bold]To Display Course Details Press:[/] 1[/]')
    console.print('[yellow][bold]To Add a Course:[/] 2[/]')
    console.print('[yellow][bold]To View Performance of a Course Press:[/] 3[/]')
    console.print('[yellow][bold]To View Histogram of a Course Press:[/] 4[/]')
    console.print('[yellow][bold]To Go To Main Menu  Press:[/] 0[/]')
