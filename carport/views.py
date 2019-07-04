import datetime
import math
from _decimal import Decimal

import decimal
from django.shortcuts import render , redirect

from django.http import HttpResponse
from django.template.defaultfilters import register

from carport import models
from carport.models import LoginForm , AppointmentForm


def index(request):
	if not request.session.get('is_login'):
		return redirect('/carport/login')
	return HttpResponse("Hello, world. You're at the polls index.")


"""
post：登录验证
其他为get，初始化网页并显示
"""
def login(request):
	request.session.flush()
	request.session['current_page'] = ''
	request.session['previous_page'] = ''
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
					request.session['user'] = user
					return redirect('/carport/appointment')
				else:
					message = "密码不正确！"
			except:
				message = "该用户不存在！"
		return render(request, 'carport/login.html', locals())

	login_form = LoginForm()
	return render(request, 'carport/login.html', locals())


#退出登录
def logout(request):
	request.session.flush()
	return HttpResponse('200')


"""
post：直接预约，生成订单
其他为get，初始化网页并显示
"""
def appointment(request):
	if not request.session.get('is_login'):
		return redirect('/carport/login')
	alert_class = ''
	appointment_message = ""
	if request.method == 'POST':
		carport_site = request.POST.get('carport_site')
		car_license = request.session['appointment_car_license']
		begin_time = request.session['appointment_begin_time']
		end_time = request.session['appointment_end_time']
		total = request.session['appointment_total']

		carport = models.Carport.objects.get(site = carport_site)
		owner = models.User.objects.get(phone = carport.owner_phone)
		customer = request.session['user']
		models.Order.objects.create(
			car_license = car_license,
			create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
			begin_time = begin_time,
			end_time = end_time,
			amount = total,
			status = 'success',
			carport_site = carport_site,
			carport_owner = owner,
			carport_customer = customer,
		)
		# models.AvailCarport.objects.get(carport_site = carport_site).delete()
		appointment_message = '预订成功!'
		alert_class = 'alert-success'
		return render(request , 'carport/appointment.html' , locals())

	#以下为get
	appointment_form = AppointmentForm(request.GET)
	request.session['previous_page'] = request.session['current_page']
	request.session['current_page'] = 'appointment'
	return render(request , 'carport/appointment.html' , locals())


#获得此时间段内可选车位
def get_carport_list(begin_time, end_time):
	list = models.AvailCarport.objects.filter(begin_time__lte = begin_time, end_time__gte = end_time)
	return list


"""
post：发出空闲车位的验证
其他为get，初始化网页并显示
"""
def publish(request):
	if not request.session.get('is_login'):
		return redirect('/carport/login')
	publish_message = ''
	user_phone = request.session.get('user').phone
	#提交发布表单
	if request.method == 'POST':
		carport_site = request.POST.get('carport_site')
		begin_time = request.POST.get('begin_time')
		end_time = request.POST.get('end_time')
		if carport_site == ''or begin_time == '' or end_time == '':
			alert_class = 'alert-danger'
			publish_message = '请检查填写信息'
		try:
			old = models.AvailCarport.objects.get(carport_site = carport_site)
			old.delete()
		except:
			pass
		finally:
			models.AvailCarport.objects.create(
				carport_site = carport_site,
				begin_time = begin_time,
				end_time = end_time,
				owner_phone = user_phone,
			)
		alert_class = 'alert-success'
		publish_message = '发布成功!'
		return render(request, 'carport/publish.html', locals())


	carport_site_list = models.Link.objects.filter(owner_phone = user_phone).values_list('carport_site', flat= True)
	request.session['previous_page'] = request.session['current_page']
	request.session['current_page'] = 'publish'
	if carport_site_list.__len__() == 0:
		publish_message = '此账号下无可发布车位'
		return render(request, 'carport/publish.html', locals())
	result_list = []
	for carport_site in carport_site_list:
		if models.Carport.objects.get(site = carport_site).current_car_license == '':
			result_list.append(carport_site)
	if result_list.__len__() == 0:
		publish_message = '此账号下无可发布车位'
	result_list_size = result_list.__len__()
	# if request.method!='POST':
	# 	publish_form = models.PublishForm(result_list)
	return render(request , 'carport/publish.html' , locals())


