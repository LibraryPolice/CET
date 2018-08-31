import requests
import re
import http.cookiejar
from PIL import Image
from io import BytesIO
from getcode import *
import random
import queue
import threading
data="<script>document.domain='neea.edu.cn';</script><script>parent.result.callback(\"{z:'360021172114104',n:'胡晓帆',x:'江西师范大学',s:474.00,t:0,l:206,r:145,w:123,kyz:'--',kys:'--'}\");</script>"

def result_table(data):
	id = re.findall(r"{z:'(.*?)',n:",data)
	name = re.findall(r"n:'(.*?)',x:",data)
	school = re.findall(r",x:'(.*?)',s:", data)
	all = re.findall(r",s:(.*?),t:", data)
	listen = re.findall(r",l:(.*?),r:", data)
	read = re.findall(r",r:(.*?),w:", data)
	write = re.findall(r",w:(.*?),kyz", data)
	str="准考证号:"+id[0]+"\n姓   名:\t"+name[0]+"\n学   校:\t"+school[0]+"\n听   力:\t"+listen[0]+"\n阅   读:\t"+read[0]+"\n写   作:\t"+write[0]+"\n总   分:\t"+all[0]
	return str
if __name__ == '__main__':
	print(result_table(data))
	with open ("code.txt","w") as f:
		f.write(result_table(data))