from django.shortcuts import render,redirect
from django.db import IntegrityError
from App1.models import *
from django.http import HttpResponse
from django.contrib import messages
import sqlite3
import string
import random
# Create your views here.
import random
import string
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
result_published=0

def treg(request):
	subjects = {
    'CSE': ['C', 'C++', 'Python', 'Software Engineering', 'Machine Learning'],
    'ECE': ['Electromagnetic Field Theory', 'Basic Electrical Engineering', 'Linear Integrated Circuits'],
    'EEE': ['Electromagnetic Field Theory', 'Basic Electrical Engineering', 'Linear Integrated Circuits'],
    'MECH': ['Mechanics', 'Dynamics', 'Thermodynamics', 'Materials Science'],
    'CIVIL': ['Surveying', 'Building Materials and Construction', 'Engineering Geology'],
    'IT': ['Digital Principles', 'Operating Systems', 'Database Management Systems']
}
	department_names=subjects.keys()
	if request.method=='POST':
		fname=request.POST.get('fn')
		lname=request.POST.get('ln')
		f_code=request.POST.get('fc')
		dept=request.POST.get('dept')
		sub=request.POST.get('subject')
		un=request.POST.get('un')
		pw=request.POST.get('pw')
		try:
			teacher_details.objects.create(fname=fname,lname=lname,f_code=f_code,dept=dept,subject=sub,username=un,pw=pw)
			error='teacher created successfully'
			return render(request,'treg.html',{'error':error,'department_names':department_names,'subjects':subjects})
		except:
			error='Faculty code or username already taken'
			return render(request,'treg.html',{'error':error,'department_names':department_names,'subjects':subjects})
	
	return render(request,'treg.html',{'department_names':department_names,'subjects':subjects})
def abase(request):
	return render(request,'abase.html')
def alogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pw = request.POST.get('pw')
        try:
            random_pw = request.session['random_pw']
            pw_used = request.session.get('pw_used', False)
            if pw == random_pw and not pw_used and username=='a*d(m)&i^n@':
                #ob=admin_details.objects.get(username=username)
                print('ok')
                del request.session['random_pw']
                request.session['pw_used'] = True
                msg = 'Login successful'
                return redirect('http://127.0.0.1:8000/abase/')
            else:
                print('not ok')
                msg = 'Invalid credentials'
        except KeyError:
            msg = 'Session expired reload page to get the password again'
        return render(request, 'adminlogin.html', {'msg': msg})
    
    random_pw = ''.join(random.choices(string.ascii_letters, k=6)) + ''.join(random.choices(string.digits, k=5))
    m='Code : '+random_pw
    t='abhignamattay@gmail.com'
    sbj='ONE-TIME LOGIN CODE FOR SRMS'
    b=send_mail(sbj,m,t,['asrms261@gmail.com'])
    request.session['random_pw'] = random_pw  # Save the random_pw in session to access it in subsequent requests
    request.session.pop('pw_used', None)  # Remove pw_used flag to ensure it starts fresh for each login attempt
    print(random_pw)
    return render(request, 'adminlogin.html')

def thome(request,id):
	ob=teacher_details.objects.get(id=id)
	return render(request,'thome.html',{'id':id,'ob':ob})
def tlogin(request):
	if request.method=="POST":
		username=request.POST.get('username')
		pw=request.POST.get('pw')
		print(username,pw)
		try:
			ob=teacher_details.objects.get(username=username,pw=pw)
			print("Login successful")
			msg="Login successful"
			return redirect('http://127.0.0.1:8000/thome/'+str(ob.id))
		except:
			print("invalid credentials")
			msg='invalid credentials'
			return render(request,'tlogin.html',{'msg':msg})
	return render(request,'tlogin.html')
def home(request):
	return render(request,'home.html')
def role(request):
	return render(request,'role.html')
def shome(request,id):
	ob=Student_details.objects.get(id=id)
	return render(request,'shome.html',{'id':id,'ob':ob})
