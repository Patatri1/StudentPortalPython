

from rich.console import Console
from rich.markdown import Markdown
from student import *
from course import *
from batch import *
from department import *
from examination import *

console = Console()
MARKDOWN = """
# Welcome to Student Portal
"""
md = Markdown(MARKDOWN)
console.print(md)

def create_main_menu():
    console.print('[green][bold]To Work With Student Data Press:[/] 1[/]')
    console.print('[green][bold]To Work With Course Data Press:[/] 2[/]')
    console.print('[green][bold]To Work With Batch Data Press:[/] 3[/]')
    console.print('[green][bold]To Work With Department Data Press:[/] 4[/]')
    console.print('[green][bold]To Work With Examination Data Press:[/] 5[/]')
    console.print('[green][bold]To Quit Press:[/] 0[/]')

def show_main_menu():
    create_main_menu()
    choice = input('Enter Your Choice: ')
    while not choice == '0':
        if choice == '1':
            process_student()
        elif choice == '2':
            process_course()
        elif choice == '3':
            process_batch()
        elif choice == '4':
            process_department()
        elif choice == '5':
            process_exam()
        create_main_menu()
        choice = input('Enter Your Choice: ')        

if __name__ == "__main__":
    show_main_menu()



