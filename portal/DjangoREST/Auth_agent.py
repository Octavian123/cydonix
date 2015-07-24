#python Auth_agent.py -c authconfig.ini

import sqlite3
import sys
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoREST.settings')
from django.conf import settings
#settings.configure()
from django.contrib.auth.models import User
from portal.models import Sensors, PermissionType, Permission
from django.core.exceptions import *
from optparse import OptionParser
import ConfigParser
import getpass
import sleekxmpp

import django
django.setup()


if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


def GetPermission(username,permission,sensor):
    # Geting user information 
    us=User.objects.get(username=self.username)
    if self.permission=="GET":

        name_permission="read"
    if self.permission=="SET":
        name_permission="write"
    #Geting permission type, read or write 
    pt=PermissionType.objects.get(name=name_permission)
    #Geting sensor information
    sr=Sensors.objects.get(sensor_type=self.sensor)
    try:
        #Testing if user has permission on sensor
        pr=Permission.objects.get(user=us,type=pt,sensor=sr)
        print" granted"
        return "granted"
    except ObjectDoesNotExist:
        print "forbidden"
        return "forbidden"


class AuthAgent(sleekxmpp.ClientXMPP):
    def __init__(self, username, password):
	sleekxmpp.ClientXMPP.__init__(self, username, password)
	self.add_event_handler("session_start", self.start)
	self.add_event_handler("message", self.message)

    def start(self, event):
	self.send_presence()
	self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
	    print "\n\n---------NEW MESSAGE----------"
	    print "Received message:  " +  msg['body']
            #msg.reply("Thanks for sending\n%(body)s" % msg).send()
	    #self.send_message(mto="bot_0007@teseus.integrasoft.ro"  ,mfrom="bot_0006@teseus.integrasoft.ro"  ,mbody="egrg", auth="dfsdf")
	    #print (msg.keys())
	    #print msg['body']
	    #print msg['subject']
	    #print msg['id']
	    #print msg['from']
	    #print "Received body: " + msg['body']
	    #print msg['from']
	    #asd=str(msg['from']).split("@")
            #self.send_message(mto="bot_0007@teseus.integrasoft.ro"  ,mfrom="bot_0006@teseus.integrasoft.ro"  ,mbody="asdsdsa")

	    #parsing id, username, permission
  	    parser=msg['body'].split(" ")
	    Pauth=parser[0]
	    Pid=parser[2]
    	    Pusername=parser[4]
   	    Ppermission=parser[6]
	    
	    #print Pauth
	    #print Pid
            #print Pusername
	    #print Ppermission

	    #parsing devices list
	    #parser2=msg['body'].split("['")
     	    #DeviceString=parser2[1]
	    #DeviceString=DeviceString[:-2]
	    #print "Device list= " + DeviceString
	    #Devices=DeviceString.split("', '")
	    #msg.reply("AUTH id= "+str(Pid)+" granted").send()    
            #bodu="AUTH id= "+str(Pid)+" granted"
            #self.send_message(mto="bot_0009@teseus.integrasoft.ro",mbody=bodu)

	    #Permission flag
	    ok=True

	    #Testing read permission for each device
	    if Ppermission == "GET":
		#print "GET loop"
		parser2=msg['body'].split("['")
     	        DeviceString=parser2[1]
	        DeviceString=DeviceString[:-2]
	        print "Device list= " + DeviceString
	        Devices=DeviceString.split("', '")
	        for i in Devices:
		    print "Testing permission for: " + i
		    try:
		        try:
		            us=User.objects.get(username=Pusername)
		            print "user: " + us.username
		        except ObjectDoesNotExist:
			    ok=False
   		        if Ppermission=="GET":
		            name_permission="read"
    		        if Ppermission=="SET":
        		    name_permission="write"
		        pt=PermissionType.objects.get(name=name_permission)
		        print "permission: " + pt.name
	                sr=Sensors.objects.get(sensor_type=i)
		        print "sensor: " + sr.sensor_type
		    except :
		        print "Unexpected error 1:", sys.exc_info()[0]
		    try:
      		        #Testing if user has permission on sensor
     		        pr=Permission.objects.get(user=us,type=pt,sensor=sr)
     		        print "User  " + us.username + " granted"
		        #print "MSG SENT1++++++++++++++++++++++++++++++++++++++++++++++++++++"
    		    except ObjectDoesNotExist:
       		        print "User  " + us.username + " forbidden"
		        ok=False
		        #print "MSG SENT2++++++++++++++++++++++++++++++++++++++++++++++++++++"
		    except:
		        print "Unexpected error 2: ", sys.exc_info()[0]
		    #print "***end for loop***"

            #Testing write permission	    
            elif Ppermission == "SET":
		#print "SET loop"
		
		#parsing the SET device
	        parser4=msg['body'].split(" ")
		parser5=parser4[8]
		#print parser5
		parser5=parser5[2:]
		parser6=parser5.split("=")
		#print "---------->>" + parser6[0]
		DeviceSET=parser6[0]
		print "Device:  " + DeviceSET

                try:
	            try:
			#checking if user exists in DB
	                us=User.objects.get(username=Pusername)
	                print "User:  " + us.username
	            except ObjectDoesNotExist:
	    	        ok=False
   		    if Ppermission=="GET":
		        name_permission="read"
    		    if Ppermission=="SET":
        		name_permission="write"
		    pt=PermissionType.objects.get(name=name_permission)
		    print "Permission:  " + pt.name
	            sr=Sensors.objects.get(sensor_type=DeviceSET)
		    print "sensor:  " + sr.sensor_type
		except:
		    print "Unexpected error 1: ", sys.exc_info()[0]
		try:
      		    #Testing if user has permission on sensor
     		    pr=Permission.objects.get(user=us,type=pt,sensor=sr)
     		    print "User  " + us.username + "  granted"
		    #print "MSG SENT1++++++++++++++++++++++++++++++++++++++++++++++++++++"
    		except ObjectDoesNotExist:
       		    print "User  " + us.username + "  forbidden"
		    ok=False
		    #print "MSG SENT2++++++++++++++++++++++++++++++++++++++++++++++++++++"
		except:
		    print "Unexpected error 2: ", sys.exc_info()[0]

		#print "END SET loop"
 	        

	    #Sending granted or forbidden message back to cydonix-agent
	    if ok==True:
                result = "granted"
	        bbody="AUTH id= "+str(Pid)+" "+result+" "+Ppermission
	        print "Sending this message back to cydonix-agent:  " + bbody
	        self.send_message(mto="bot_0009@teseus.integrasoft.ro", mbody=bbody)
		print "Message sent"
	    else:
     	        result = "forbidden"
	        bbody="AUTH id= "+str(Pid)+" "+result+" "+Ppermission
	        print "Sending this message back to cydonix-agent:  " + bbody
	        self.send_message(mto="bot_0009@teseus.integrasoft.ro", mbody=bbody)
		print "Message sent"
	        
	        
	    

if __name__ == '__main__':
    print "----------START---------"

    optp = OptionParser()

    #Setting up the command line arguments
    optp.add_option('-c', '--config=FILE', dest="conf_file", help='configuration FILE')

    opts, args = optp.parse_args()

    #Checking if the configuration file exists
    if not(os.path.isfile(str(opts.conf_file))):
        print "Configuration file does not exist"
        sys.exit()
    else:
        print "Configuration file found!"

    #Reading data from the configuration file
    conf = ConfigParser.ConfigParser()
    conf.read(opts.conf_file)

    username=conf.get("XMPP", "username")
    password=conf.get("XMPP", "password")
    host=conf.get("XMPP","host")
    port=conf.get("XMPP","port")

    print username
    print password
    print host
    print port

    print os.getcwd()
    print "----------END CONFIG---------"
  
    xmpp = AuthAgent(username, password)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199') # XMPP Ping

    if xmpp.connect():
        xmpp.process(block=True)
	print("Done")
    else:
	print("Unable to connect")








                  
    
    
    
    
    