def schedule(request, id):
    ob=Student_details.objects.get(id=id)
    # Retrieve all courses of the student with id 'id'
    marks_list=marks.objects.filter(s_id=id)
    d={}
    for i in marks_list:
        d[i.course_id]=i.cla1_marks+i.cla2_marks+i.mid1_marks+i.mid2_marks
    from collections import OrderedDict
    import numpy as np
    keys = list(d.keys())
    values = list(d.values())
    sorted_value_index = np.argsort(values)
    sorted_marks = {keys[i]: values[i] for i in sorted_value_index}
    hmc = list(sorted_marks)[-1]
    hmv = sorted_marks[hmc]
    lmc = list(sorted_marks)[0]
    lmv = sorted_marks[lmc]
    print(sorted_marks)
    mid1vsmid2={}
    for i in marks_list:
    	mid1vsmid2[i.course_id]=[courses.objects.get(course_id=i.course_id).cname,i.mid1_marks,i.mid2_marks]
    	if i.mid1_marks>i.mid2_marks:
    		p=((i.mid1_marks-i.mid2_marks)/i.mid1_marks)*100
    		p=round(p,3)
    		print(p)
    		mid1vsmid2[i.course_id].append(str(p)+'% decrease in the score')
    	elif i.mid1_marks<i.mid2_marks:
    		p=((i.mid2_marks-i.mid1_marks)/i.mid2_marks)*100
    		p=round(p,3)
    		mid1vsmid2[i.course_id].append(str(p)+'% increase in the score')
    	else:
    		mid1vsmid2[i.course_id].append('No increase or decrease in the score')
    print(mid1vsmid2)
    return render(request, 'schedule.html',{'id':id,'ob':ob,'hmc':hmc,'lmc':lmc,'hmv':hmv,'lmv':lmv,'mid1vsmid2':mid1vsmid2})

from django.shortcuts import render, get_object_or_404
import sqlite3

def e_reg(request, id):
    ob = get_object_or_404(Student_details, id=id)
    subjects = courses.objects.filter(dept=ob.dept)
    
    if request.method == 'POST':
        try:
            conn = sqlite3.connect(r"C:\Users\ABHIGNA\Desktop\srms\srms\db.sqlite3")
            cursor = conn.cursor()

            # Check if the student is already registered
            cursor.execute("SELECT id FROM examreg WHERE id=?", (id,))
            existing_registration = cursor.fetchone()
            if existing_registration:
                error = 'You are already registered for the exam.'
            else:
                # If not registered, register the student
                cursor.execute("INSERT INTO examreg (id, status) VALUES (?, ?)", (id, 1))
                conn.commit()
                error = 'Successfully registered for the exam.'

            conn.close()
            return render(request, 'exam-reg.html', {'error': error, 'id': id, 'ob': ob, 'subjects': subjects})
        
        except Exception as e:
            print(e)
            error = 'An error occurred while registering. Please try again.'
            return render(request, 'exam-reg.html', {'error': error, 'id': id, 'ob': ob, 'subjects': subjects})
    
    return render(request, 'exam-reg.html', {'id': id, 'ob': ob, 'subjects': subjects})

def im(request,id):
	ob=Student_details.objects.get(id=id)
	ml=marks.objects.filter(s_id=id)
	return render(request,'im.html',{'id':id,'ob':ob,'ml':ml})
def eim(request,id):
	ob=Student_details.objects.get(id=id)
	return render(request,'schedule.html',{'id':id,'ob':ob})
def sr(request,id):
	global result_published
	if result_published==1:
		ob=Student_details.objects.get(id=id)
		ml=marks.objects.filter(s_id=id)
		percentage_list=[]
		for m in ml:
			try:
				p=results.objects.get(s_id=id,course_id=m.course_id)
				percentage_list.append(p)
			except:
				continue
		l=zip(ml,percentage_list)
		return render(request,'sem_res.html',{'id':id,'ob':ob,'l':l})
	else:
		return redirect('http://127.0.0.1:8000/notfound/')
def login(request):
	if request.method=="POST":
		rno=request.POST.get('rno')
		pw=request.POST.get('pw')
		try:
			ob=Student_details.objects.get(reg_no=rno,pw=pw)
			print("Login successful")
			msg="Login successful"
			return redirect('http://127.0.0.1:8000/shome/'+str(ob.id))
		except:
			print("invalid credentials")
			msg='invalid credentials'
			return render(request,'login.html',{'msg':msg})
	return render(request,'login.html')

