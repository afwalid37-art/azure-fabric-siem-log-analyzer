import json
import random
from datetime import datetime, timedelta

# CONFIGURATION
# We simulate 1000 events. 
# 95% will be normal. 5% will be a "Brute Force" attack from a specific IP.
TOTAL_EVENTS = 5000
ATTACKER_IP = "192.168.1.105"
NORMAL_IPS = ["10.0.0.5", "10.0.0.6", "192.168.1.20", "172.16.0.50"]
USERS = ["Admin", "System", "HR_User", "CEO_Backup"]

def generate_log():
    data = []
    start_time = datetime.now() - timedelta(days=1)
    
    print(f"Generating {TOTAL_EVENTS} logs...")
    
    for i in range(TOTAL_EVENTS):
        # 1. Decide if this is a normal event or an attack event
        is_attack = random.random() < 0.05 # 5% chance of attack
        
        current_time = start_time + timedelta(seconds=i*5) # Events happen every 5 seconds
        
        if is_attack:
            # ATTACK PATTERN: Event 4625 (Failed Login) from the Bad IP
            event_id = 4625 
            ip = ATTACKER_IP
            user = "Admin" # Attacker trying to guess Admin password
            status = "0xC000006D" # Bad Password
        else:
            # NORMAL PATTERN: Mostly 4624 (Success) or random noise
            event_id = random.choice([4624, 4624, 4624, 4634, 4672]) 
            ip = random.choice(NORMAL_IPS)
            user = random.choice(USERS)
            status = "0x0" # Success

        # 2. Build the JSON object (Mimicking Windows Event Log structure)
        log_entry = {
            "TimeCreated": current_time.isoformat(),
            "EventID": event_id,
            "Computer": "SRV-FINANCE-01",
            "EventData": {
                "IpAddress": ip,
                "TargetUserName": user,
                "Status": status,
                "LogonType": 3 # Network Logon
            }
        }
        data.append(log_entry)

    # 3. Save to file
    with open("server_logs.json", "w") as f:
        # Write as "JSON Lines" (one JSON object per line) - Best for Big Data
        for entry in data:
            f.write(json.dumps(entry) + "\n")
    
    print("Done! 'server_logs.json' created with hidden attack patterns.")

if __name__ == "__main__":
    generate_log()