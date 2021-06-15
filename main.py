"""
IMPORTANT : THE NEXT 5 LINES ARE TO BE IGNORED, DO NOT MODIFY

Why these imports are required:
- Pynput imports are required for listening to key events and mouse clicking
- Random is required for the random_interval part of the program
- Time import is required for waiting or sleeping before the next click
- threading is required to start the main loop in another thread to prevent it getting in the way of the main one
"""
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import random
import time
from threading import Thread

# VARIABLES : MODIFY THESE VARIABLES TO CHANGE HOW THE AUTOCLICKER WORKS
random_interval = False  # Whether you want a random interval or not [True or False]
start_stop_key = 'p'  # The key to start or stop the autoclicker
program_stop_key = 'o'  # The key to completely stop the program

"""
If you use random interval, set interval delay (integer > 1) [seconds]

This is the time between each click, 
when random interval is on, it will choose between a number from 1 to this interval delay

When it is off, this will just be the time interval between each click
"""
interval_delay = 1

# !!!! DO NOT MODIFY ANYTHING HEREAFTER !!!

# Set mouse for clicking, could also change the button to a specific key
mouse = Controller()
button = Button.left


class Click:  # Click class, used a class to store the variables so I can access them anytime
    def __init__(self, click_num=1):  # Init function, function runs when the class is called
        # These two variables are set for the main loop, should_stop is the
        # temporary stop/start trigger and can_run is the permanent stop variable
        self.should_stop = True
        self.can_run = True

        # Check click_num, I haven't tested click_num for anything above 1 lol
        if click_num > 5:
            print("WARNING : CLICK NUM IS ABOVE 5, SETTING TO DEFAULT")
            self.click_num = 1
        else:
            self.click_num = click_num

    # Getter functions
    def get_status(self):
        return self.should_stop

    # Setter functions
    def start(self):
        self.should_stop = False

    def stop(self):
        self.should_stop = True

    def complete_stop(self):
        self.can_run = False

    # Main loop
    def run(self):
        # If the can_run variable is true
        while self.can_run:
            #
            if not self.should_stop:
                mouse.click(button=button, count=self.click_num)

                # Random interval, could do a ternary operator but it'll look unclean
                if random_interval:
                    time.sleep(random.randrange(interval_delay * 100) / 100)
                else:
                    time.sleep(interval_delay)


def on_press(key, local_class):
    if key == KeyCode.from_char(start_stop_key):
        if not local_class.get_status():
            print("Autoclicker Stopped")
            local_class.stop()
        else:
            print("Autoclicker Started")
            local_class.start()

    elif key == KeyCode.from_char(program_stop_key):
        print("Exited Program")
        local_class.complete_stop()


def main():
    print("Starting Autoclicker..")
    time.sleep(0.5)
    print("\n====Keybinds====")
    print("{} for start / stop".format(start_stop_key))
    print("{} for program stop".format(program_stop_key))

    time.sleep(1)

    # Daemon threads exit automatically when the main program is stopped
    click_class = Click(1)
    thread = Thread(target=click_class.run, daemon=True)
    print("\nStarting Thread..")
    thread.start()
    print("Started.")

    print("Starting Listener..")
    listener = Listener(on_press=lambda event: on_press(event, click_class))
    listener.start()
    print("Started.")

    print("Press {} to start the program...".format(start_stop_key))
    thread.join()

    print("\n\n====== Events ======")


if __name__ == "__main__":
    main()
