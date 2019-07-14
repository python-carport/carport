import datetime
import math
from _decimal import Decimal

import decimal
from django.shortcuts import render , redirect

from django.http import HttpResponse
from django.template.defaultfilters import register

from carport import models
from carport.models import LoginForm , AppointmentForm


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
					request.session['message'] = ''
					request.session['alert_class'] = ''
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
	message = request.session['message']
	alert_class = request.session['alert_class']
	request.session['message'] = ''
	request.session['alert_class'] = ''
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
			create_time = get_now(),
			begin_time = begin_time,
			end_time = end_time,
			amount = total,
			status = 'success',
			carport_site = carport_site,
			carport_owner = owner,
			carport_customer = customer,
		)
		request.session['message'] = '预订成功!'
		request.session['alert_class'] = 'alert-success'
		return render(request , 'carport/order_to.html' , locals())


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
		# request.session['message'] = '发布成功!'
		# request.session['alert_class'] = 'alert-success'
		message = '发布成功!'
		alert_class = 'alert-success'
		request.session['previous_page'] = request.session['current_page']
		request.session['current_page'] = 'publish'
		return render(request, 'carport/publish.html', locals())

	# message = request.session['message']
	# alert_class = request.session['alert_class']
	# request.session['message'] = ''
	# request.session['alert_class'] = ''
	carport_site_list = models.Carport.objects.filter(owner_phone = user_phone).values_list('site', flat= True)
	request.session['previous_page'] = request.session['current_page']
	request.session['current_page'] = 'publish'
	result_list = []
	for carport_site in carport_site_list:
		if models.Carport.objects.get(site = carport_site).current_car_license == '':
			result_list.append(carport_site)
	if result_list.__len__() == 0:
		message = '此账号下无可发布车位'
		alert_class = 'alert-warning'
	result_list_size = result_list.__len__()
	return render(request , 'carport/publish.html' , locals())


"""
按时间查询此时间段内被发布的可用车位
"""
def inquiry(request):
	appointment_message = "检查填写内容！"
	alert_class = 'alert-danger'
	appointment_form = AppointmentForm(request.GET)
	carport_list = []
	negotiate_list = []
	if appointment_form.is_valid():
		car_license = appointment_form.cleaned_data['car_license']
		begin_time = appointment_form.cleaned_data['begin_time']
		end_time = appointment_form.cleaned_data['end_time']
		diff = date_diff(begin_time, end_time)
		temp = math.floor(diff)
		if diff > temp:
			appointment_form.total = get_price(temp+1)
		elif diff == temp:
			appointment_form.total = get_price(temp)

		# request.session['message'] = '查询、计价成功！'
		# request.session['alert_class'] = 'alert-success'
		message = '查询、计价成功！'
		alert_class = 'alert-success'
		carport_list = get_carport_list(begin_time, end_time)
		negotiate_list = get_negotiate_list(begin_time, end_time)
		request.session['negotiate_list'] = negotiate_list
		request.session['appointment_car_license'] = car_license
		request.session['appointment_begin_time'] = begin_time
		request.session['appointment_end_time'] = end_time
		request.session['appointment_total'] = appointment_form.total

	return render(request, 'carport/appointment.html', locals())


"""
返回指定时间内的可协商车位的列表
"""
def get_negotiate_list(begin_time, end_time):
	record_list = models.Record.objects.all()
	record_map = {}
	result = []
	for i in record_list:#时间相加有问题
		record_map.update({i.carport_site:record_map.get(i.carport_site, 0)+i.total_time})
	sort_list = sorted(record_map.items(), key = lambda x: x[1], reverse = False)
	diff = date_diff(begin_time, end_time)
	for i in range(0 , 9):
		try:
			result.append((sort_list[i][0] , models.Carport.objects.get(site = sort_list[i][0]).owner_phone, result.__len__()+1))
		except:
			print(i)
	return result


