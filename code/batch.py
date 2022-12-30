import pandas as pd
import os
from rich.console import Console
import numpy as np
import ast
from common import get_dir
from rich.table import Table

console = Console()
DATA_DIR=get_dir()
def search_batch(batch_id):
    batch_df = pd.read_csv(os.path.join(DATA_DIR,'batch.csv'))
    batch_mask = batch_df['Batch ID'] == batch_id
    pos = np.flatnonzero(batch_mask)
    if len(pos) > 0:
        return pos[0]
    else:
        return -1

def create_dummy_batch():
    new_row={'Batch ID':['CSC2022'],'Department Name':['CSE'],'Name':['CSC 2022-2026'], 'List of Courses':[['COO1','COO2']],'List of Students':[['CSC102','CSC103','CSC104','CSC105','CSC106','CSC110']]}
    new_df = pd.DataFrame(new_row)
    new_df.to_csv(os.path.join(DATA_DIR,'batch.csv'),index=False)
def display_batch_students():
    batch_df = pd.read_csv(os.path.join(DATA_DIR,'batch.csv'))
    batch_id = input('Batch ID: ')
    index_number = search_batch(batch_id)
    while not index_number >= 0:
        print("Batch does not exist, please reenter")
        batch_id = input('Batch Id: ')
        index_number = search_batch(batch_id)
    mask = batch_df['Batch ID'] == batch_id
    pos = np.flatnonzero(mask)
    student_list = ast.literal_eval(batch_df.at[pos[0],'List of Students'])
    student_df = pd.read_csv(os.path.join(DATA_DIR,'student.csv'))
    a_df = student_df[student_df['Student Id'].isin(student_list)]
    b_df = a_df.reset_index(drop=True)
    table = Table(title="Batch Students Table")
    table.add_column("Student ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green", no_wrap=True)
    table.add_column("Class Roll Number", style="magenta")
    for i in range(len(b_df)):
        student_id = b_df.at[i,'Student Id']
        student_name = b_df.at[i,'Name']
        student_roll = b_df.at[i,'Class Roll Number']
        table.add_row(student_id,student_name,str(student_roll))
    console.print(table)
    #print(student_df[student_df['Student Id'].isin(student_list)])
def create_batch_menu():
    console.print('[magenta][bold]To Create a Batch Press:[/] 1[/]')
    console.print('[magenta][bold]To Display List of Students Press:[/] 2[/]')
    console.print('[magenta][bold]To Display List of Courses Press:[/] 3[/]')
    console.print('[magenta][bold]To Display Performance of all Students Press:[/] 4[/]')
    console.print('[magenta][bold]To Go To Main Menu  Press:[/] 0[/]')
def display_batch_courses():
    batch_df = pd.read_csv(os.path.join(DATA_DIR,'batch.csv'))
    batch_id = input('Batch ID: ')
    index_number = search_batch(batch_id)
    while not index_number >= 0:
        print("Batch does not exist, please reenter")
        batch_id = input('Batch Id: ')
        index_number = search_batch(batch_id)
    mask = batch_df['Batch ID'] == batch_id
    pos = np.flatnonzero(mask)
    course_list = ast.literal_eval(batch_df.at[pos[0],'List of Courses'])
    course_df = pd.read_csv(os.path.join(DATA_DIR,'course.csv'))
    table = Table(title="Batch Course Table")
    table.add_column("Course ID", style="cyan", no_wrap=True)
    table.add_column("Course Name", style="green", no_wrap=True)
    a_df = course_df[course_df['Course ID'].isin(course_list)].drop(columns=['Marks Obtained'])
    b_df = a_df.reset_index(drop=True)
    for i in range(len(b_df)):
        course_id = b_df.at[i,'Course ID']
        course_name = b_df.at[i,'Name']
        table.add_row(course_id,course_name)
    console.print(table)
    #print(course_df[course_df['Course ID'].isin(course_list)].drop(columns=['Marks Obtained']))
def display_batch_performance():
    batch_df = pd.read_csv(os.path.join(DATA_DIR,'batch.csv'))
    student_df = pd.read_csv(os.path.join(DATA_DIR,'student.csv'))
    course_df = pd.read_csv(os.path.join(DATA_DIR,'course.csv'))
    table = Table(title="Batch Students Perdormance")
    table.add_column("Student ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta", no_wrap=True)
    table.add_column("Class Roll Number", style="blue", no_wrap=True)
    table.add_column("Overall Percentage", justify="right" ,style="green", no_wrap=True)
    batch_id = input('Batch ID: ')
    index_number = search_batch(batch_id)
    while not index_number >= 0:
        print("Batch does not exist, please reenter")
        batch_id = input('Batch Id: ')
        index_number = search_batch(batch_id)
    mask = batch_df['Batch ID'] == batch_id
    pos = np.flatnonzero(mask)
    course_list = ast.literal_eval(batch_df.at[pos[0],'List of Courses'])
    student_list = ast.literal_eval(batch_df.at[pos[0],'List of Students'])
    for student_id in student_list:
        student_mask = student_df['Student Id'] == student_id
        student_pos = np.flatnonzero(student_mask)
        course_count = 0
        marks = 0
        for course_id in course_list:
            course_mask = course_df['Course ID'] == course_id
            course_pos = np.flatnonzero(course_mask)
            course_marks_dict = ast.literal_eval(course_df.at[course_pos[0],'Marks Obtained'])
            if student_id in course_marks_dict:
                course_count = course_count + 1
                marks = marks + float(course_marks_dict[student_id])
        table.add_row(student_id,student_df.at[student_pos[0],'Name'],str(student_df.at[student_pos[0],'Class Roll Number']),str(marks/course_count)+'%')
    console.print(table)

def create_batch():
    batch_df = pd.read_csv(os.path.join(DATA_DIR,'batch.csv'))
    batch_id = input('Batch ID: ')
    batch_name = input('Batch Name: ')
    department_name = input('Department Name: ')
    student_list = []
    print('Enter Student IDs, When Finished Press 0')
    student_id = input('Student ID: ')
    while not student_id == '0':
        student_list.append(student_id)
        student_id = input('Student ID: ')
    course_list = []
    print('Enter Course IDs, When Finished Press 0')
    course_id = input('Course ID: ')
    while not course_id == '0':
        course_list.append(course_id)
        course_id = input('Course ID: ')

    new_row={'Batch ID':[batch_id],'Department Name':[department_name],'Batch Name':[batch_name], 'List of Courses':[course_list],'List of Students':[student_list]}
    new_df = pd.DataFrame(new_row)
    whole_df = pd.concat([batch_df,new_df],ignore_index = True)
    whole_df.to_csv(os.path.join(DATA_DIR,'batch.csv'),index=False)

def process_batch():
    create_batch_menu()
    batch_choice = input('Enter Your Choice: ')
    while not batch_choice == '0':
        if batch_choice == '1':
            create_batch()
        elif batch_choice == '2':
            display_batch_students()
        elif batch_choice == '3':
            display_batch_courses()
        elif batch_choice == '4':
            display_batch_performance()
        create_batch_menu()
        batch_choice = input('Enter Your Choice: ')

