import math

from django.shortcuts import render , redirect

from django.http import HttpResponse
from django.template.defaultfilters import register

from carport import models
from carport.models import LoginForm , AppointmentForm


def index(request):
	if not request.session.get('is_login'):
		return redirect('/carport/login')
	return HttpResponse("Hello, world. You're at the polls index.")


def login(request):
	request.session.flush()
	request.session['current_page'] = ''
	request.session['previous_page'] = 'x'
	if request.method == "POST":
		login_form = LoginForm(request.POST)
		message = "检查填写内容！"
		if login_form.is_valid():
			phone = login_form.cleaned_data['phone']
			password = login_form.cleaned_data['password']
			try:
				user = models.User.objects.get(phone = phone)
				if user.password == password:
					request.session['is_login'] = True
					request.session['user_id'] = user.id
					request.session['user_name'] = user.name
					return redirect('/carport/appointment')
				else:
					message = "密码不正确！"
			except:
				message = "该用户不存在！"
		return render(request, 'carport/login.html', locals())

	login_form = LoginForm()
	return render(request, 'carport/login.html', locals())


def logout(request):
	request.session.flush()
	return redirect('/carport/login')


def appointment(request):
	if not request.session.get('is_login'):
		return redirect('/carport/login')
	if request.method == "GET":
		appointment_message = ""
		appointment_form = AppointmentForm(request.GET)
		request.session['previous_page'] = request.session['current_page']
		request.session['current_page'] = 'appointment'
		return render(request, 'carport/appointment.html', locals())
	# elif request.method == "POST":


def inquiry(request):
	appointment_message = "检查填写内容！"
	appointment_form = AppointmentForm(request.GET)
	if appointment_form.is_valid():
		car_license = appointment_form.cleaned_data['car_license']
		begin_time = appointment_form.cleaned_data['begin_time']
		end_time = appointment_form.cleaned_data['end_time']
		diff = date_diff(begin_time, end_time)
		temp = math.floor(diff)
		print(end_time-begin_time)
		print(diff)
		print(temp)
		if diff > temp:
			appointment_form.total = get_price(temp+1)
		elif diff == temp:
			appointment_form.total = get_price(temp)
	return render(request, 'carport/appointment.html', locals())


def order(request):
	order_message = "x"
	user_id = request.session['user_id']
	order_list = models.Order.objects.filter(carport_customer_id = user_id)

	request.session['previous_page'] = request.session['current_page']
	request.session['current_page'] = 'order'
	return render(request, 'carport/order.html', locals())


def finish(request):
	print(request.GET)
	return HttpResponse("Hello, world. You're at the polls index.")


def date_diff(begin_time, end_time):
	diff = end_time - begin_time
	diff_str = str(diff)
	if diff_str.find(' days, ') > 0:
		d = int(diff_str.split(' days, ')[0])
		h = diff.seconds/60/60
		return d*24+h
	elif diff_str.find(' day, ') > 0:
		h = diff.seconds / 60 / 60
		return 24 + h
	else:
		h = diff.seconds/60/60
		return h


def get_price(time):
	table = {1: 2, 5: 5, 24: 10}
	over_day = (int(time / 24)) * 10
	inner_day = 0
	for i in table:
		if (int(time % 24)) < i:
			inner_day = table[i]
			break
	return over_day + inner_day


@register.filter(name='displayName')
def displayName(value, arg):
	return eval('value.get_'+arg+'_display()')#eval字符串方法了解一下

