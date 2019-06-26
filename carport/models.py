from django.db import models
from django import forms


class User(models.Model):

	# gender = (
	# 	('male', '男'),
	# 	('female', '女'),
	# )

	id = models.IntegerField(primary_key = True, db_column = 'Fld')
	name = models.CharField(max_length = 200)
	# sex = models.CharField(max_length = 32, choices = gender, default = '男')
	phone = models.CharField(max_length = 200)
	# email = models.EmailField(unique = True, default = "")
	password = models.CharField(max_length = 200)
	remain = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
	credit = models.DecimalField(max_digits = 10, decimal_places = 2, default = 5.0)

	def __str__(self):
		return '%s , %s' % (self.id, self.name)


class Carport(models.Model):
	id = models.IntegerField(primary_key = True, db_column = 'Fld')
	site = models.CharField(max_length = 200, default = "")
	owner = models.ForeignKey(User, on_delete = models.CASCADE)
	using = models.CharField(max_length = 10)

	def __str__(self):
		return '%s 属于 %s' % (self.locate, self.user.name)


class Record(models.Model):
	id = models.IntegerField(primary_key = True)
	car_license = models.CharField(max_length = 200)
	type = models.CharField(max_length = 200)
	local = models.CharField(max_length = 200)
	account = models.DecimalField(max_digits = 10, decimal_places = 2)
	total_time = models.CharField(max_length = 200)
	begin_time = models.DateTimeField()
	end_time = models.DateTimeField()

	def __str__(self):
		return '%s , %s' % (self.id, self.car_license)


class Order(models.Model):
	id = models.IntegerField(primary_key = True, db_column = 'Fld')
	carport_owner = models.ForeignKey(User, related_name = '+', on_delete = models.CASCADE)
	carport_customer = models.ForeignKey(User, related_name = '+', on_delete = models.CASCADE)
	car_license = models.CharField(max_length = 200)
	carport = models.CharField(max_length = 200)
	create_time = models.DateTimeField()
	begin_time = models.DateTimeField()
	end_time = models.DateTimeField()
	amount = models.DecimalField(max_digits = 10, decimal_places = 2)

	def __str__(self):
		return '%s 与 %s -- %s' % (self.customer.name, self.owner.name, self.create_time)


class LoginForm(forms.Form):
	phone = forms.CharField(max_length = 128, widget=forms.TextInput(
		attrs={'class': 'form-control', 'placeholder': '电话号码'}))
	password = forms.CharField(max_length = 256, widget = forms.PasswordInput(
		attrs={'class': 'form-control', 'placeholder': '密 码'}))


class AppointmentForm(forms.Form):
	total = 0.0
	car_license = forms.CharField(max_length = 200, widget = forms.TextInput(
		attrs = {'class': 'form-control'}))
	begin_time = forms.DateTimeField(widget = forms.TextInput(
		attrs = {'class': 'form-control', 'id': 'x'}))
	end_time = forms.DateTimeField(widget = forms.TextInput(
		attrs = {'class': 'form-control'}))
