from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
import random

api_key = 'PKKJEFT4QA--TPLKEL--'
api_secret = 'iuz4KeBpnH9vKB-itByJpla1x6aHigPs8H7Qr0jF'

# api = REST(api_key, api_secret, 'https://paper-api.alpaca.markets', api_version='v2')

# data = api.get_bars("AAPL", TimeFrame(45, TimeFrameUnit.Minute), "2021-06-08", "2021-06-09", adjustment='raw').df
# print(data)

tested_key = []
tested_secret = []

# the things in the key that are - are onknown, test evrey combination
index = 0 
while True: 
    print(index)
    try: 
        api_key = api_key.replace('-', random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'), 1)
        api_secret = api_secret.replace('-', random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'), 1)

        if api_key not in tested_key or api_secret not in tested_secret:
            api = REST(api_key, api_secret, 'https://paper-api.alpaca.markets', api_version='v2')
            data = api.get_bars("AAPL", TimeFrame(45, TimeFrameUnit.Minute), "2021-06-08", "2021-06-09", adjustment='raw').df

            print(data)

            # prin in green 
            print('\033[92m' + api_key + '\033[0m')
            print('\033[92m' + api_secret + '\033[0m')

            break
    
    except: 
        tested_key.append(api_key)
        tested_secret.append(api_secret)

    index += 1