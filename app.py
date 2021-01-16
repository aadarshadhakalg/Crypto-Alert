from flask import Flask
import requests
import json
from string import Template
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import os
from twilio.rest import Client


def sendMsg(name,value):
    text = 'The Value for {name} has exceeded {value}'.format(name=name,value=value)
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
                .create(
                     body=text,
                     from_='+17633163171',
                     to='+9779869698962'
                 )

    print(message.sid)



def sensor():
    print('sensor')
    exceed = True
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.request("GET", url)
    
    response_data = response.text
    
    decoded_data = json.loads(response_data)

    for val in decoded_data:
        if(val['symbol'] == 'BTCUSDT'):
            global bitcoin
            bitcoin = val['price']
            if(not exceed):
                if(float(bitcoin) > 37500.0):
                    exceed = True
                    sendMsg('Bitcoin',bitcoin)
            elif (exceed):
                if(float(bitcoin) < 37500.0):
                    exceed = False
                    sendMsg('Bitcoin',bitcoin)
            

        elif(val['symbol'] == 'BNBUSDT'):
            global binance
            binance = val['price']
        
        elif(val['symbol'] == 'ETHUSDT'):
            global ethereum
            ethereum = val['price']
        
        elif(val['symbol'] == 'GRTUSDT'):
            global thegraph
            thegraph = val['price']

        elif(val['symbol'] == 'LINKUSDT'):
            global chainlink
            chainlink = val['price']


sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',seconds=10)

app = Flask(__name__)

@app.route('/')
def hello_world():
    template = Template("""
<html>
<head>
<style>
table {
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
</head>
<body>

<h2>Aviyan Koirala's Bitcoin Tracker</h2>

<table>
  <tr>
    <th>Currency</th>
    <th>Price</th>
  </tr>
  <tr>
    <td>Bitcoin</td>
    <td>$bitcoin</td>
  </tr>
  <tr>
    <td>Binance</td>
    <td>$binance</td>
  </tr>
  <tr>
    <td>Ethereum</td>
    <td>$ethereum</td>
  </tr>
  <tr>
    <td>The Graph</td>
    <td>$thegraph</td>
  </tr>
  <tr>
    <td>Chainlink</td>
    <td>$chainlink</td>
  </tr>
</table>

</body>
</html> 
    """)

    return template.substitute(bitcoin=bitcoin,ethereum=ethereum,binance=binance,thegraph=thegraph,chainlink=chainlink)

if __name__ == "__main__":
    app.run(threaded=True, port=5000,debug=True)