"""
执行协商
"""
def negotiate(request):
	negotiate_list = request.session['negotiate_list']
	user = request.session['user']

	car_license = request.POST['car_license']
	begin_time = request.POST['begin_time']
	end_time = request.POST['end_time']
	total = get_price(date_diff(datetime.datetime.strptime(begin_time, '%Y-%m-%d %H:%M'), datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M')))
	try:
		models.Order.objects.filter(carport_customer_id = user.phone, status = 'negotiate').delete()
	except:
		pass
	try:
		n = models.Negotiation.objects.get(customer_phone = user.phone , status = 'underway')
		try:
			info = models.Inform.objects.filter(negotiate_id = n.id , status = 'success')
			for i in info:
				i.status = 'over_time'
				i.save()
		except:
			pass
		n.delete()
	except:
		pass
	o = models.Order.objects.create(
		car_license = car_license,
		create_time = get_now(),
		begin_time = begin_time,
		carport_site = negotiate_list[0][0],
		end_time = end_time,
		amount = total,
		status = 'negotiate',
		carport_customer_id = user.phone,
		carport_owner_id = negotiate_list[0][1],
	)
	n = models.Negotiation.objects.create(
		customer_phone = user.phone ,
		owner_phone = negotiate_list[0][1] ,
		negotiate_site = negotiate_list[0][0] ,
		negotiate_list = negotiate_list ,
		record_time = get_now() ,
		status = 'underway' ,
	)
	models.Inform.objects.create(
		belong_phone = negotiate_list[0][1] ,
		message = user.phone + ' 请求协商车位：' + negotiate_list[0][0] + "\t预约时间为：" + begin_time + " 至 " + end_time ,
		create_time = get_now() ,
		status = 'success' ,
		order = o ,
		negotiate_id = n.id,
	)
	return render(request , 'carport/appointment.html' ,locals())


"""
自动协商
"""
def auto_negotiate():
	negotiation_list = models.Negotiation.objects.filter(status = 'underway')
	for item in negotiation_list:
		now = get_now()
		create_time = item.record_time
		# 如果当前时间-记录时间 > 1min ，选择下一个车位进行协商
		if (now - create_time).seconds / 60 > 1:
			negotiate_next(item)

"""
协商下一车位
"""
def negotiate_next(negotiation):
	site = negotiation.negotiate_site
	negotiate_list = eval(negotiation.negotiate_list)
	o = models.Order.objects.get(carport_customer_id = negotiation.customer_phone , status = 'negotiate')
	# 如果已经是最后一个协商车位，则结束
	if site == negotiate_list[negotiate_list.__len__() - 1][0]:
		negotiation.status = 'end'
		negotiation.save()
		o.status = 'invalid'
		info = models.Inform.objects.get(belong_phone = negotiation.owner_phone)
		info.status = 'active'
		info.save()
		models.Inform.objects.create(
			belong_phone = negotiation.customer_phone ,
			message = '协商未成功' ,
			create_time = get_now() ,
			status = 'danger' ,
			order = o
		)

		return 200

	for i in range(0 , negotiate_list.__len__() - 1):
		if negotiate_list[i][0] == site:
			info = models.Inform.objects.get(belong_phone = negotiation.owner_phone)
			info.status = 'active'
			info.save()
			# 信息更新
			negotiation.negotiate_site = negotiate_list[i + 1][0]
			negotiation.owner_phone = models.Carport.objects.get(site = negotiate_list[i + 1][0]).owner_phone
			o.carport_owner_id = negotiation.owner_phone
			o.carport_site = negotiation.negotiate_site
			o.create_time = get_now()
			o.save()
			negotiation.save()
			# 通知下一车位主人
			models.Inform.objects.create(
				belong_phone = negotiate_list[i+1][1] ,
				message = o.carport_customer_id + ' 请求协商车位：' + negotiation.negotiate_site + "\t预约时间为：" + str(o.begin_time) + " 至 " + str(o.end_time) ,
				create_time = get_now() ,
				status = 'success' ,
				order = o ,
				negotiate_id = negotiation.id ,
			)
			break



"""
初始化，显示我预订的订单页面
"""
def order_to(request):
	message = request.session['message']
	alert_class = request.session['alert_class']
	request.session['message'] = ''
	request.session['alert_class'] = ''
	user_phone = request.session.get('user').phone
	order_list = models.Order.objects.filter(carport_customer_id = user_phone).exclude(status = 'negotiate').exclude(status = 'invalid')
	k = 0
	step_index = -1
	try:
		negotiation = models.Negotiation.objects.get(customer_phone = user_phone , status = 'underway')
		negotiate_list = eval(negotiation.negotiate_list)
		list_len = negotiate_list.__len__()
		negotiate_site = negotiation.negotiate_site
		for i in range(0 , negotiate_list.__len__()):
			if negotiate_list[i][0] == negotiate_site:
				step_index = i
				break
	except:
		pass

	request.session['previous_page'] = request.session['current_page']
	request.session['current_page'] = 'order_to'
	return render(request, 'carport/order_to.html', locals())


"""
初始化，显示我接受的订单页面
"""
def order_from(request):
	message = request.session['message']
	alert_class = request.session['alert_class']
	request.session['message'] = ''
	request.session['alert_class'] = ''
	user_phone = request.session.get('user').phone
	order_list = models.Order.objects.filter(carport_owner_id = user_phone).exclude(status = 'negotiate').exclude(status = 'invalid')

	request.session['previous_page'] = request.session['current_page']
	request.session['current_page'] = 'order_from'
	return render(request, 'carport/order_from.html', locals())


"""
显示消息通知页面
"""
def inform(request):
	message = request.session['message']
	alert_class = request.session['alert_class']
	request.session['message'] = ''
	request.session['alert_class'] = ''
	user_phone = request.session['user'].phone
	inform_list = []
	try:
		inform_list = models.Inform.objects.filter(belong_phone = user_phone)
	except:
		pass
	list_len = inform_list.__len__()
	request.session['previous_page'] = request.session['current_page']
	request.session['current_page'] = 'inform'
	return render(request , 'carport/inform.html' , locals())


"""
接受协商
"""
def accept(request):
	inform_id = request.POST['inform_id']
	info = models.Inform.objects.get(id = inform_id)
	o = info.order
	n = models.Negotiation.objects.get(customer_phone = o.carport_customer_id, status = 'underway')
	n.status = 'end'
	n.save()
	o.status = 'success'
	o.save()
	info.status = 'warning'
	info.save()
	request.session['message'] = '协商成交，订单生成成功！'
	request.session['alert_class'] = 'alert-success'
	return render(request , 'carport/order_from.html' , locals())


"""
拒绝协商
"""
def reject(request):
	inform_id = request.POST['inform_id']
	info = models.Inform.objects.get(id = inform_id)
	n = models.Negotiation.objects.get(customer_phone = info.order.carport_customer_id, status = 'underway')
	negotiate_next(n)
	request.session['message'] = '拒绝协商成功'
	request.session['alert_class'] = 'alert-warning'
	return render(request , 'carport/order_from.html' , locals())


"""
在我的订单页面提前终止订单的方法
"""
def finish(request):
	order_id = request.GET.get('order_id')
	this_order = models.Order.objects.get(id = order_id)
	this_order.status = 'warning'
	this_order.save()
	user_phone = request.session.get('user').phone
	order_list = models.Order.objects.filter(carport_customer_id = user_phone).exclude(status = 'negotiate').exclude(status = 'invalid')
	request.session['message'] = '终止成功'
	request.session['alert_class'] = 'alert-success'
	return render(request, 'carport/order_to.html', locals())


"""
在我的订单页面，撤销订单的方法
"""
def cancel(request):
	order_id = request.GET.get ('order_id')
	order = models.Order.objects.get (id=order_id)
	begin_time = order.begin_time
	now = get_now()
	diff = date_diff (now, begin_time)
	user_phone = request.session.get('user').phone
	carport_customer = order.carport_customer
	carport_owner = order.carport_owner
	if diff>1:
		order.status='active'
		order.save()
	elif diff<=1:
		if order.carport_owner.id == user_phone:
			carport_owner.credit -= decimal.Decimal(0.50)
			carport_owner.remain -= decimal.Decimal(order.amount*2)
			carport_customer.remain += decimal.Decimal(order.amount*2)
			order.status = 'active'
			order.save()
			carport_owner.save()
			carport_customer.save()
		elif order.carport_customer.id == user_phone:
			order.status = 'active'
			order.save()
			carport_customer.credit -= decimal.Decimal(0.50)
			carport_customer.save()
	request.session['message'] = '取消成功'
	request.session['alert_class'] = 'alert-success'
	return render(request , 'carport/order_to.html' , locals())


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
		present_time = get_now()
		carport_customer = order.carport_customer
		if present_time > end_time:
			carport_customer.credit -= decimal.Decimal(1)
			order.status = 'danger'
			carport_customer.save()
			order.save()


"""
返回特定格式的当前时间
"""
def get_now():
	return datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')


"""
django辅助函数,详情见
https://blog.csdn.net/lzw2016/article/details/81546311
"""
@register.filter(name='displayName')
def displayName(value, arg):
	return eval('value.get_'+arg+'_display()')

