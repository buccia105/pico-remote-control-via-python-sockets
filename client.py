# This code connects to a remote TCP socket. 
# It sends a voltage value to the server, that sets the DAC output to this voltage, 
# and then performs measurements using ADC. The measured values from the server are sent back to this client.


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

import socket

## Global variables
HOST = '172.20.10.5'    # The remote host
PORT = 500              # The same port as used by the server

## Functions
# Function to decode the data received from the server
def float_decoder(data):
    return float(data.decode('utf-8'))

# Function to encode the data to be sent to the server
def float_encoder(floatnumber):
    string = str(floatnumber)
    return string.encode('utf-8')

## Main

# Create a socket and connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Request the voltage value to be sent to the server
v_in = input("Inserisci la tensione di ingresso: ")

# Send the voltage value to the server
sock.sendall(float_encoder(v_in))

# Receive the confirmation message from the server
conferma = sock.recv(1024) 
print((conferma.decode('utf-8')))

# If the voltage value is out of range, close the socket and exit
if conferma == b'Out of range':
    sock.close()
    exit()

# Receive the measured values from the server and close the socket
sensor_voltage = sock.recv(1024) 
led_voltage = sock.recv(1024)
sock.close()

# Print the measured values
print('Sensor voltage: ', round(float_decoder(sensor_voltage), 5), 'V')
print('LED voltage: ', round(float_decoder(led_voltage), 5), 'V')
