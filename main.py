"""
IMPORTANT : THE NEXT 5 LINES ARE TO BE IGNORED, DO NOT MODIFY

Why these imports are required:
- Pynput imports are required for listening to key events and mouse clicking
- Random is required for the random_interval part of the program
- Time import is required for waiting or sleeping before the next click
- threading is required to start the main loop in another thread to prevent it getting in the way of the main one
"""
from pynput.mouse import Button, Controller
from pynput.keyboard import KeyCode
import pynput.keyboard as keyboard
import random
import time
# import tracemalloc

from threading import *
# from threading import Thread

# Set mouse for clicking, could also change the button to a specific key
mouse = Controller()


# VARIABLES : MODIFY THESE VARIABLES TO CHANGE HOW THE AUTOCLICKER WORKS
random_interval = False  # Whether you want a random interval or not [True or False]
start_stop_key = 'p'  # The key to start or stop the autoclicker
program_stop_key = 'o'  # The key to completely stop the program
click_num = 1 # The amount of times to click the key
button = Button.left # The Button that will be pressed for the autoclicker

"""
If you use random interval, set interval delay (integer > 1) [seconds]

This is the time between each click, 
when random interval is on, it will choose between a number from 1 to this interval delay

When it is off, this will just be the time interval between each click
"""
interval_delay = 20

# !!!! DO NOT MODIFY ANYTHING HEREAFTER !!!

if click_num > 5: # Don't allow user to click more than 5 times once because it will cause unexpected results
    print("WARNING : CLICK NUM IS ABOVE 5, SETTING TO DEFAULT")
    click_num = 1

class Click:  # Click class, used a class to store the variables so I can access them anytime
    def __init__(self):  # Init function, function runs when the class is called
        # can_run is the stop variable
        self.can_run = False
        self.complete_stop = False
        self.condition_object = Condition()


    def on_press(self, key):
        if key == KeyCode.from_char(start_stop_key):
            if self.can_run:
                self.can_run = False
                print("Autoclicker Stopped")
            else:
                print("Autoclicker Started")
                self.can_run = True
                self.condition_object.acquire()
                self.condition_object.notify()
                self.condition_object.release()

        elif key == KeyCode.from_char(program_stop_key):
            print("Exited Program")
            self.complete_stop = True
            self.condition_object.acquire()
            self.condition_object.notify()
            self.condition_object.release()
            # tracemalloc.stop()

    # Main loop
    def run(self):
        self.condition_object.acquire()
        # If the can_run variable is true
        while True: # TRY PAUSE THE THREAD
            if self.complete_stop:
                    return

            if self.can_run:
                mouse.click(button=button, count=click_num)

                # Random interval, could do a ternary operator but it'll look unclean
                if random_interval:
                    time.sleep(random.randrange(interval_delay * 100) / 100)
                else:
                    time.sleep(interval_delay)
            else:
                self.condition_object.wait()
            

def main():
    print("Starting Autoclicker..")
    time.sleep(0.5)
    print("\n====Keybinds====")
    print(f"{start_stop_key} for start / stop")
    print(f"{program_stop_key} for program stop")

    time.sleep(1)

    # Daemon threads exit automatically when the main program is stopped
    click_class = Click()
    thread = Thread(target=click_class.run, daemon=True)
    print("\nStarting Thread..")
    thread.start()
    print("Started Thread.")
    print("Starting Listener..")

    # Lambda event because I need to pass args to the on_press function, found this method on stackoverflow
    with keyboard.Listener(on_press=lambda event: click_class.on_press(event)) as listener:
        print("Started Listener.")
        print(f"Press {start_stop_key} to start the program...")
        # print(f"Resources: {tracemalloc.get_traced_memory()}")
        print("\n\n====== Events ======")
        thread.join()
        # tracemalloc.stop()


if __name__ == "__main__":
    # tracemalloc.start()
    main()

