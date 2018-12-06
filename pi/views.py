from django.shortcuts import render, redirect
from django.http import HttpResponse

# AWS IOT
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json

def index(request):
    context = {
        'title':'Pi',
        'menus':[
            ['Home','/'],
            ['Pi','/pi']
        ],
        'object':[
            ['Light','']
        ]
    }
    return render(request, 'pi/index.html', context)

def api(request):
    if request.GET.get('object') and request.GET.get('action'):
        data = {
            'object':request.GET['object'],
            'action':request.GET['action']
        }
        messageJson = json.dumps(data)
        result = publish(messageJson)
        data['status'] = result
        messageJson = json.dumps(data)
        context = {
            'title':'Pi',
            'menus':[
                ['Home','/'],
                ['Pi','/pi']
            ],
            'object':[
                ['Light',messageJson]
            ]
        }
        return render(request, 'pi/index.html', context)
    else:
        return redirect('/pi')

def publish(messageJson):
    host = "a2xgz48pfgodus-ats.iot.us-east-1.amazonaws.com"
    rootCAPath = 'doc/root-CA.crt'
    certificatePath = 'doc/SmartHome.cert.pem'
    privateKeyPath = 'doc/SmartHome.private.key'
    useWebsocket = False
    clientId = "smarthome"
    topic = "smarthome"
    myAWSIoTMQTTClient = None
    if useWebsocket:
        port = 443
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
        myAWSIoTMQTTClient.configureEndpoint(host, port)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath)
    else:
        port = 8883
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
        myAWSIoTMQTTClient.configureEndpoint(host, port)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
    myAWSIoTMQTTClient.configureDrainingFrequency(2)
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)
    try:
        myAWSIoTMQTTClient.connect()
        print("Connection Success")
    except:
        print("Connection Failed")
        return False
    try:
        myAWSIoTMQTTClient.publish(topic, messageJson, 1)
        print("Publish Success")
    except:
        print("Publish Failed")
        return False
    return True