import math
import os
import time
from gpiozero import Button
from threading import Thread
from time import sleep

belt_button = Button(2)

# 15 is the length of my belt in feet
belt_length = 8.0416666666667
# My lowest treadmill speed takes about 40 seconds to pass
timeout = 40


def display(original_time=None, total_distance=None, current_speed=None, prev_rev_time=None):
    os.system('clear')
    print('Current Workout Information')
    print('')
    if original_time is None:
        print(f'Time Elapsed: 00:00:00')
        print('')
        print('Distance')
        print(f'Miles: --')
        print(f'Kilometers: --')
        print('')
        print('Current Speed')
        print(f'M/H: --')
        print(f'KM/H: --')
        print('')
        print('Pace')
        print(f'Mile: --:--')
        print(f'Kilometer: --:--')
    elif current_speed == 0:
        seconds_elapsed = time.time() - original_time
        time_elapsed = increment(seconds_elapsed)
        mi = total_distance / 5280
        km = total_distance / 3280.84
        print(f'Time Elapsed: {time_elapsed}')
        print('')
        print('Distance')
        print(f'Miles: {round(mi, 2)}')
        print(f'Kilometers: {round(km, 2)}')
        print('')
        print('Current Speed')
        print(f'M/H: 0')
        print(f'KM/H: 0')
        print('')
        print('Pace')
        print(f'Mile: 00:00')
        print(f'Kilometer: 00:00')
    else:
        seconds_elapsed = time.time() - original_time
        time_elapsed = increment(seconds_elapsed)
        mi = total_distance / 5280
        km = total_distance / 3280.84
        mph = current_speed / 1.46667
        kmph = current_speed * 1.09728
        min_mi = 60 / mph
        min_km = 60 / kmph
        mi_pace_min = math.floor(min_mi)
        mi_pace_sec = round((min_mi * 60) % 60)
        if mi_pace_sec < 10:
            mi_pace_sec = f'0{mi_pace_sec}'
        km_pace_min = math.floor(min_km)
        km_pace_sec = round((min_km * 60) % 60)
        if km_pace_sec < 10:
            km_pace_sec = f'0{km_pace_sec}'
        print(f'Time Elapsed: {time_elapsed}')
        print('')
        print('Distance')
        print(f'Miles: {round(mi, 2)}')
        print(f'Kilometers: {round(km, 2)}')
        print('')
        print('Current Speed')
        print(f'M/H: {round(mph, 2)}')
        print(f'KM/H: {round(kmph, 2)}')
        print('')
        print('Pace')
        print(f'Mile: {mi_pace_min}:{mi_pace_sec}')
        print(f'Kilometer: {km_pace_min}:{km_pace_sec}')


def increment(seconds_elapsed):
    seconds_elapsed = math.floor(seconds_elapsed)
    h = seconds_elapsed // 3600
    m = (seconds_elapsed // 60) % 60
    s = seconds_elapsed % 60
    if h < 10:
        h = f'0{h}'
    if m < 10:
        m = f'0{m}'
    if s < 10:
        s = f'0{s}'
    return f'{h}:{m}:{s}'


def rev_counter():
    original_time = time.time()
    prev_rev_time = original_time
    revolutions = 0
    try:
        display()
        while True:
            # Times out after 40 seconds
            # Belt should be stopped if it's taking that long
            belt_button.wait_for_press(timeout)
            # Code when debugging
            # sleep(1)
            rev_seconds = time.time() - prev_rev_time
            prev_rev_time = time.time()
            if rev_seconds < timeout:
                revolutions += 1
            thread = Thread(target=update_display, args=(original_time, prev_rev_time, rev_seconds, revolutions))
            thread.start()    
            sleep(0.25)
    except KeyboardInterrupt:
        total_distance = belt_length * revolutions
        results(original_time, prev_rev_time, total_distance)


def update_display(original_time, prev_rev_time, rev_seconds, revolutions):
    # Feet * rev count
    # 15 = Length of my treadmill in feet
    total_distance = belt_length * revolutions
    if rev_seconds >= timeout:
        # Set current speed to zero if timed out
        current_speed = 0
    else:
        # Feet / second
        current_speed = belt_length / rev_seconds
    display(original_time, total_distance, current_speed, prev_rev_time)


def results(original_time, prev_rev_time, total_distance):
    try:
        os.system('clear')
        seconds_elapsed = time.time() - original_time
        time_elapsed = increment(seconds_elapsed)
        print('Workout Results')
        print('')
        if total_distance == 0:
            print(f'Total Time: {time_elapsed}')
            print('')
            print('Distance')
            print(f'Miles: 0')
            print(f'Kilometers: 0')
            print('')
            print('Average Speed')
            print(f'M/H: 0')
            print(f'KM/H: 0')
            print('')
            print('Average Pace')
            print(f'Mile: 00:00')
            print(f'Kilometer: 00:00')
        else:
            working_seconds_elapsed = prev_rev_time - original_time
            average_speed = total_distance / working_seconds_elapsed
            mi = total_distance / 5280
            km = total_distance / 3280.84
            mph = average_speed / 1.46667
            kmph = average_speed * 1.09728
            min_mi = 60 / mph
            min_km = 60 / kmph
            mi_pace_min = math.floor(min_mi)
            mi_pace_sec = round((min_mi * 60) % 60)
            if mi_pace_sec < 10:
                mi_pace_sec = f'0{mi_pace_sec}'
            km_pace_min = math.floor(min_km)
            km_pace_sec = round((min_km * 60) % 60)
            if km_pace_sec < 10:
                km_pace_sec = f'0{km_pace_sec}'
            print(f'Total Time: {time_elapsed}')
            print('')
            print('Distance')
            print(f'Miles: {round(mi, 2)}')
            print(f'Kilometers: {round(km, 2)}')
            print('')
            print('Average Speed')
            print(f'M/H: {round(mph, 2)}')
            print(f'KM/H: {round(kmph, 2)}')
            print('')
            print('Average Pace')
            print(f'Mile: {mi_pace_min}:{mi_pace_sec}')
            print(f'Kilometer: {km_pace_min}:{km_pace_sec}')
        print('')
        input('Exit ')
        os.system('clear')
    except KeyboardInterrupt:
        os.system('clear')


def main():
    os.system('clear')
    while True:
        try:
            print('ASHER Treadmill Workout Program')
            print('')
            input('Start Workout ')
            rev_counter()
        except KeyboardInterrupt:
            print('\n')
            print('Quitting... ')
            break


if __name__ == '__main__':
    main()
