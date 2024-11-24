# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using  data classes
# with structured error handling
# Change Log: (Who, When, What)
#   Renato Felicio, 11/16/2024,Created Script
#   Renato Felicio, 11/23/2024, Modified to work with data classes
#   <Your Name Here>,<Date>,<Activity>
# ------------------------------------------------------------------------------------------ #

# Import section
import json
from typing import TextIO

# Global Data Layer

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
# Define the Data Constants

FILE_NAME: str = "Enrollments.json" # Constant holds the name of the file with students data

# Define the Data Variables and constants
students: list=[] # This variable holds the information of all registered students.
menu_choice: str=''  # It holds the user choice.

# Class definition

# Data Class (This section includes person and student data classes)

class Person:
    """
       A class representing person data.

       Properties:
           student_first_name (str): The student's first name.
           student_last_name (str): The student's last name.

       ChangeLog:
           - Renato Felicio, 11/23/2024: Created the class.
       """
    # Constructor for student's first and last name are defined below:
    def __init__(self, student_first_name: str ='', student_last_name: str =''):  # parameters default to empty
        self.student_first_name = student_first_name  # set the attribute using the property to provide validation
        self.student_last_name = student_last_name  # set the attribute using the property to provide validation

    # Getter and Setter Properties for first name are created below
    @property
    def student_first_name(self):
        return self.__student_first_name.title()

    @student_first_name.setter
    def student_first_name(self, value: str):
        if value.isalpha() or value == "": # checks if user input values are alphabetic characters or empty string
            self.__student_first_name = value
        else:
            raise ValueError("The first name should not contain numbers.") # Custom error message

    # Getter and Setter Properties for last name are created below
    @property
    def student_last_name(self):
        return self.__student_last_name.title()  # checks if user input values are alphabetic characters or empty string
    @student_last_name.setter
    def student_last_name(self, value: str):
        if value.isalpha() or value == "": # checks if user input values are alphabetic characters or empty string
            self.__student_last_name = value
        else:
            raise ValueError("The last name should not contain numbers.") # Custom error message
    # Method to extract the comma separate data is presented below, it overrides the __str__() method
    def __str__(self):
        return f"{self.student_first_name},{self.student_last_name}"

# Student class is defined below, and it inherited person class

class Student(Person):
    """
    A class representing student data.

    Properties:
        course_name (str): The course name for the student registration.

    ChangeLog: (Who, When, What)
    Renato Felicio, 11/23/2024,Created Class
    """

    # Constructor for student's course name is defined below:
    def __init__(self, student_first_name: str = '', student_last_name: str = '', course_name: str = ''):
        super().__init__(student_first_name=student_first_name, student_last_name=student_last_name)
        self.course_name = course_name

    # Getter and Setter Properties for course name are created below
    @property
    def course_name(self):
        return self.__course_name

    @course_name.setter
    def course_name(self, value: str):
        self.__course_name = value

    # Method to extract the comma separate data is presented below, it overrides the __str__() method
    def __str__(self):
        return f'{self.student_first_name},{self.student_last_name},{self.course_name}'

