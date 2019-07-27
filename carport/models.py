from django.db import models
from django import forms


class User(models.Model):
	# gender = (
	# 	('male', '男'),
	# 	('female', '女'),
	# )

	# id = models.IntegerField(primary_key = True, db_column = 'Fld')
	name = models.CharField(max_length = 200)
	phone = models.CharField(primary_key = True, max_length = 200)
	password = models.CharField(max_length = 200)
	remain = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
	credit = models.DecimalField(max_digits = 10, decimal_places = 2, default = 5.0)

	def __str__(self):
		return '%s , %s' % (self.name, self.phone)


class Carport(models.Model):
	site = models.CharField(primary_key = True, max_length = 200)
	current_car_license = models.CharField(max_length = 200, default = '')
	owner_phone = models.CharField(max_length = 200)

	def __str__(self):
		if self.current_car_license != '':
			return '车位 %s ，%s 正在使用' % (self.site, self.current_car_license)
		return '车位 %s ，空闲' % self.site


#车位与车位主人所拥有的车辆的关系，用于车位推荐算法
class Link(models.Model):
	id = models.IntegerField(primary_key = True, db_column = 'Fld')
	carport_site = models.CharField(max_length = 200)
	car_license = models.CharField(max_length = 200)
	owner_phone = models.CharField(max_length = 200)


class Record(models.Model):
	id = models.AutoField(primary_key = True)
	car_license = models.CharField(max_length = 200)
	type = models.CharField(max_length = 200)
	local = models.CharField(max_length = 200)
	account = models.DecimalField(max_digits = 10, decimal_places = 2)
	total_time = models.DecimalField(max_digits = 10, decimal_places = 2)
	begin_time = models.DateTimeField()
	end_time = models.DateTimeField()
	weekday = models.IntegerField()
	group = models.IntegerField()
	carport_site = models.CharField(max_length = 10)
	begin_hours = models.DateTimeField()
	end_hours = models.DateTimeField()



	def __str__(self):
		return '%s , %s' % (self.id, self.car_license)


class Order(models.Model):
	status_list = (
		('negotiate', '协商中'),
		('success', '进行中'),
		('warning', '已结束'),
		('active', '已撤销'),
		('danger', '超时'),
		('invalid' , '无效订单') ,
	)
	id = models.AutoField(primary_key = True)
	carport_owner = models.ForeignKey(User, related_name = '+', on_delete = models.CASCADE)
	carport_customer = models.ForeignKey(User, related_name = '+', on_delete = models.CASCADE)
	car_license = models.CharField(max_length = 200)
	carport_site = models.CharField(max_length = 200)
	create_time = models.DateTimeField()
	begin_time = models.DateTimeField()
	end_time = models.DateTimeField()
	amount = models.DecimalField(max_digits = 10, decimal_places = 2)
	status = models.CharField(max_length = 10, choices = status_list)

	def __str__(self):
		return '%s 与 %s -- %s' % (self.carport_customer.name, self.carport_owner.name, self.create_time)


#协商列表
class Negotiation(models.Model):
	id = models.AutoField(primary_key = True)
	customer_phone = models.CharField(max_length = 200)
	last_site = models.CharField(max_length = 200)
	begin_site = models.CharField(max_length = 200)
	negotiate_list = models.CharField(max_length = 1000)
	record_time = models.DateTimeField()
	# underway--进行中, end--结束
	status = models.CharField(max_length = 20, default = 'underway')


class AvailCarport(models.Model):
	carport_site = models.CharField(primary_key = True,max_length = 200)
	begin_time = models.DateTimeField()
	end_time = models.DateTimeField()
	owner_phone = models.CharField(max_length = 200)


class Inform(models.Model):
	status_list = (
		('success' , '进行中') ,
		('warning' , '已接受') ,
		('active' , '超时/已拒绝') ,
		('danger' , '协商失败') ,
	)
	id = models.IntegerField(primary_key = True , db_column = 'Fld')
	belong_phone = models.CharField(max_length = 200)
	message = models.CharField(max_length = 200)
	create_time = models.DateTimeField()
	status = models.CharField(max_length = 10 , choices = status_list)
	order = models.ForeignKey(Order, related_name = '+', on_delete = models.CASCADE)
	negotiate_id = models.CharField(max_length = 200)


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
		attrs = {'class': 'form-control'}))
	end_time = forms.DateTimeField(widget = forms.TextInput(
		attrs = {'class': 'form-control'}))




