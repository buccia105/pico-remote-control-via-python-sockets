# pico-remote-control-via-python-sockets
Hello everyone as we all know, every day can be a learning day, that is a pretty sure thing when learning in school.
In fact this project was done as a class project from my electronics professor in high school, he wanted this project to be done in java and an arduino,
but I had other plans and done it in Python, MicroPython and a Raspberry Pi Pico 2W, doing so I removed the second computer that acted as the server.
The scope of this project is to learn communication over any LAN, WAN, WLAN.

# Starting on with the circuit and pinout

For the circuit we will need only 2 resistors, a white LED, and a photoresistor (CdS),
I will not include the values of this components because I'd like to give a small challenge.
The whole circuit should be enclosed in a dark box as we need to know from the voltage of the photoresistor when the led is on, so we'll know at what exact voltage
the led starts to turn on.
As the Pico doesn't have a DAC i used a PWM pin by modulating the duty cycle to have the exact voltage that the user requests, obiusly it has some limitations the major one
is that you can't exceede 3.3V of output.

<img width="929" alt="Schematics and Pinout" src="https://github.com/user-attachments/assets/a4c94ede-eccc-45b9-8992-7834046d6fcd" />

# The code
As you can see it's already done, you don't have much to do, you only need to define your SSID, PASSWORD, and the ip address of the server, you can also change the TCP port, mess around with the protocols, if you want to improve it then push the improvements here on GitHub, it would be nice for everyone.

Now seriously, as for the *main.py*, you need to change SSID and PASSWORD, if you want also the PORT. afterwards just upload it on your Pico running MicroPython, but this code is pretty cross platform with small modifications on the libraries and pin initialaization, you just need to run it on a MycroPython board.

For the client side, after you changed the HOST, and on the same network and port as your Pico, just run the code on any PC or Mac that has Python installed, and then just enjoy it.
