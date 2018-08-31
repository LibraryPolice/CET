# -*- coding: UTF-8 -*-
import requests
import re
import http.cookiejar
from PIL import Image
from io import BytesIO
import random
import queue
import threading
import time
from sklearn import svm
import os
from numpy import array

clf = svm.SVC(kernel='linear')  #线性准确率高一点

def do_image_crop(img):
    """做图片切割，返回块图片列表"""
    start = 18
    width = 37
    top = 0
    height = 100

    img_list = []

    def init_table(threshold=135):
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)

        return table

    img = img.convert("L").point(init_table(), '1')

    for i in range(4):
        new_start = start + width * i
        box = (new_start, top, new_start + width, height)
        piece = img.crop(box)

        img_list.append(piece)

    return img_list
def img_list_to_array_list(img_list):
    """PIL Image对象转array_list"""
    array_list = []
    for img in img_list:
        array_list.append(array(img).flatten())
    return array_list

def get_image_fit_data(dir_name):
    """读取labeled_images文件夹的图片，返回图片的特征矩阵及相应标记"""
    X = []
    Y = []
    name_list = os.listdir(dir_name)
    for name in name_list:
        if not os.path.isdir(os.path.join(dir_name, name)):
            continue
        image_files = os.listdir(os.path.join(dir_name, name))
        for img in image_files:
            i = Image.open(os.path.join(dir_name, name, img))
            X.append(array(i).flatten())
            Y.append(name)

    return X, Y


def get_classifier_from_learn():
    """学习数据获取分类器"""
    t = time.time()
    #clf = svm.SVC()   #默认为rbf
    X, Y = get_image_fit_data("labeled_images")
    clf.fit(X, Y)
    print("学习用了"+str(time.time()-t)+"s")
def get_validate_code_from_image(img):
    img_piece = do_image_crop(img)
    X = img_list_to_array_list(img_piece)
    y = clf.predict(X)
    return "".join(y)

s=requests.session()
chaxun_api="http://cache.neea.edu.cn/cet/query"
chaxun_header={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Content-Length':'75',
'Content-Type':'application/x-www-form-urlencoded',
'Host':'cache.neea.edu.cn',
'Origin':'http://cet.neea.edu.cn',
'Referer':'http://cet.neea.edu.cn/cet',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5514.400 QQBrowser/10.1.1628.400'
}
img_header = {
'Accept':'*/*',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'Host':'cache.neea.edu.cn',
'Referer':'http://cet.neea.edu.cn/cet/',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5514.400 QQBrowser/10.1.1628.400'
}
flag=True
class thread_cet(threading.Thread):

	def __init__(self, que):
		threading.Thread.__init__(self)
		self.que=que

	def run(self):
		global flag
		while flag:
			if not self.que.empty():
				id=self.que.get()
				response=chaxun(id)
				if id in response:
					print(result_table(response))
					with open ("result/"+name+"-"+str(id)+".txt","w") as f:
						f.write(result_table(response))  #查到存成绩
					flag=False
			else:
				break

def kcformat(kc):
	if kc<10:
		kc="00"+str(kc)
	elif kc<100:
		kc="0"+str(kc)
	return str(kc)
def zwformat(zw):
	if zw<10:
		zw="0"+str(zw)
	return str(zw)
def info():
	global idten,name,start,jibie
	idten=input("请输入前十位准考证:")
	name=input("请输入姓名:")
	jibie=input("请输入四六级(四级输入1,六级输入2):")
	start=input("从哪个考场开始(默认是000):")
	if start=="":
		start=1
	else:
		start=int(start)
	if jibie=='1':
		jibie='CET4_181_DANGCI'
	elif jibie=='2':
		jibie='CET6_181_DANGCI'
	else:
		print("输入错误,请重新输入!")
		return info()
def push_value_to_query(idten_from_input,name_from_input,start_from_input,jibie_from_input):#api_for_wxpython
	global idten,name,start,jibie
	idten = idten_from_input
	name = name_from_input
	start = start_from_input
	jibie = jibie_from_input
def query():
	for i in range(int(start),end):
		i=kcformat(i)
		for j in range(1,31):
			id=idten+i+zwformat(j)
			response = chaxun(id)
			if "结果为空" in response:
				continue
			else:
				print(result_table(response))
				#print("找到了,你的准考证号:"+id)
				exit(0)
def thread_query():
	que = queue.Queue()
	for i in range(int(start),end):
		i=kcformat(i)
		for j in range(1,31):
			id=idten+i+zwformat(j)
			que.put(id)
	th1=thread_cet(que)
	th2=thread_cet(que)
	th3=thread_cet(que)
	th1.start()
	th2.start()
	th3.start()  #三线程

def result_table(data):
	id = re.findall(r"{z:'(.*?)',n:",data)
	name = re.findall(r"n:'(.*?)',x:",data)
	school = re.findall(r",x:'(.*?)',s:", data)
	all = re.findall(r",s:(.*?),t:", data)
	listen = re.findall(r",l:(.*?),r:", data)
	read = re.findall(r",r:(.*?),w:", data)
	write = re.findall(r",w:(.*?),kyz", data)
	str="准考证号:\t"+id[0]+"\n姓   名:\t"+name[0]+"\n学   校:\t"+school[0]+"\n听   力:\t"+listen[0]+"\n阅   读:\t"+read[0]+"\n写   作:\t"+write[0]+"\n总   分:\t"+all[0]
	return str
def chaxun(id):  #递归查询
	im=getimg(id)   #获取图片
	code=get_validate_code_from_image(im)   #预测验证码
	data = {
		"data": jibie+","+id+","+name,
		"v": code
	}
	query_resp = s.post(chaxun_api,data=data,headers=chaxun_header)
	query_text = query_resp.text
	if "验证码错误" in query_text:
		query_text = chaxun(id)
		#im.save("error/error_"+code+".png")
	else:
		print(id+"\t"+jibie+"\r"+query_text)   #返回id和服务器中的信息
	return query_text

def getimg(id):
	imgurl="http://cache.neea.edu.cn/Imgs.do?c=CET&ik="+id+"&t="+str(random.random())
	try:
		response=s.get(imgurl,headers=img_header,timeout=2)
		#print(response.text)  #返回图片url  result
		#print(response.text)
		url = re.findall(r"imgs\(\"(.*?)\"\)",response.text)
		#print(url)
		r = s.get(url[0])  #图片url
		im=Image.open(BytesIO(r.content))
		im = im.convert('L')
	except:
		print("获取图片超时")
		im=getimg(id)
	return im  #return 图片
def info2():
	global idten,name,start,jibie,end
	start = 0    #开头的考场号,如果是第11位是1的话位100，如果第11位是2的话，为200
	end = 400		#结束的考场号
	name = "付灏"   #姓名  千万不能输错,输错了死也查不到
	idten = "2300601811"   #准考证号前十位
	if idten[9]=='1':
		jibie='CJT4_181_DANGCI'
	else:
		jibie='CET6_181_DANGCI'
if __name__ == "__main__":
	info2()
	get_classifier_from_learn()   #学习验证码
	thread_query()
