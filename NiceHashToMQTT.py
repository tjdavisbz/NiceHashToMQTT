import Config
import requests
import json
from NicehashData import NicehashData
from NicehashData import NicehashDataList
import paho.mqtt.client as mqtt
import datetime
import os,sys
from time import sleep
nicehashdatalist = NicehashDataList([])

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected.")
    else:
        print("MQTT Connection failed with error code " + str(rc))

def deserializenicehash(nicehashjsondata):
    for algorithm in nicehashjsondata['result']['current']:
        try:
            nicehashdata = NicehashData(algorithm['name'],algorithm['data'][0]['a'],algorithm['suffix'],algorithm['data'][1])
            nicehashdatalist.append(nicehashdata)
        except Exception as e:
            # print str(e)
            error = 1

def publishToMQTT():
    client = mqtt.Client()
    client.on_connect = on_connect

    nicehashdatalist.clear()

    if Config.brokerUser != "" and Config.brokerPassword != "":
        client.username_pw_set(username=Config.brokerUser,password=Config.brokerPassword)

    client.connect(Config.brokerURL,Config.brokerPort,60)

    response = requests.get("https://api.nicehash.com/api?method=stats.provider.ex&addr=" + Config.walletaddress)
    nicehashjsondata = json.loads(response.text)

    nicehashdata = deserializenicehash(nicehashjsondata)

    client.publish(Config.brokerTopic + "/hashrate",nicehashdatalist.hashratetotal())
    sleep(1)
    client.publish(Config.brokerTopic + "/pendingbalance",nicehashdatalist.balancetotal())
    sleep(1)
    client.publish(Config.brokerTopic + "/pendingbalanceUSD",nicehashdatalist.balanceUSDtotal())
    sleep(1)
    client.publish(Config.brokerTopic + "/jsonvalues","{\"Hashrate\":\"" + str(nicehashdatalist.hashratetotal()) + "\"" + ",\"Pending Balance\":\"" + str(nicehashdatalist.balancetotal()) + "\"" + ",\"Pending Balance USD\":\"" + str(nicehashdatalist.balanceUSDtotal()) + "\"}")
    # print "/jsonvalues","{\"Hashrate\":\"" + str(nicehashdatalist.hashratetotal()) + "\"" + ",\"Pending Balance\":\"" + str(nicehashdatalist.balancetotal()) + "\"" + ",\"Pending Balance USD\":\"" + str(nicehashdatalist.balanceUSDtotal()) + "\"}"
    client.loop_stop()
    client.disconnect()

while 1 == 1:
    publishToMQTT()
    print str(datetime.datetime.now()) + ": Publishing again in " + str(Config.brokerPublishFrequency) + " seconds"
    sleep(Config.brokerPublishFrequency)