def getSubjects(dept):
	s_list=[ob.cname for ob in courses.objects.filter(dept=dept)]
	return s_list
def sreg(request):
	subjects = {
    'CSE': ['C', 'C++', 'Python', 'Software Engineering', 'Machine Learning'],
    'ECE': ['Electromagnetic Field Theory', 'Basic Electrical Engineering', 'Linear Integrated Circuits'],
    'EEE': ['Electromagnetic Field Theory', 'Basic Electrical Engineering', 'Linear Integrated Circuits'],
    'MECH': ['Mechanics', 'Dynamics', 'Thermodynamics', 'Materials Science'],
    'CIVIL': ['Surveying', 'Building Materials and Construction', 'Engineering Geology'],
    'IT': ['Digital Principles', 'Operating Systems', 'Database Management Systems']
}
	error=None
	department_names = subjects.keys()
	if request.method=="POST":
		fname=request.POST.get('fn')
		lname=request.POST.get('ln')
		dept=request.POST.get('dept')
		reg_no=request.POST.get('rno')
		pw=request.POST.get('pw')
		try:
			sub_list=getSubjects(dept)
			teachers_assigned=''
			for sub in sub_list:
				tl=[ob.f_code for ob in teacher_details.objects.filter(subject=sub)]
				tchoice=random.choice(tl)
				teachers_assigned=teachers_assigned+str(tchoice)+','
			Student_details.objects.create(fname=fname,lname=lname,reg_no=reg_no,dept=dept,pw=pw)
			ob=Student_details.objects.get(reg_no=reg_no)
			st_map_details.objects.create(s_id=ob.id,t_list=teachers_assigned)
			msg='registration successful go to login page for login'
			print(msg)
			return redirect('http://127.0.0.1:8000/login/')
		except IntegrityError:
			print("username already taken")
			error='username already taken'
			return render(request,'student_register.html',{'error':error,'department_names': department_names})
	return render(request, 'student_register.html', {'department_names': department_names})


def marks_entry(request, id):
    if request.method == 'POST':
        try:
            t=teacher_details.objects.get(id=id)
            course_id = courses.objects.get(cname=t.subject).course_id
            
            # Loop through each student's marks submitted in the form
            for key, value in request.POST.items():
                if key.startswith('cla1_marks_'):  # Check if the field is for CLA 1 marks
                    stu_id = key.split('_')[-1]  # Extract student ID from the key
                    
                    # Get raw input values
                    cla1_marks = int(request.POST.get('cla1_marks_' + stu_id))
                    cla2_marks = int(request.POST.get('cla2_marks_' + stu_id))
                    mid1_marks = int(request.POST.get('mid1_marks_' + stu_id))
                    mid2_marks = int(request.POST.get('mid2_marks_' + stu_id))
                    endsem_marks = int(request.POST.get('endsem_marks_' + stu_id))
                    
                    # Create or update marks for the student and course
                    marks.objects.update_or_create(
                        s_id=int(stu_id),
                        course_id=course_id,
                        defaults={
                            'cla1_marks': cla1_marks,
                            'cla2_marks': cla2_marks,
                            'mid1_marks': mid1_marks,
                            'mid2_marks': mid2_marks,
                            'endsem_marks': endsem_marks
                        }
                    )
                    messages.success(request, 'Marks updated successfully!')
        except Exception as e:
            # Handle other exceptions
            print("Error:", e)  # Print error message

    
    teacher = teacher_details.objects.get(pk=id)
    fc = teacher.f_code
    cid=courses.objects.get(cname=teacher.subject).course_id
    print(cid)
    students = st_map_details.objects.filter(t_list__contains=str(fc))  # Filter students by teacher's code
    sl = []
    ml=[]
    for student in students:
        sl.append(Student_details.objects.get(id=student.s_id))
        try:
        	ml.append(marks.objects.get(s_id=student.s_id,course_id=cid))
        except:
        	marks.objects.create(s_id=student.s_id,course_id=cid,cla1_marks=0,cla2_marks=0,mid1_marks=0,mid2_marks=0,endsem_marks=0)
        	ml.append(marks.objects.get(s_id=student.s_id,course_id=cid))
    print(ml)
    zl = zip(sl,ml)
    ob=teacher
    return render(request, 'marks_entry.html', {'zl':zl,'id':id,'ob':ob})

