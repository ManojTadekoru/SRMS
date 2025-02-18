import os
import sys
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'srms.settings')
import django
django.setup()

# Import your Django models
from App1.models import Student_details, teacher_details, st_map_details, courses

def getSubjects(dept):
    s_list = [ob.cname for ob in courses.objects.filter(dept=dept)]
    return s_list

def assign_teachers_to_unmapped_students():
    # Get all students who are not yet mapped with teachers
    s = Student_details.objects.all()
    for stu in s:
        try:
            # Check if the student is already mapped
            st_map_details.objects.get(s_id=stu.id)
        except st_map_details.DoesNotExist:
            dept = stu.dept
            sub_list = getSubjects(dept)
            teachers_assigned = ''
            
            for sub in sub_list:
                tl = [ob.f_code for ob in teacher_details.objects.filter(subject=sub)]
                if tl:  # Check if teachers are available for the subject
                    tchoice = random.choice(tl)
                    teachers_assigned += str(tchoice) + ','
                else:
                    # If no teacher is available for the subject, you can handle it here
                    # For example, you can assign a default teacher or skip the subject
                    pass
            
            # Update student's teachers_assigned in st_map_details
            st_map_details.objects.create(s_id=stu.id, t_list=teachers_assigned)  

# Call the function to assign teachers to unmapped students
assign_teachers_to_unmapped_students()
print('done')
