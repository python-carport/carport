import datetime

print('s11s11a'.split('11'))
print(datetime.datetime.now())

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

	#ss