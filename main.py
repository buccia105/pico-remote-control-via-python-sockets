# This code connects to a WiFi network and creates a TCP socket. 
# It receives a voltage value from the client, sets the DAC output to this voltage, 
# and then performs measurements using ADC. The measured values are sent back to the client.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import network
import usocket as socket
import time
from machine import ADC, PWM, Pin

##Global variables

#set your wifi credentials
SSID = 'your ssid' #set your ssid
PASSWORD = 'your password' #set your wifi password

#set the host and port of the server socket
HOST = '' #statemant to bind to all available interfaces
PORT = 500 #set your preferred port

#initialization of the gpio pins
on_led = Pin('LED', Pin.OUT)
on_led.value(0)
sensor = ADC(Pin(26))
led_o = ADC(Pin(27))
dac = PWM(Pin(22))
dac.freq(5000)

#function to connect to the wifi network
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print('Connecting to network...')
        time.sleep(1)

    print('Network connected!')
    print('IP address:', wlan.ifconfig()[0])
    on_led.value(1)

#function to set the output voltage
def set_dac(voltage):
    if 0 <= voltage <= 3.3:
        duty_cycle = int((voltage / 3.3) * 65535)
        dac.duty_u16(duty_cycle)
    else:
        print('out of range')

#function to decode the data to float
def float_decoder(data):
    return float(data.decode('utf-8'))

#function to encode floats to data
def float_encoder(floatnumber):
    string = str(floatnumber)
    return string.encode('utf-8')

##Main code
#connecting to the wifi network
connect_to_wifi(SSID, PASSWORD)

#creating the server tcp socket and listening for incoming connections 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

while True:
    
    #accepting the incoming connection
    conn, addr = s.accept()
    #printing the address of the connected client
    print("Connected to: ", addr)
    
    #receiving the data from the client
    data = conn.recv(1024)
    v_in = float_decoder(data)

    #setting the output voltage
    if 0 <= v_in <= 3.3:
        set_dac(v_in)
        conn.sendall(b'Voltage was properly set')
        time.sleep(1)
    else:
        conn.sendall(b'Out of range')
    time.sleep(1)

    #reading the sensor and led values
    sensor_val = sensor.read_u16()
    sensor_v = (sensor_val / 65535) * 5.0
    print(sensor_v)
    
    led_val = led_o.read_u16()
    led_v = (led_val / 65535) * v_in
    print(led_v)
    
    #sending the sensor and led values back to the client
    conn.sendall(float_encoder(sensor_v))
    conn.sendall(float_encoder(led_v))
