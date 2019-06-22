from django.db import models
from django import forms


class User(models.Model):

	gender = (
		('male', '男'),
		('female', '女'),
	)

	id = models.IntegerField(primary_key = True, db_column = 'Fld')
	name = models.CharField(max_length = 200)
	sex = models.CharField(max_length = 32, choices = gender, default = '男')
	phone = models.CharField(max_length = 200)
	email = models.EmailField(unique = True, default = "")
	password = models.CharField(max_length = 200)
	remain = models.FloatField(default = 0.00)
	credit = models.FloatField(default = 5.0)

	def __str__(self):
		return '%s , %s' % (self.id, self.name)


class Carport(models.Model):
	id = models.IntegerField(primary_key = True, db_column = 'Fld')
	locate = models.CharField(max_length = 200, default = "")
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	using = models.CharField(max_length = 10)

	def __str__(self):
		return '%s 属于 %s' % (self.locate, self.user.name)


class LoginForm(forms.Form):
	phone = forms.CharField(max_length = 128, widget=forms.TextInput(
		attrs={'class': 'form-control', 'placeholder': '电话号码'}))
	password = forms.CharField(max_length = 256, widget = forms.PasswordInput(
		attrs={'class': 'form-control', 'placeholder': '密 码'}))
