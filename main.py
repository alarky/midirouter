#!/usr/bin/env python
import time
import subprocess
import itertools
from pprint import pprint

def cmd(command: str):
    return subprocess.run(command, shell=True, check=True, capture_output=True)

def led_heartbeat():
    cmd(f"echo heartbeat > /sys/class/leds/led0/trigger")

def led_timer():
    cmd(f"echo timer > /sys/class/leds/led0/trigger")

def led_on():
    cmd(f"echo default-on > /sys/class/leds/led0/trigger")

def get_clients():
    clients = []
    for line in cmd("aconnect -l").stdout.decode().split("\n"):
        if not line.startswith("client "):
            continue
        (cid, cname) = line.split(": ", 1)
        if cname in ("'System' [type=kernel]", "'Midi Through' [type=kernel]"):
            continue
        cid = cid.split(" ")[1]
        clients.append({"id": cid, "name": cname})
    return clients

def main():
    led_timer()
    pre_cnt = 0
    while True:
        clients = get_clients()
        cnt = len(clients)

        if cnt >= 2:
            led_on()

            if cnt > pre_cnt:
                for a, b in itertools.combinations(clients, 2):
                    pprint(a)
                    pprint(b)
                    cmd(f"aconnect {a['id']} {b['id']}")
                    cmd(f"aconnect {b['id']} {a['id']}")

        elif cnt == 1:
            led_heartbeat()
        else:
            led_timer()

        pre_cnt = cnt
        time.sleep(1)

if __name__ == "__main__":
    main()


