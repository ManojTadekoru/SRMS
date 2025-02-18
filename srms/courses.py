import os
# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'srms.settings')  # Change 'your_project.settings' to your project's settings module

import django
django.setup()

# Now you can import your Django model and proceed with the data insertion
from App1.models import courses

# Dictionary of subjects
subjects = {
    'CSE': ['C', 'C++', 'Python'],
    'ECE': ['Electromagnetic Field Theory', 'Basic Electrical Engineering', 'Linear Integrated Circuits'],
    'EEE': ['Electromagnetic Field Theory', 'Basic Electrical Engineering', 'Linear Integrated Circuits'],
    'MECH': ['Mechanics', 'Dynamics', 'Thermodynamics'],
    'CIVIL': ['Surveying', 'Building Materials and Construction', 'Engineering Geology'],
    'IT': ['Digital Principles', 'Operating Systems', 'Database Management Systems']
}

# Function to generate course_id
def generate_course_id(dept, number):
    return dept + str(number)*3

# Inserting data into the courses table
for dept, courses_list in subjects.items():
    for index, course_name in enumerate(courses_list, start=1):
        course_id = generate_course_id(dept, index)
        # Insert into database
        course = courses(course_id=course_id, cname=course_name, dept=dept)
        course.save()