# Processing Data Layer
class FileProcessor:
    """
        A collection of processing layer functions that work with json files

        ChangeLog: (Who, When, What)
        Renato Felicio,11/16/2024,Created Class
        Renato Felicio, 11/26/2024, Modified Class to work with list of student objects
        """
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list): # This function reads data from json file
        """ This function reads data from a json file into a list of object rows

            Notes:
            - Data sent to the student_data parameter will be overwritten.

            ChangeLog: (Who, When, What)
            Renato Felicio,11/16/2024,Created function
            Renato Felicio, 11/23/2024,Modified function to work with student data in objects instead of dictionaries

            :param file_name: string with the name of the file we are reading
            :param student_data: list of object rows containing student data
            :return: list of object rows filled with data
        """
        try:
            file : TextIO = open(file_name, "r")  # Open the JSON file for reading
            json_data: list = json.load(file) # File data is loaded into a table of dictionaries
            # Now 'json_data' contains the parsed JSON data as a Python list of dictionaries
            for student in json_data: # This for will convert the student data into a table of objects
                student_object = Student(student_first_name=student["FirstName"],
                                         student_last_name=student["LastName"],
                                         course_name=student["CourseName"])
                student_data.append(student_object)

            file.close()
        except FileNotFoundError as e:  # Handles error in case there is no initial file
            IO.output_error_messages("Data file must exist before running this script!",  e)
            file = open(FILE_NAME, "w")  # Creates an empty initial file, in case of file not found
            IO.output_error_messages("Empty file was created!\n")
        except Exception as e:
            IO.output_error_messages("Error: There was a problem with reading the file.", e)
        finally:
            if file.closed == False:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list): # This function reads data from json file
        """ This function writes data to a json file from a list of object rows

            ChangeLog: (Who, When, What)
            Renato Felicio,11/16/2024,Created function
            Renato Felicio, 11/23/2024, Modified function to work with students objects instead of dictionaries, and
            added type exception error

            :param file_name: string with the name of the file we are writing to
            :param student_data: list of object rows containing student data
            :return: None
        """
        try:
            json_data: list = []
            for student in student_data:  # Converts List of Student objects to list of dictionary rows.
                student_json: dict \
                    = {"FirstName": student.student_first_name,
                       "LastName": student.student_last_name,
                       "CourseName": student.course_name}
                json_data.append(student_json)

            file: TextIO = open(file_name, "w")
            json.dump(json_data, file)  # It writes the list of dictionaries into a json file
            file.close()
        except TypeError as e:
            IO.output_error_messages("Please check that the data is a valid JSON format", e)
        except Exception as e: # It handles any exception that could happen when writing the file
            if file.closed == False:
                file.close()
                IO.output_error_messages("There was a problem with writing to the file.", e)
                IO.output_error_messages("Please check that the file is not open by another program.",e)
                print()
# End of Processing Data Layer

# Presentation Data Layer

class IO:
    """A collection of presentation layer functions that manage user input and output

        ChangeLog: (Who, When, What)
        Renato Felicio,11/16/2024,Created Class
    """
    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays a custom error messages to the user

            ChangeLog: (Who, When, What)
            Renato Felicio,11/16/2024,Created function

            :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

            ChangeLog: (Who, When, What)
            Renato Felicio,11/16/2024,Created function

            :return: None
        """
        print(menu)

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

            ChangeLog: (Who, When, What)
            Renato Felicio,11/16/2024,Created function

            :return: string with the users choice
        """
        choice="0"
        try:
            choice: str = input("What would you like to do: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
               raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message

        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """ This function displays the current data to the user

            ChangeLog: (Who, When, What)
            Renato Felicio,11/16/2024,Created function
            Renato Felicio, 11/23/2024, Modified to work with objects

            :return: None
        """
        # Process the data to create and display a custom message
        print("-" * 50)
        #student_data=
        for student in student_data:
            print(f'Student {student.student_first_name} '
                  f'{student.student_last_name} is enrolled in {student.course_name}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets data from the user and adds it to a list of object rows

            ChangeLog: (Who, When, What)
            Renato Felicio,11/16/2024,Created function
            Renato Felicio, 11/23/2024, Modified function to work with objects instead of dictionaries

            :param student_data: list of dictionary rows containing student current data
            :return: list of object rows filled with a new row of data
        """
        try:
            # Input of data
            student=Student()
            student.student_first_name: str = input("Enter the student's first name: ") # Holds student first name input
            student.student_last_name: str = input("Enter the student's last name: ") # Holds student last name input
            student.course_name: str = input("Please enter the name of the course: ") # Holds course name input
            student_data.append(student)

        except ValueError as e:
            IO.output_error_messages("", e)
        except Exception as e:
            IO.output_error_messages("Error: There was a problem with your entered data.",e)
        return student_data

# End of Presentation Data Layer

# End of class definition

# Start of the main body of the script

# Read data from a file
students:list = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

while (True): # Loops through the menu of options
    # Present the menu of choices
    IO.output_menu(MENU)
    menu_choice=IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students=IO.input_student_data(students)
        continue

    # Present the current data
    elif menu_choice == "2":
        # Process the data to create and display a custom message
        IO.output_student_courses(student_data=students)
        continue

    # Save the data to a file and present to user
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(FILE_NAME,students)
        IO.output_student_courses(students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, or 3")

print("Program Ended")

