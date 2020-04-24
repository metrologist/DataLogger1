#simulates return of temperature and humidity
import math
import time
import random

import telnetlib
import sys

HOST = '172.16.52.172'


def vsl_reading2():
	t = time.time()  # time in seconds since epoch
	w = 2 * math.pi /1200  # 20 minute cycle
	temp = 20.0 + math.sin(w*t) +random.gauss(0, 0.1)
	hum = 45.0 + 10*math.cos(w*t) + random.gauss(0, 1)
	return (temp, hum)

def vsl_reading():
    tn = telnetlib.Telnet(HOST)
    try:
        tn.read_until(b'\r\nHMT330 / 5.16\r\n>')
    except:
        print('telnet error on setup ',sys.exc_info())
        return(0.0, 0.0)
    tn.write(b'send\r')
    time.sleep(1)
    while True:
        try:
            line = tn.read_until(b'\r\n', timeout=1)
        except:
            print('telnet error on reading ', sys.exc_info())
            return(0.0, 0.0)
        if(b'C') in line:
            break
    vsloutput = line.decode('ascii')
    temp = float(vsloutput[37:42])
    hum = float(vsloutput[24:29])
    return(temp, hum)

if __name__ == '__main__':
	print(vsl_reading())
	
