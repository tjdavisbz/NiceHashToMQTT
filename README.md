# NiceHashToMQTT
Python scripts to publish NiceHash json API data for a wallet to an MQTT broker

Simply with the config.py.example file with your information and then save it as config.py.  

MQTT data will be published to your broker using the root topic.  The current sub-topics are
currently published:

1.  hashrate - The sum of the hashrates for all mining algorithms in use, in MH/s.
2.  pendingbalance - The sum of your pending balance for all mining algorithms in BTC.
3.  pendingbalanceUSD - The sum of your pending balance for all mining algorithms in USD.
4.  jsonvalues - A JSON formatted representation of all above values.

## Here is my use case for this:

I am running Nicehash on a Windows OS.  I'm not a big fan of Windows and this is my only Windows workstation
but I chose it because it is much easier to overclock and setup in Windows.  Because it's in Windows,
I have the issues that come along with that.  The two main issues are:

1.  One or more GPU will randomly go offline and the only way I have found to bring it back is to reboot.
2.  I'm using a TP-Link wireless card for now and it will randomly stop working and the only fix is to reboot.

These are problems I don't think I would have on Linux or MacOS but I'm taking the good with the bad.  At any rate,
I created this Python library to publish my hashrate to MQTT.  I am running Home Assistant so I added hashate as a
sensor and have a Node-Red flow that checks my hashrate every 15 minutes.  If it is enough below the baseline rate to
signify that at least one GPU is offline (My GPUs do around 32MH/s) then it checks again in 1 minutes then again in 2
minutes and, if it is still too low, it powers off the smart switch that my mining rig is plugged into, waits 10
seconds, then powers it back on.  I have the workstation to autologin, restore overclocking values on the GPUs
and open NiceHash and start mining.  This solution has worked and improved my mining efficiency termendously because
now when something goes wrong it is fixed within a maximum of 18 minutes.

## Roadmap

This is very much still a work in progress, here are my current plans for future changes:

1.  Create a Nicehash class that the JSON response can be fully deserialized to.
2.  Add more fields to parse and publish to MQTT


## Feature Requests
I would love to enhance this to make it more usable for others if needed.  Please feel free to submit any requests
and I will take a look.

## Feedback

I have been a developer for several years but have only dabbled in Python.  I'm starting to use it a lot now with
home automation but have a lot to learn.  I welcome feedback on how I could have done things better.
