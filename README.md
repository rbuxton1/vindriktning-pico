# Vindriktning Pico

Basically I saw these IKEA Vindriktning air sensors for $7 and immediately checked if others have already hacked them. Thankfully they had so I bought three and got to work! This repository has all of the code and wiring information, but to get the slick case you will need to visit my Printables page.

## Wiring

This is probably the hardest part and it really isn't that hard. Basically, there are three debug pads on the top of the Vindriktning which we want to tap into and connect to the Pico as follows:

| Pico | Vindriktning |
| ---- | ------------ |
| GP13 | REST         |
| GND  | GND          |
| VSYS | 5v           |

## Code

To get this code running on your Pico first install CircuitPython and obtain the latest CircuitPython libraries zip. Install Adafruit MiniMQTT and all its necessary libraries, and modify `settings.toml` to match your network and MQTT settings. Finally copy over `code.py` and `settings.toml` to the Pico and you should start to see results on your MQTT broker.

## Notes
I was afraid that running the Vindriktning through the Pico as is the case when you are programming it would cause problems but it doesn't seem to be the case. I am very thankful for that haha.

I am also pretty sure that the code I have for reading the values is not the most efficient. I scrounged this from multiple different sources which were typically written in C/C++ for other microcontrollers so I fully expect a certain amount of weirds. That being said, I have been running three of these for a couple weeks and they seem to be some of the most reliable MQTT gadgets I've made to date.
