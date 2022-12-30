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
def search_department(department_id):
    dep_df = pd.read_csv(os.path.join(DATA_DIR,'department.csv'))
    dep_mask = dep_df['Department ID'] == department_id
    pos = np.flatnonzero(dep_mask)
    if len(pos) > 0:
        return pos[0]
    else:
        return -1

def create_department_menu():
    console.print('[purple][bold]To Create a Department Press:[/] 1[/]')
    console.print('[purple][bold]To View Batches in a Department Press:[/] 2[/]')
    console.print('[purple][bold]To View Average Percentage Press:[/] 3[/]')
    console.print('[purple][bold]To View Average Percentage Graph Press:[/] 4[/]')
    console.print('[purple][bold]To Go To Main Menu  Press:[/] 0[/]')
def create_department():
    dep_df = pd.read_csv(os.path.join(DATA_DIR,'department.csv'))
    department_id = input('Department ID: ')
    department_name = input('Department Name: ')
    batch_list = []
    print('Enter Batch IDs, When Finished Press 0')
    batch_id = input('Batch ID: ')
    while not batch_id == '0':
        batch_list.append(batch_id)
        batch_id = input('Batch ID: ')
    new_row={'Department ID':[department_id],'Department Name':[department_name], 'List of Batches':[batch_list]}
    new_df = pd.DataFrame(new_row)
    whole_df = pd.concat([dep_df,new_df],ignore_index = True)
    whole_df.to_csv(os.path.join(DATA_DIR,'department.csv'),index=False)
def view_department_batches():
    dep_df = pd.read_csv(os.path.join(DATA_DIR,'department.csv'))
    table = Table(title="Batch Table")
    table.add_column("Batch ID", style="cyan", no_wrap=True)
    department_id = input('Department ID: ')
    index_number = search_department(department_id)
    while not index_number >= 0:
        print("Department does not exist, please reenter")
        department_id = input('Department Id: ')
        index_number = search_department(department_id)
    mask = dep_df['Department ID'] == department_id
    pos = np.flatnonzero(mask)
    batch_list = ast.literal_eval(dep_df.at[pos[0],'List of Batches'])
    for batch_name in batch_list:
        table.add_row(batch_name)
    console.print(table)
def calculate_department_performance():
    dep_df = pd.read_csv(os.path.join(DATA_DIR,'department.csv'))
    batch_df = pd.read_csv(os.path.join(DATA_DIR,'batch.csv'))
    course_df = pd.read_csv(os.path.join(DATA_DIR,'course.csv'))
    department_id = input('Department ID: ')
    index_number = search_department(department_id)
    while not index_number >= 0:
        print("Department does not exist, please reenter")
        department_id = input('Department Id: ')
        index_number = search_department(department_id)
    mask = dep_df['Department ID'] == department_id
    departmentpos = np.flatnonzero(mask)
    batch_list = ast.literal_eval(dep_df.at[departmentpos[0],'List of Batches'])
    batch_percentage_list = []
    for batch_id in batch_list:
        student_percentage = 0
        mask = batch_df['Batch ID'] == batch_id
        pos = np.flatnonzero(mask)
        course_list = ast.literal_eval(batch_df.at[pos[0],'List of Courses'])
        student_list = ast.literal_eval(batch_df.at[pos[0],'List of Students'])
        student_count = 0
        for student_id in student_list:
            student_count = student_count +1
            course_count = 0
            marks = 0
            for course_id in course_list:
                course_mask = course_df['Course ID'] == course_id
                course_pos = np.flatnonzero(course_mask)
                course_marks_dict = ast.literal_eval(course_df.at[course_pos[0],'Marks Obtained'])
                if student_id in course_marks_dict:
                    course_count = course_count + 1
                    marks = marks + float(course_marks_dict[student_id])
            student_avg = marks/course_count
            student_percentage = student_percentage + student_avg
        batch_percentage_list.append(student_percentage/student_count)
    return batch_list,batch_percentage_list
def view_department_performance():
    table = Table(title="Department Performance")
    table.add_column("Batch ID", style="cyan", no_wrap=True)
    table.add_column("Average Percentage", style="green", no_wrap=True)
    batch_list, batch_percentage = calculate_department_performance()
    for i in range(len(batch_list)):
        table.add_row(batch_list[i],str(round(batch_percentage[i],2))+'%')
    console.print(table)
def view_performance_plot():
    batch_list, batch_percentage = calculate_department_performance()
    #plt.title('Department Performance')
    #plt.bar(batch_list,batch_percentage)
    #plt.show()
    plt.title('Department Performance')
    plt.plot(batch_list,batch_percentage)
    plt.show()
def create_dummy_dept():
    new_row={'Department ID':['CSE'],'Department Name':['Computer Science and Engineering'], 'List of Batches':[['CSC2021','CSC2022']]}
    new_df = pd.DataFrame(new_row)
    new_df.to_csv(os.path.join(DATA_DIR,'department.csv'),index=False)

def process_department():
    create_department_menu()
    department_choice = input('Enter Your Choice: ')
    while not department_choice == '0':
        if department_choice == '1':
            create_department()
        elif department_choice == '2':
            view_department_batches()
        elif department_choice == '3':
            view_department_performance()
        elif department_choice == '4':
            view_performance_plot()
        create_department_menu()
        department_choice = input('Enter Your Choice: ')