"""
按时间查询此时间段内被发布的可用车位
"""
def inquiry(request):
	appointment_message = "检查填写内容！"
	alert_class = '	alert-danger'
	appointment_form = AppointmentForm(request.GET)
	carport_list = []
	negotiate_list = []
	if appointment_form.is_valid():
		car_license = appointment_form.cleaned_data['car_license']
		begin_time = appointment_form.cleaned_data['begin_time']
		end_time = appointment_form.cleaned_data['end_time']
		diff = date_diff(begin_time, end_time)
		get_carport_list(begin_time, end_time)
		temp = math.floor(diff)
		if diff > temp:
			appointment_form.total = get_price(temp+1)
		elif diff == temp:
			appointment_form.total = get_price(temp)

		appointment_message = '查询、计价成功！'
		alert_class = 'alert-success'
		carport_list = get_carport_list(begin_time, end_time)
		request.session['appointment_car_license'] = car_license
		request.session['appointment_begin_time'] = begin_time
		request.session['appointment_end_time'] = end_time
		request.session['appointment_total'] = appointment_form.total

	return render(request, 'carport/appointment.html', locals())


"""
返回指定时间内的可协商车位的列表
"""
# def negotiate(begin_time, end_time):
# 	diff = date_diff(begin_time, end_time)
# 	if diff <= 24:



"""
初始化，显示我的订单页面
"""
def order(request):
	order_message = "x"
	user_phone = request.session.get('user').id
	order_list = models.Order.objects.filter(carport_owner_phone = user_phone)

	request.session['previous_page'] = request.session['current_page']
	request.session['current_page'] = 'order'
	return render(request, 'carport/order.html', locals())


"""
在我的订单页面提前终止订单的方法
"""
def finish(request):
	order_id = request.GET.get('order_id')
	this_order = models.Order.objects.get(id = order_id)
	this_order.status = "warning"
	this_order.save()

	order_message = "x"
	user_phone = request.session.get('user').phone
	order_list = models.Order.objects.filter(carport_customer_phone = user_phone)
	return render(request, 'carport/order.html', locals())


"""
在我的订单页面，撤销订单的方法
"""
def cancel(request):
	order_id = request.GET.get ('order_id')
	order = models.Order.objects.get (id=order_id)
	begin_time = order.begin_time
	now = datetime.datetime.now()
	diff = date_diff (now, begin_time)
	user_phone = request.session.get('user').phone
	carport_customer = order.carport_customer
	carport_owner = order.carport_owner
	if diff>1:
		order.status='active'
		order.save()
	elif diff<=1:
		if order.carport_owner.id == user_phone:
			print(1)
			carport_owner.credit -= decimal.Decimal(0.50)
			carport_owner.remain -= decimal.Decimal(order.amount*2)
			carport_customer.remain += decimal.Decimal(order.amount*2)
			order.status = 'active'
			order.save()
			carport_owner.save()
			carport_customer.save()
		elif order.carport_customer.id == user_phone:
			print(2)
			order.status = 'active'
			order.save()
			carport_customer.credit -= decimal.Decimal(0.50)
			carport_customer.save()
	return render(request , 'carport/order.html' , locals())


"""
辅助函数，返回end_time - begin_time的差值，结果为一个可能包含小数的数值，单位为小时
"""
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


"""
由传入的小时数，返回相应时间的停车费
"""
def get_price(time):
	table = {1: 2, 5: 5, 24: 10}
	over_day = (int(time / 24)) * 10
	inner_day = 0
	for i in table:
		if (int(time % 24)) < i:
			inner_day = table[i]
			break
	return over_day + inner_day


"""
定时任务，检查订单是否超时
"""
def check():
	order_list = models.Order.objects.filter(status='success')
	for order in order_list :
		end_time = order.end_time
		present_time = datetime.datetime.now()
		carport_customer = order.carport_customer
		if present_time > end_time:
			carport_customer.credit -= decimal.Decimal(1)
			order.status = 'danger'
			carport_customer.save()
			order.save()
			print(order)
			print(carport_customer)



"""
django辅助函数,详情见
https://blog.csdn.net/lzw2016/article/details/81546311
"""
@register.filter(name='displayName')
def displayName(value, arg):
	return eval('value.get_'+arg+'_display()')