def cp(request,id):
	opw=Student_details.objects.get(id=id).pw
	ob=Student_details.objects.get(id=id)
	if request.method=='POST':
		npw=request.POST.get('npw')
		rnpw=request.POST.get('rnpw')
		if npw==rnpw:
			ob=Student_details.objects.get(id=id)
			ob.pw=npw 
			ob.save()
			return redirect('http://127.0.0.1:8000/login/')
		else:
			msg='passwords do not match'
			return render(request,'cp.html',{'opw':opw,'msg':msg,'id':id,'ob':ob})
	
	return render(request,'cp.html',{'opw':opw,'id':id,'ob':ob})


def reports(request,id):
	global result_published
	if result_published==1:
	    teacher_id = id
	    t=teacher_details.objects.get(id=id)
	    allocated_students = st_map_details.objects.filter(t_list__contains=str(t.f_code))
	    print(allocated_students)
	    student_ids = [entry.s_id for entry in allocated_students]
	    print(student_ids)
	    student_marks=[]
	    student_results=[]
	    for ob in marks.objects.filter(course_id=courses.objects.get(cname=t.subject).course_id):
	        if ob.s_id in student_ids:
	        	student_marks.append(ob)
	    print(student_marks)
	    for ob in results.objects.filter(course_id=courses.objects.get(cname=t.subject).course_id):
	    	if ob.s_id in student_ids:
	    		student_results.append(ob)

	    c1avg=sum([mark.cla1_marks for mark in student_marks])/len(student_marks)
	    c2avg=sum([mark.cla2_marks for mark in student_marks])/len(student_marks)
	    m1avg=sum([mark.mid1_marks for mark in student_marks])/len(student_marks)
	    m2avg=sum([mark.mid2_marks for mark in student_marks])/len(student_marks)
	    sem_avg=sum([mark.endsem_marks for mark in student_marks])/len(student_marks)

	    maxc1marks = max([mark.cla1_marks for mark in student_marks])
	    maxc2marks = max([mark.cla2_marks for mark in student_marks])
	    maxm1marks = max([mark.mid1_marks for mark in student_marks])
	    maxm2marks = max([mark.mid2_marks for mark in student_marks])
	    maxesmarks = max([mark.endsem_marks for mark in student_marks])

	    maxc1students = Student_details.objects.filter(id__in=[mark.s_id for mark in student_marks if mark.cla1_marks == maxc1marks])
	    maxc2students = Student_details.objects.filter(id__in=[mark.s_id for mark in student_marks if mark.cla2_marks == maxc2marks])
	    maxm1students = Student_details.objects.filter(id__in=[mark.s_id for mark in student_marks if mark.mid1_marks == maxm1marks])
	    maxm2students = Student_details.objects.filter(id__in=[mark.s_id for mark in student_marks if mark.mid2_marks == maxm2marks])
	    maxesstudents = Student_details.objects.filter(id__in=[mark.s_id for mark in student_marks if mark.endsem_marks == maxesmarks])

	    maxc1student_names = [student.fname + ' ' + student.lname for student in maxc1students]
	    maxc2student_names = [student.fname + ' ' + student.lname for student in maxc2students]
	    maxm1student_names = [student.fname + ' ' + student.lname for student in maxm1students]
	    maxm2student_names = [student.fname + ' ' + student.lname for student in maxm2students]
	    maxesstudent_names = [student.fname + ' ' + student.lname for student in maxesstudents]

	    results_counts = {
	    '90-100%': 0,
	    '80-89%': 0,
	    '70-79%': 0,
	    '60-69%': 0,
	    '50-59%': 0,
	    '40-49%': 0,
	    '30-39%': 0,
	    '20-29%': 0,
	    '10-19%': 0,
	    '0-9%': 0
	}

	    for res in student_results:
	        percentage = res.percentage
	    
	        if 90 <= percentage <= 100:
	            results_counts['90-100%'] += 1
	        elif 80 <= percentage < 90:
	            results_counts['80-89%'] += 1
	        elif 70 <= percentage < 80:
	            results_counts['70-79%'] += 1
	        elif 60 <= percentage < 70:
	            results_counts['60-69%'] += 1
	        elif 50 <= percentage < 60:
	            results_counts['50-59%'] += 1
	        elif 40 <= percentage < 50:
	            results_counts['40-49%'] += 1
	        elif 30 <= percentage < 40:
	            results_counts['30-39%'] += 1
	        elif 20 <= percentage < 30:
	            results_counts['20-29%'] += 1
	        elif 10 <= percentage < 20:
	            results_counts['10-19%'] += 1
	        elif percentage < 10:
	            results_counts['0-9%'] += 1

	    marks_counts = {
	    '250-300': 0,
	    '200-249': 0,
	    '150-199': 0,
	    '100-149': 0,
	    '50-99': 0,
	    '0-49': 0
	}

	    for res in student_results:
	        total_marks = res.total_marks
	    
	        if 250 <= total_marks <= 300:
	            marks_counts['250-300'] += 1
	        elif 200 <= total_marks < 250:
	            marks_counts['200-249'] += 1
	        elif 150 <= total_marks < 200:
	            marks_counts['150-199'] += 1
	        elif 100 <= total_marks < 150:
	            marks_counts['100-149'] += 1
	        elif 50 <= total_marks < 100:
	            marks_counts['50-99'] += 1
	        elif total_marks < 50:
	            marks_counts['0-49'] += 1
	    print(results_counts)
	    ob=teacher_details.objects.get(id=id)
	    context = {
	    'results_counts': results_counts,
	    'marks_counts': marks_counts,
	    'c1avg': c1avg,
	    'c2avg': c2avg,
	    'm1avg': m1avg,
	    'm2avg': m2avg,
	    'sem_avg': sem_avg,
	    'maxc1marks': maxc1marks,
	    'maxc2marks': maxc2marks,
	    'maxm1marks': maxm1marks,
	    'maxm2marks': maxm2marks,
	    'maxesmarks': maxesmarks,
	    'maxc1student_names': maxc1student_names,
	    'maxc2student_names': maxc2student_names,
	    'maxm1student_names': maxm1student_names,
	    'maxm2student_names': maxm2student_names,
	    'maxesstudent_names': maxesstudent_names,
	    'id':teacher_id,
	    'ob':ob
	}


	    return render(request, 'reports.html', context)

	else:
		return redirect('http://127.0.0.1:8000/notfound/')
