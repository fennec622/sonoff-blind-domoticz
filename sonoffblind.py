#!/usr/bin/python

import sys
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import threading 
import time 
import datetime
from datetime import datetime
import urllib2
import Queue
from datetime import datetime
from datetime import timedelta


print str(datetime.now())

b=[]
r=0
while r==0:

	try:
	
		url2=urllib2.Request('http://127.0.0.1:8080/json.htm?type=devices&filter=light&used=true&order=Name')
		url2=urllib2.urlopen(url2)
		url = json.loads(url2.read())
		r=1
	except:
		
		time.sleep(3)
		pass

#print url
thread=[]
dico={}
place=0
places={}
blinds=[]
blind=0

for i in url['result']:
	#print i
	types=i['SwitchType']
	matos=i['HardwareName']
	#print types
	if types =="Blinds Percentage Inverted" and matos=="Virtual":
		#dico[i['Name']]=i['LevelInt']
		thr=[]
		thr.append(str(i['idx']))
		thr.append(i['LevelInt'])
		thr.append(Queue.Queue())
		thr.append(threading.Lock())
		thr.append(Queue.Queue())
		thr.append(Queue.Queue())
		thr.append(threading.Lock())
		thr.append(i['Name'])
		thr.append(i['Description'])
		thr.append(Queue.Queue())
		thread.append(thr)
		pulsetime1=str(int(i['Description'].split(" ")[0])+7)
		pulsetime2=str(int(i['Description'].split(" ")[1])+7)
		places[i['Name']]=str(place)
		place+=1
		publish.single("cmnd/"+i['Name']+"/PulseTime1","1"+pulsetime1, hostname="192.168.5.1")
		publish.single("cmnd/"+i['Name']+"/PulseTime2","1"+pulsetime2, hostname="192.168.5.1")
	if types =="Blinds" and matos=="rfxcom":
		bl=[]
	





class verifblindauto2(threading.Thread):

	def __init__(self, tab,pos,fin): 
		threading.Thread.__init__(self) 
		print "verifiblind "+str(pos)
		self.tab = tab
		self.pos = pos
		self.terminated = fin
		self.r=0

	def run(self): 

		t=(float(str(self.tab[self.pos][8].split(" ")[1]))-1)/15
		t1=(float(str(self.tab[self.pos][8].split(" ")[0]))-1)/15

		while self.terminated :
			try:
				if not self.tab[self.pos][4].empty() :
					#self.tab[self.pos][6].acquire()
					ad=self.tab[self.pos][4].get()
					z=0
					while z==0:
						self.r+=0.1
						time.sleep(0.1)
						if not self.tab[self.pos][4].empty():
							ad=self.tab[self.pos][4].get()
						if ad == 1:
							te=t
						if ad == -1:
							te=t1
						if self.r>=te:
							self.r=0
							self.tab[self.pos][1]=self.tab[self.pos][1]+ad
							#self.tab[self.pos][9].put(self.tab[self.pos][1])
							#self.tab[self.pos][3].acquire()
							print str(datetime.now())+" pourcentage bouton "+str(self.tab[self.pos][1])
							publish.single("domoticz/in",'{"command":"switchlight","idx":'+str(self.tab[self.pos][0])+',"level":'+str(self.tab[self.pos][1])+',"switchcmd":"Set Level"}', hostname="192.168.5.1")
							#while self.thread[self.places][3].locked():
							#	time.sleep(0.1)
						if ad==2 or self.tab[self.pos][1]>14 and ad==1 or self.tab[self.pos][1]<1 and ad==-1:
							print str(datetime.now())+" STOP ou fermeture/ouverture complete"
							
							z=1
					self.r=0
					#self.tab[self.pos][6].release()
				
				else:
					time.sleep(0.1)
			except:
				print sys.exc_info()
				time.sleep(0.1)
				pass



