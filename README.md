# ASHER
A program designed to work with a Raspberry Pi if your treadmill info display breaks

ASHER stands for **Automated System to Harness Expected Results**. Why ASHER and not something else? I'm not sure. Maybe it sounds cool to me. ASHER is designed as a replacement for an info display on a treadmill in case it breaks. Who knows? Maybe your treadmill is from the 90s and the display stopped working.

## Setup

It's designed to work with the Raspberry Pi's GPIO pins. When pin 2 and GND are shorted (normally used for a button), it will take that as the belt has rotated one time. It then uses how fast the belt rotated to calculate all the useful information like distance and speed in MPH and Minute Mile pace.

You must setup the physical system first. All you have to do is stick a metal piece to your belt and when the belt passes it must short the two pins. This can be done with wires that are taped down that to the treadmill that go from the RPi to the place where they will hit the belt when it passes. Also, you will have to have some kind of monitor and input device for the program.

## Using the Program

After that, start up the program with Python, start the workout, and it should work. For right now, you might have to use a keyboard to start the workout which is silly, but you might be able to use a little joystick. You use enter to start and exit the workout.

To stop the workout and show results, you have to press CTRL+C, so I'm not sure how you would want to set that up.

This program was mainly designed for myself, but I decided to put it on GitHub in case anyone else might benefit from it.