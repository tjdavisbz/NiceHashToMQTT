import config
import requests
import json
from NicehashData import NicehashData
from NicehashData import NicehashDataList
import paho.mqtt.client as mqtt
import datetime
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
            nicehashdata = NicehashData(algorithm['name'], algorithm['data'][0]['a'], algorithm['suffix'], algorithm['data'][1])
            nicehashdatalist.append(nicehashdata)
            return 0
        except Exception as e:
            return 1


def publishtomqtt():
    client = mqtt.Client()
    client.on_connect = on_connect

    nicehashdatalist.clear()

    if config.brokerUser != "" and config.brokerPassword != "":
        client.username_pw_set(username=config.brokerUser, password=config.brokerPassword)

    client.connect(config.brokerHost, config.brokerPort, 60)

    response = requests.get("https://api.nicehash.com/api?method=stats.provider.ex&addr=" + config.walletaddress)
    nicehashjsondata = json.loads(response.text)

    deserializenicehash(nicehashjsondata)

    client.publish(config.brokerTopic + "/hashrate", nicehashdatalist.hashratetotal())
    sleep(1)
    client.publish(config.brokerTopic + "/pendingbalance", nicehashdatalist.balancetotal())
    sleep(1)
    client.publish(config.brokerTopic + "/pendingbalanceUSD", nicehashdatalist.balanceusdtotal())
    sleep(1)
    client.publish(config.brokerTopic + "/jsonvalues", "{\"Hashrate\":\"" + str(nicehashdatalist.hashratetotal()) + "\"" + ",\"Pending Balance\":\"" + str(nicehashdatalist.balancetotal()) + "\"" + ",\"Pending Balance USD\":\"" + str(nicehashdatalist.balanceusdtotal()) + "\"}")
    client.loop_stop()
    client.disconnect()


while 1 == 1:
    publishtomqtt()
    print(str(datetime.datetime.now()) + ": Publishing again in " + str(config.brokerPublishFrequency) + " seconds")
    sleep(config.brokerPublishFrequency)