class remotepercent(threading.Thread): 
	def __init__(self, tab,pos,fin): 
		threading.Thread.__init__(self) 
		print "percent "+str(pos)
		self.tab = tab
		self.pos = pos
		self.terminated = fin

	def run(self): 

		while self.terminated :
			#try:
				if not self.tab[self.pos][2].empty() :
					
					ne=self.tab[self.pos][2].get()
					print str(datetime.now())+" move domoticz"
					if self.tab[self.pos][1]!=ne:
						nom= self.tab[self.pos][7]
						initpos=self.tab[self.pos][1]
						timedown=self.tab[self.pos][8].split(" ")[0]
						timeup=self.tab[self.pos][8].split(" ")[1]
						newpos=ne

						#self.tab[self.pos][6].acquire()
						newpos=movevolet(initpos,newpos,nom,timedown,timeup)
						self.tab[self.pos][1]=newpos
						#self.tab[self.pos][6].release()
						print str(datetime.now())+" fin move domoticz"
						#try:
						#	off=self.tab[self.pos][5].get()
						#except:pass
				#logger.info(initpos,newpos,idx)
					time.sleep(0.1)
					
					
					#self.tab[self.pos][5].get()
					
					#print "fin move"
					
				time.sleep(0.1)
			#except:
				#logger.info(sys.exc_info())
				#time.sleep(0.5)
				#pass

def movevolet(valeurinit,valeur,nom,timedown,timeup):
	if int(valeur)>int(valeurinit):
		valeurinit=int(valeurinit)
		valeur=int(valeur)
		publish.single("cmnd/"+nom+"/power1",'on', hostname="192.168.5.1")
		print str(datetime.now())+" ouverture dom "+str(nom)
		z=1
		t=(int(timeup)-1)/15
		#t=((int(valeur)-int(valeurinit))*int(timeup)/15)
		print str(datetime.now())+" temps mouvement "+str(t)
		t1=0
		while z==1:
			if t1>=t:
				valeurinit+=1
			if valeurinit>=valeur:
				z=0
				if int(valeurinit) != 15 :
					publish.single("cmnd/"+nom+"/power1",'off', hostname="192.168.5.1")
					print str(datetime.now())+" stop dom "+str(nom)
					print str(datetime.now())+" nouvelle valeur "+str(valeurinit)
				return valeurinit
			elif not thread[int(places[nom])][4].empty():

				publish.single("cmnd/"+nom+"/power1",'off', hostname="192.168.5.1")
				print str(datetime.now())+" stop dom "+str(nom)
				print str(datetime.now())+" nouvelle valeur "+str(valeurinit)
				return valeurinit
			t1+=0.1
			time.sleep(0.1)


		#time.sleep(((int(valeur)-int(valeurinit))*int(timeup)/15))
		
	else :
		valeurinit=int(valeurinit)
		valeur=int(valeur)
		publish.single("cmnd/"+nom+"/power2",'on', hostname="192.168.5.1")
		print str(datetime.now())+" fermeture dom "+str(nom)
		z=1
		#t=((int(valeurinit)-int(valeur))*int(timedown)/15)
		t=(int(timedown)-1)/15
		print str(datetime.now())+" temps mouvement "+str(t)
		t1=0
		while z==1:
			if t1>=t:
				valeurinit-=1
			if valeurinit<=valeur:
				z=0
				if int(valeurinit) !=0 :
					publish.single("cmnd/"+nom+"/power2",'off', hostname="192.168.5.1")
					print str(datetime.now())+" stop dom "+str(nom)
					print str(datetime.now())+" nouvelle valeur "+str(valeurinit)
				return valeurinit
			elif not thread[int(places[nom])][4].empty():
				publish.single("cmnd/"+nom+"/power2",'off', hostname="192.168.5.1")
				print str(datetime.now())+" stop dom "+str(nom)
				print str(datetime.now())+" nouvelle valeur "+str(valeurinit)
				return valeurinit
			t1+=0.1
			time.sleep(0.1)

