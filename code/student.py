import pandas as pd
import os
from rich.console import Console
from rich.table import Table
from common import get_dir
import ast
import numpy as np
console = Console()
DATA_DIR=get_dir()

def display_student():
    student_df = pd.read_csv(os.path.join(DATA_DIR,'student.csv'))
    table = Table(title="Student Table")
    table.add_column("Student ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Class Roll Number", style="blue", no_wrap=True)
    table.add_column("Batch", style="green")
    for i in range(len(student_df)):
        student_id = student_df.at[i,'Student Id']
        student_name = student_df.at[i,'Name']
        roll_number = student_df.at[i,'Class Roll Number']
        batch = student_df.at[i,'Batch Name']
        table.add_row(student_id,student_name,str(roll_number),batch)
    console.print(table)
    #print(student_df)
def search_student(student_id):
    student_df = pd.read_csv(os.path.join(DATA_DIR,'student.csv'))
    student_mask = student_df['Student Id'] == student_id
    student_pos = np.flatnonzero(student_mask)
    if len(student_pos) > 0:
        return student_pos[0]
    else:
        return -1



def update_student():
    student_df = pd.read_csv(os.path.join(DATA_DIR,'student.csv'))
    student_id = input('Student Id: ')
    index_number = search_student(student_id)
    while not index_number >= 0:
        print("Student does not exist, please reenter")
        student_id = input('Student Id: ')
        index_number = search_student(student_id)
    student_name = input('Student Name: ')
    student_roll = str(input('Class Roll Number: '))
    student_batch = input('Batch: ')
    student_df.at[index_number,'Student Id'] = student_id
    student_df.at[index_number,'Name'] = student_name
    student_df.at[index_number,'Class Roll Number'] = student_roll
    student_df.at[index_number,'Batch Name'] = student_batch
    student_df.to_csv(os.path.join(DATA_DIR,'student.csv'),index=False)
def delete_student():
    student_df = pd.read_csv(os.path.join(DATA_DIR,'student.csv'))
    student_id = input('Student Id: ')
    index_number = search_student(student_id)
    while not index_number >= 0:
        print("Student does not exist, please reenter")
        student_id = input('Student Id: ')
        index_number = search_student(student_id)
    new_df = student_df.drop(index_number)
    new_df.to_csv(os.path.join(DATA_DIR,'student.csv'),index=False)
def show_student_result():
    student_id = input('Student Id: ')
    index_number = search_student(student_id)
    while not index_number >= 0:
        print("Student does not exist, please reenter")
        student_id = input('Student Id: ')
        index_number = search_student(student_id)
    course_df = pd.read_csv(os.path.join(DATA_DIR,'course.csv'))
    table = Table(title="Student Performance")
    table.add_column("Course Name", style="cyan", no_wrap=True)
    table.add_column("Grade", style="magenta")
    for i in range(len(course_df)):
        course_name = course_df.at[i,'Name']
        marks_dict = ast.literal_eval(course_df.at[i,'Marks Obtained'])
        grade = ''
        if student_id in marks_dict:
            student_marks = float(marks_dict[student_id])
            if student_marks >= 90:
                grade = 'A'
            elif student_marks >= 80:
                grade = 'B'
            elif student_marks >= 70:
                grade = 'C'
            elif student_marks >= 60:
                grade = 'D'
            elif student_marks >= 50:
                grade = 'E'
            else:
                grade = 'F'
            table.add_row(course_name,grade)
    console.print(table)


def create_student():
    student_df = pd.read_csv(os.path.join(DATA_DIR,'student.csv'))
    student_id = input('Student Id: ')
    student_name = input('Student Name: ')
    student_roll = input('Class Roll Number: ')
    student_batch = input('Batch: ')
    new_row={'Student Id':[student_id],'Name':[student_name], 'Class Roll Number':[student_roll],'Batch Name':[student_batch]}
    new_df = pd.DataFrame(new_row)
    whole_df = pd.concat([student_df,new_df],ignore_index = True)
    whole_df.to_csv(os.path.join(DATA_DIR,'student.csv'),index=False)
def create_student_menu():
    console.print('[blue][bold]To Display Student Details Press:[/] 1[/]')
    console.print('[blue][bold]To Add a Student:[/] 2[/]')
    console.print('[blue][bold]To Update a Student Press:[/] 3[/]')
    console.print('[blue][bold]To Delete a Student Press:[/] 4[/]')
    console.print('[blue][bold]To Print Result of a Student Press:[/] 5[/]')
    console.print('[blue][bold]To Go To Main Menu  Press:[/] 0[/]')
def process_student():
    create_student_menu()
    student_choice = input('Enter Your Choice: ')
    while not student_choice == '0':
        if student_choice == '1':
            display_student()
        elif student_choice == '2':
            create_student()
        elif student_choice == '3':
            update_student()
        elif student_choice == '4':
            delete_student()
        elif student_choice == '5':
            show_student_result()
        create_student_menu()
        student_choice = input('Enter Your Choice: ')