def smsg(request):
	return render(request,'success-msg.html')
def pr(request):
	if request.method=="POST":
		student_marks=marks.objects.all()
		for mark in student_marks:
			results.objects.update_or_create(course_id=mark.course_id,s_id=mark.s_id,percentage=((mark.cla1_marks+mark.cla2_marks+mark.mid1_marks+mark.mid2_marks+mark.endsem_marks)*100)/300,total_marks=mark.cla1_marks+mark.cla2_marks+mark.mid1_marks+mark.mid2_marks+mark.endsem_marks)
		calculate_cgpa()
		global result_published
		result_published=1
		return redirect('http://127.0.0.1:8000/smsg/')
	return render(request,'pr.html')


def calculate_cgpa():
    grade_points = {
        (810, 900): 10,
        (720, 809): 9,
        (630, 719): 8,
        (540, 629): 7,
        (450, 539): 6,
        (360, 449): 5,
        (270, 359): 4,
        (180, 269): 3,
        (90, 179): 2,
        (0, 89): 1
    }
    d={}
    result_list=results.objects.all()
    for mark in result_list:
        if mark.s_id not in d:
            d[mark.s_id]=[mark.total_marks]
        else:
            d[mark.s_id].append(mark.total_marks)
    for student in d:
        grand_total=sum(d[student])
        total_marks = grand_total
        total_grade_points = 0

        for marks_range, grade_point in grade_points.items():
            if marks_range[0] <= total_marks <= marks_range[1]:
                total_grade_points = grade_point
                print(total_grade_points)
                break

        cgpa = total_grade_points / 10.0
        gpa.objects.update_or_create(s_id=student,gpa=cgpa,final_score=grand_total)

def notfound(request):
	return render(request,'notfound.html')

def npr(request):
	if request.method=='POST':
		global result_published 
		result_published = 0
		return redirect('http://127.0.0.1:8000/cancel-msg/')
	return render(request,'npr.html')

def cmsg(request):
	return render(request,'cmsg.html')