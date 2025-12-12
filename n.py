import requests
import random
import json
import time
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from gzip import decompress
from ssl import CERT_NONE
from websocket import create_connection
from queue import Queue

# Color codes
E, B, G, S, F, R, Y, Bl, P, C, W, PN = '\033[1;31m', '\033[2;36m', '\033[1;32m', '\033[1;33m', '\033[1;32m', '\033[1;31m', '\033[1;33m', '\033[1;34m', '\033[1;35m', '\033[1;36m', '\033[1;37m', '\033[1;35m'

# Predefined Telegram credentials
CHAT_ID = "8391674276"
TOKEN = "8060081718:AAGsnkkJXY-fZJmpg9HcvnXWPQ2DZz1ZC7E"

# Global counters and storage
failed, success, retry = 0, 0, 0
accounts = Queue()
batch_size = 10

# Optimized username generation
def generate_username():
    return random.choice('qwertyuioplkjhgfdsazxcvbnm') + ''.join(random.choices('qwertyuioplkjhgfdsazxcvbnm1234567890', k=12))

# Batch Telegram sending
def send_to_telegram(batch):
    try:
        message = "\n".join(batch)
        t = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={
            "chat_id": CHAT_ID,
            "text": f"⋘─────━**━─────⋙\nformat >> USER:PASS \naccounts>> \n{message} \n\njoin >> @Indian_Hackers_Team\n⋘─────━❤️🌚━─────⋙\n𝐁𝐘 :  @Indian_Hackers_Team"
        }, timeout=5)
        if t.status_code == 200:
            print(f'{G}Batch of accounts sent to Telegram successfully')
        else:
            print(f"{R}Telegram send failed: {t.status_code}")
    except Exception as e:
        print(f"{R}Telegram error: {e}")

# Optimized worker function
def work():
    global failed, success, retry
    username = generate_username()
    
    try:
        # Connection pooling could be implemented here if supported by server
        con = create_connection("wss://195.13.182.213/Auth", 
                              header={
                                  "app": "com.safeum.android",
                                  "sessionId": "b6cbb22d-06ca-41ff-8fda-c0ddeb148195",
                                  "time": "2023-04-30 12:13:32"
                              }, 
                              sslopt={"cert_reqs": CERT_NONE})
        
        con.send(json.dumps({
            "action": "Register",
            "subaction": "Desktop",
            "locale": "en_GB",
            "gmt": "+02",
            "password": {
                "m1x": "503c73d12b354f86ff9706b2114704380876f59f1444133e62ca27b5ee8127cc",
                "m1y": "6387ae32b7087257452ae27fc8a925ddd6ba31d955639838249c02b3de175dfc",
                "m2": "219d1d9b049550f26a6c7b7914a44da1b5c931eff8692dbfe3127eeb1a922fcf",
                "iv": "e38cb9e83aef6ceb60a7a71493317903",
                "message": "0d99759f972c527722a18a74b3e0b3c6060fe1be3ad53581a7692ff67b7bb651a18cde40552972d6d0b1482e119abde6203f5ab4985940da19bb998bb73f523806ed67cc6c9dbd310fd59fedee420f32"
            },
            "magicword": {
                "m1x": "04eb364e4ef79f31f3e95df2a956e9c72ddc7b8ed4bf965f4cea42739dbe8a4a",
                "m1y": "ef1608faa151cb7989b0ba7f57b39822d7b282511a77c4d7a33afe8165bdc1ab",
                "m2": "4b4d1468bfaf01a82c574ea71c44052d3ecb7c2866a2ced102d0a1a55901c94b",
                "iv": "b31d0165dde6b3d204263d6ea4b96789",
                "message": "8c6ec7ce0b9108d882bb076be6e49fe2"
            },
            "magicwordhint": "0000",
            "login": username,
            "devicename": "Xiaomi Redmi Note 8 Pro",
            "softwareversion": "1.1.0.1380",
            "nickname": "hvtctchnjvfxfx",
            "os": "AND",
            "deviceuid": "c72d110c1ae40d50",
            "devicepushuid": "*dxT6B6Solm0:APA91bHqL8wxzlyKHckKxMDz66HmUqmxCPAVKBDrs8KcxCAjwdpxIPTCfRmeEw8Jks_q13vOSFsOVjCVhb-CkkKmTUsaiS7YOYHQS_pbH1g6P4N-jlnRzySQwGvqMP1gxRVksHiOXKKP",
            "osversion": "and_11.0.0",
            "id": "1734805700"
        }))
        
        response = decompress(con.recv()).decode('utf-8')
        con.close()  # Close connection immediately
        
        if '"status":"Success"' in response:
            success += 1
            account = f"{username}:hhhh"
            accounts.put(account)
            print(f"{G}Created: {username}")
            
            with open('SafeUM_@Indian_Hackers_Team.txt', 'a') as f:
                f.write(f"{account} | TG : @Indian_Hackers_Team\n")
            
            # Process batch when queue has enough items
            if accounts.qsize() >= batch_size:
                batch = []
                for _ in range(batch_size):
                    batch.append(accounts.get())
                send_to_telegram(batch)
        else:
            failed += 1
            
    except Exception as e:
        retry += 1
        print(f"{R}Error: {e}")

# Main execution
def main():
    print(f"{C}Starting Account Creator...")
    print(f"{Y}Using Chat ID: {CHAT_ID}")
    print(f"{Y}Using Token: {TOKEN[:10]}...{TOKEN[-5:]}")
    
    executor = ThreadPoolExecutor(max_workers=500)  # Reduced workers for better resource management
    
    try:
        while True:
            executor.submit(work)
            time.sleep(0.1)  # Small delay to prevent overwhelming the system
            os.system('clear')
            print(f'\n\n\n{" "*25}Success: {success}\n\n\n{" "*25}Failed: {failed}\n\n\n{" "*25}Retry: {retry}')
            
    except KeyboardInterrupt:
        print(f"{Y}Shutting down...")
        executor.shutdown(wait=False)

if __name__ == "__main__":
    main()