def on_connect(client, userdata, flags, rc):
		
	channel="stat/"+str(userdata)+"/#"
	print channel
	client.subscribe(channel)
	#client.subscribe("domoticz/#")



def on_messagebou(client, userdata, msg):

	#action(msg,thread,places).start()
	#if  not thread[int(places[msg.topic.split("/")[1]])][6].locked():	
		


			if "POWER1" in msg.topic:
				if msg.payload=="ON":
					value=1
				#print corvolet[str(a['idx'])]
					print str(datetime.now())+" ouverture"
					#if thread[int(places[msg.topic.split("/")[1]])][1]<15:
					thread[int(places[msg.topic.split("/")[1]])][4].put(value)
					
				elif msg.payload=="OFF":
					value=2
				#print corvolet[str(a['idx'])]
					print str(datetime.now())+" off ouverture"
					thread[int(places[msg.topic.split("/")[1]])][4].put(value)
					
			if "POWER2" in msg.topic:
				if msg.payload=="ON":
					value=-1
				#print corvolet[str(a['idx'])]
					print str(datetime.now())+" fermeture"
					#if thread[int(places[msg.topic.split("/")[1]])][1]>0:
					thread[int(places[msg.topic.split("/")[1]])][4].put(value)
					
				elif msg.payload=="OFF":
					value=2
					print str(datetime.now())+" fermeture OFF"
					thread[int(places[msg.topic.split("/")[1]])][4].put(value)

	#else:
			#print str(datetime.now())+" mouvement homebridge"
	


def on_connectdom(client, userdata, flags, rc):
	
	client.subscribe("domoticz/out")
	print str(userdata)

def on_messagedom(client, userdata, msg):

	#a=json.loads(msg.payload)
	#print a
	try:
		if a['switchType']== 'Blinds Percentage Inverted' and a['stype']== 'AC':
			print str(datetime.now())+" switch domoticz"
			#actiondom(msg,thread,places).start()
			if  not thread[int(places[str(a['name'])])][6].locked():
				a=json.loads(msg.payload)
				if a['switchType']== 'Blinds Percentage Inverted' and a['stype']== 'AC':
					# 	try:print(str(a['switchType'])+" "+str(a['name'])+" pourcentage "+str(a['svalue1']))
					# 	except:print(str(a['switchType'])+" "+str(a['name'])+" nvalue "+nvalue[str(a['nvalue'])])
					if int(a['nvalue'])==0:

						pos=0
					elif int(a['nvalue'])==1:

					 	pos=15
					elif int(a['nvalue'])==2:

					 	pos=int(a['svalue1'])
				 	print str(datetime.now())+" "+a['name']+" "+str(pos)
					thread[int(places[str(a['name'])])][2].put(pos)
			else:
				
				print str(datetime.now())+" mouvement bouton"
		#print str(userdata)
	#print msg.payload
	except:
		pass
		#print sys.exc_info()
		#print str(datetime.now())+" pas de nom"



		 



def on_message(client, userdata, msg):
	print str(datetime.now())+" "+str(msg.topic)+" "+str(msg.payload)

fin=True
lock=threading.Lock()

print range(len(thread))
for t in range(len(thread)):
	remotepercent(thread,t,fin).start()
	verifblindauto2(thread,t,fin).start()
	#startmqttdom(thread,t,fin).start()
	#startmqtt(thread,t,fin).start()



while True:
				try:
					client=mqtt.Client()
					client.message_callback_add("stat/#", on_messagebou)
					client.message_callback_add("domoticz/out", on_messagedom)
					client.on_message = on_message
					client.connect("127.0.0.1", 1883, 60)
					client.subscribe("#")
					client.loop_forever()
				except:
					print sys.exc_info()
					print "erreur startmqttdom"
					print "Exception handled, reconnecting...\nDetail:\n%s"
					time.sleep(5)

			
				
				

fin=False
