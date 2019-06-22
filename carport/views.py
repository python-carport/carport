from django.shortcuts import render , redirect

from django.http import HttpResponse

from carport import models
from carport.models import LoginForm


def index(request):
	if not request.session.get('is_login'):
		return redirect('/carport/login')
	return HttpResponse("Hello, world. You're at the polls index.")


def login(request):
	request.session.flush()
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
					return redirect('/carport/index')
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
