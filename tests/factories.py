import time
import random

def create_random_time_str(st_time="2021-01-01", end_time="2021-12-1"):
	"""generate a random "YYYY-DD-MM" date within st_time and end_time
	"""
		
	time_format = "%Y-%d-%m"
	stime = time.mktime(time.strptime(st_time, time_format))
	etime = time.mktime(time.strptime(end_time, time_format))
	prop = random.random()
	random_time = stime + prop * (etime - stime)
	return time.strftime(time_format, time.localtime(random_time))