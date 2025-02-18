from django.db import models

# Create your models here.
class Student_details(models.Model):
	fname=models.CharField(max_length=40)
	lname=models.CharField(max_length=40)
	reg_no=models.CharField(max_length=55,unique=True)
	dept=models.CharField(max_length=10)
	pw=models.CharField(max_length=40)

class teacher_details(models.Model):
	fname=models.CharField(max_length=40)
	lname=models.CharField(max_length=40)
	f_code=models.IntegerField(unique=True)
	subject=models.CharField(max_length=20)
	dept=models.CharField(max_length=20)
	username=models.CharField(max_length=20,unique=True)
	pw=models.CharField(max_length=40)

class courses(models.Model):
	course_id=models.CharField(max_length=6)
	cname=models.CharField(max_length=20)
	dept=models.CharField(max_length=20)

class st_map_details(models.Model):
	s_id=models.IntegerField(unique=True)
	t_list=models.CharField(max_length=50)

class marks(models.Model):
	s_id=models.IntegerField()
	course_id=models.CharField(max_length=6)
	cla1_marks=models.IntegerField()
	cla2_marks=models.IntegerField()
	mid1_marks=models.IntegerField()
	mid2_marks=models.IntegerField()
	endsem_marks=models.IntegerField()

class results(models.Model):
	s_id=models.IntegerField()
	course_id=models.CharField(max_length=6)
	percentage=models.IntegerField()
	total_marks = models.IntegerField()  


class gpa(models.Model):
	s_id=models.IntegerField()
	final_score=models.IntegerField()
	gpa=models.DecimalField(max_digits=4,decimal_places=2)

