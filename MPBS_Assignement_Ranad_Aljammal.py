################################################ Section 2.1 Real-Time data Logging ########################################################
# This section vosualizes the actual measurements from the ultrasnic ranging module in real time in textual, and visual ways
# It has been decided to use the RPI.GPIO library
# --------------------------------------------- Import the general library calls --------------------------------------------------------- #

# Import the RPI GPIO library by using the alias RPI
import RPi.GPIO as RPI
# Define the pin numbering system as Broadcom Pin Number (BCM)
RPI.setmode(RPI.BCM)
# Import the time library
import time
# Import the random library
import random

#----------------------------------------------------------------------------------------------------------------------------------------- #
######################################## Section 2.1.1 Acquisition of range measurement data ###############################################

# Define the pin-numbers for the Transmitter, and the receiver pins according to the GPIO Header and Pins PI-Trokli Development System
pin_trigger = 16
pin_echo = 12

# Define the trigger pin as an output
RPI.setup(pin_trigger, RPI.OUT, RPI.PUD_OFF)
# Define the echo pin as an input
RPI.setup(pin_echo, RPI.IN, RPI.PUD_OFF)
# We have to make sure that the trigger pin is not sending any pulse signal before we initialize the sensor
RPI.output(pin_trigger, RPI.LOW)

# Define a funciton that returns the measured pulse time
def ultra_sonic_ranging_time_difference(pin_trigger, pin_echo):
    # Initialize the sensor
    print("Initiliazing the sensor")
    time.sleep(2)
    # Activate the trigger to send the pulse signal
    RPI.output(pin_trigger, RPI.HIGH)
    # We set the time of the signal pulse duration with 1 micro-second
    time.sleep(0.00001)
    # Deactivate the trigger pin
    RPI.output(pin_trigger, RPI.LOW)
    # We measure the first time duration (t1) "The first rising edge" as long as the echo-pin is deactivated
    while RPI.input(pin_echo) == 0:
        t1 = time.time()
    # We measure the second time duration (t2) "The second falling edge" as long as the echo-pin is activated
    while RPI.input(pin_echo) == 1:
        t2 = time.time()
    # We measure the time difference between the two falling-rising edges
    measured_pulse_time = t2-t1
    # Return the time difference measured value
    return measured_pulse_time

#----------------------------------------------------------------------------------------------------------------------------------------- #
############################### Section 2.1.2 Visualizing the distance measure on the 7 segment display ####################################
############################################# Section 2.1.2 Actual real time measurement ###################################################

# Import the SevenSegment display library
from Adafruit_LED_Backpack import SevenSegment
# Define SevenSegment object and define the I2C address as (0x70)
sev_seg = SevenSegment.SevenSegment(address=0x70)

# Define a function that scale the measured distance, and show it on the 7SD
def scale_distance_show_7SD(time_difference, update_rate):
    # Initializing the 7SD
    sev_seg.begin()
    # Calculate the distance by inputting the time difference, which was obtained from the previous funciton
    dist = time_difference * 17241 # Distance will be in cm
    dist = (dist/200) * 100 # Scaling the distance
    dist = float(round(dist, 1)) # We assume the distance value is rounded to the nearest single decimal digit (50.23 >> 50.2)
    # Show the actual distance measurment on the console to compare it with the one shown on the 7SD
    print(dist)
    # In case the number is negative
    if dist < 0:
        for i in range(4):
            sev_seg.set_digit(i, '0')
    # Displaying the number between 0 and 10
    elif dist >= 0 and dist < 10:
        dist = str(dist)
        for i in range(2):
            sev_seg.set_digit(i, '0')
        sev_seg.set_digit(2, dist[0])
        sev_seg.set_digit(3, dist[2])
    # Displaying the number between 10 and 100
    elif dist >= 10 and dist < 100:
        dist = str(dist)
        sev_seg.set_digit(0, '0')
        sev_seg.set_digit(1, dist[0])
        sev_seg.set_digit(2, dist[1])
        sev_seg.set_digit(3, dist[3])
    # Displaying the maximum possible number
    elif dist >= 100:
        dist = str(dist)
        sev_seg.set_digit(0, '1')
        sev_seg.set_digit(1, '0')
        sev_seg.set_digit(2, '0')
        sev_seg.set_digit(3, '0')
    sev_seg.set_decimal(2, True)
    sev_seg.write_display()
    time.sleep(update_rate)

############################################### Section 2.1.2 Remotely Keyboard Testing ###################################################

# Define a function that tests the functionality by asking the user to input a random value
def scale_distance_show_7SD_keyboard_test(update_rate):
    # Initializing the 7SD
    sev_seg.begin()
    # Ask the user to enter a floating value between 0 and 100
    random_val = float(input("Please enter a random number between 0 and 100: "))
    # Rounding the value to the nearest decimal digit as requested
    random_val = round(random_val, 1)
    # In case the number is negative
    if random_val < 0:
        for i in range(4):
            sev_seg.set_digit(i, '0')
    # Displaying the number between 0 and 10
    elif random_val >= 0 and random_val < 10:
        random_val = str(random_val)
        for i in range(2):
            sev_seg.set_digit(i, '0')
        sev_seg.set_digit(2, random_val[0])
        sev_seg.set_digit(3, random_val[2])
    # Displaying the number between 10 and 100
    elif random_val >= 10 and random_val < 100:
        random_val = str(random_val)
        sev_seg.set_digit(0, '0')
        sev_seg.set_digit(1, random_val[0])
        sev_seg.set_digit(2, random_val[1])
        sev_seg.set_digit(3, random_val[3])
    # Displaying the maximum possible number
    elif random_val >= 100:
        random_val = str(random_val)
        sev_seg.set_digit(0, '1')
        sev_seg.set_digit(1, '0')
        sev_seg.set_digit(2, '0')
        sev_seg.set_digit(3, '0')
    sev_seg.set_decimal(2, True)
    sev_seg.write_display()
    time.sleep(update_rate)

#------------------------------------------------------------------------------------------------------------------------------------------#
########################## Section 2.1.3 Visualizing the distance measure on the Matrix LED Display (MLD) ##################################

# ------------------------------------------------- Import LUMA library calls ---------------------------------------------------------#
# Import the SPI communicaiton capability from the LUMA
from luma.core.interface.serial import spi, noop
# Import the canvas definition from the LUMA
from luma.core.render import canvas
# Import the device definitions for the MAX7219
from luma.led_matrix.device import max7219
# ----------------------------------------- Setup max 7219 device and Communication ---------------------------------------------------#

# Setup the interface
my_spi_interface = spi(port = 0, device = 1, gpio = noop())
# Setup the device
cascaded = 1
block_orientation = 90
rotate = 0
my_max7219_device = max7219(my_spi_interface, cascaded = cascaded, block_orientaiton = block_orientation, rotate = rotate)

# Define a funciton that scales the measured distance, and show it on the MLD
def matrix_led_display(time_difference, update_rate):
    # --------------------------------------- Obtain the ultrasonic measurment samples ------------------------------------------------- #
    # Calculate the distance by inputting the time difference, which was obtained from the previous funciton
    dist = time_difference * 17241 # Distance will be in cm
    dist = int(round(7*(dist / 195))) # Scaling the distance according to the MLD individual column (e.g. starting with 0, ending with 7)
    # Add the new scaled value "dist" to the pre-defined list "bar_height"
    bar_height.append(dist)
    # Remove the oldest scaled value from the list
    del bar_height[0]
    # Defining a canvas drawing environment
    with canvas(my_max7219_device) as draw:
        for i in range(8):
            draw.line([i, 7 - bar_height[i], i, 7 - bar_height[i]], fill="white")
    time.sleep(update_rate)

# ---------------------------------------------------------------------------------------------------------------------------------------- #
#################################### Section 2.1.4 Test setup for the basic funcitonality of MLD ###########################################

# Define a funciton that scales a random value, and show it on the MLD
def matrix_led_display_test(update_rate):
    # Generate a random floating value (0 to 1) by using the random library
    random_val = random.random()
    # Scale the random value to lie between 0 and 7 as integer value
    dist = random_val * 100
    dist = int(round(dist, 0))
    dist = int(round(dist * 7 / 100))
    # Add the new scaled value "dist" to the pre-defined list "bar_height"
    bar_height.append(dist)
    # Remove the oldest mscaled value from the list
    del bar_height[0]
    # Defining a canvas drawing environment
    with canvas(my_max7219_device) as draw:
        for i in range(0, 8):
            draw.line([i, 7 - bar_height[i], i, 7 - bar_height[i]], fill="white")
    time.sleep(update_rate)

# ---------------------------------------------------------------------------------------------------------------------------------------- #
####################################################### Section 2.2 Update Rate ############################################################

# Define a funciton that asks the user to input an update rate (0 - 9)
def update_rate_keyboard_test():
    # Define and initialize the update rate to be zero
    update_rate = '0'
    # Implement a for-ever loop in-case the user input a number out of the range (0 - 9)
    while update_rate not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        # Ask the user to choose an integer number ranging from 1 to 9
        update_rate = input("Please choose a number ranging from 1 to 9: ")
    # Assign the third decimal to be equal to the desired integer value
    sev_seg.set_digit(2, update_rate)
    # Assign the last decimal to be equal to zero
    sev_seg.set_digit(3, '0')
    # Show the decimal point in the third order
    sev_seg.set_decimal(2, True)
    sev_seg.write_display()
    # Show the time delay on the 7SD screen
    time.sleep(1)
    # Clear the 7SD screen
    sev_seg.clear()
    # Make sure to re-define the update_rate as integer to be used whenever the funciton is called
    update_rate = int(update_rate)
    return update_rate

# ---------------------------------------------------------------------------------------------------------------------------------------- #
####################################################### Implementation Area - 1 ############################################################
# Here we display the actual ultrasonic measurements on the 7SD screen and the MLD screen by using the pre-defined funcitons

# -------------------------------------------- Uncomment the below code for execution ---------------------------------------------------- #

# # Clear the actual time value on the 7SD screen
# sev_seg.clear()
# sev_seg.write_display()
# print("Cleaning the 7SD screen")
# time.sleep(2)
#
# # Clear the MLD before we display the measured samples on the MLD screen
# with canvas(my_max7219_device) as draw:
#     draw.rectangle([0,0,7,7], fill = "black", outline = "black")
# print("Cleaning the MLD Matrix")
# time.sleep(2)
#
# # Define a list of 8 indices and set the values to -1 (or any other value out of 0-7 range) instead of 0, because we don't want the first sample values to appear in the MLD
# bar_height = [100, 50, 70, 111, 54, 96, 1000, -1]
#
# # Calling the update rate function
# update_rate = update_rate_keyboard_test()
#
# # Run a for-ever loop to obtain infinite number of ultrasonic measured samples
# while True:
#     # Get the time difference from the ultrasonic module function
#     time_difference = ultra_sonic_ranging_time_difference(pin_trigger, pin_echo)
#     # Show the measured distance on the 7SD screen
#     scale_distance_show_7SD(time_difference, update_rate)
#     # Show the measured distance on the MLD screen
#     matrix_led_display(time_difference, update_rate)

# -------------------------------------------- Uncomment the above code for execution ---------------------------------------------------- #

# ---------------------------------------------------------------------------------------------------------------------------------------- #
####################################################### Implementation Area - 2 ############################################################
# Here we implement the remote edition functions

# -------------------------------------------- Uncomment the below code for execution ---------------------------------------------------- #

# # Clear the actual time value on the 7SD screen
# sev_seg.clear()
# sev_seg.write_display()
# print("Cleaning the 7SD screen")
# time.sleep(2)
#
# # Clear the MLD before we display the measured samples on the MLD
# with canvas(my_max7219_device) as draw:
#     draw.rectangle([0,0,7,7], fill = "black", outline = "black")
# print("Cleaning the MLD Matrix")
# time.sleep(2)
#
# # Define a list of 8 indices and set the values to -1 (or any other value out of 0-7 range) instead of 0,
# # because we don't want the first sample values to appear in the MLD
# bar_height = [100, 50, 70, 111, 54, 96, 1000, -1]
#
# # Calling the update rate function
# update_rate = update_rate_keyboard_test()
#
# # Run a for-ever loop to ask the user to input a floating number between 0 and 100 and show a random value on the MLD
# while True:
#     # Show the floating number (0-100) on the 7SD screen
#     scale_distance_show_7SD_keyboard_test()
#     # Show the integer value (0-7) on the MLD screen
#     matrix_led_display_test(update_rate)

# -------------------------------------------- Uncomment the above code for execution ---------------------------------------------------- #

# ---------------------------------------------------------------------------------------------------------------------------------------- #
########################################### Section 2.3 Archive + Seciton 2.4 Calibraiton ##################################################
####################################################### Implementation Area - 3 ############################################################

# -------------------------------------------- Uncomment the below code for execution ---------------------------------------------------- #

# Define a funciton that asks the user to input an update rate (0 - 9)
def update_rate_keyboard_test():
    # Define and initialize the update rate to be zero
    update_rate = '0'
    # Implement a for-ever loop in-case the user input a number out of the range (0 - 9)
    while update_rate not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        # Ask the user to choose an integer number ranging from 1 to 9
        update_rate = input("Please choose a number ranging from 1 to 9: ")
    # Assign the third decimal to be equal to the desired integer value
    sev_seg.set_digit(2, update_rate)
    # Assign the last decimal to be equal to zero
    sev_seg.set_digit(3, '0')
    # Show the decimal point in the third order
    sev_seg.set_decimal(2, True)
    sev_seg.write_display()
    # Show the time delay on the 7SD screen
    time.sleep(1)
    # Clear the 7SD screen
    sev_seg.clear()
    # Make sure to re-define the update_rate as integer to be used whenever the funciton is called
    update_rate = int(update_rate)
    return update_rate

# Define a funciton for generating a random floating value lies between 0 and 100
def generate_random_value_imp_3():
    # Generating a random value
    random_var = random.random()
    random_var = random_var * 100
    random_var = round(random_var, 1)
    return random_var

# Define a funciton for displaying the random floaitng value on the 7SD
def scale_distance_show_7SD_keyboard_imp_3(random_var):
    # In case the number is negative
    if random_var < 0:
        for i in range(4):
            sev_seg.set_digit(i, '0')

    # Displaying the number between 0 and 10
    elif random_var >= 0 and random_var < 10:
        random_var = str(random_var)
        for i in range(2):
            sev_seg.set_digit(i, '0')
        sev_seg.set_digit(2, random_var[0])
        sev_seg.set_digit(3, random_var[2])

    # Displaying the number between 10 and 100
    elif random_var >= 10 and random_var < 100:
        random_var = str(random_var)
        sev_seg.set_digit(0, '0')
        sev_seg.set_digit(1, random_var[0])
        sev_seg.set_digit(2, random_var[1])
        sev_seg.set_digit(3, random_var[3])

    # Displaying the maximum possible number
    elif random_var >= 100:
        random_var = str(random_var)
        sev_seg.set_digit(0, '1')
        sev_seg.set_digit(1, '0')
        sev_seg.set_digit(2, '0')
        sev_seg.set_digit(3, '0')
    sev_seg.set_decimal(2, True)
    sev_seg.write_display()

def matrix_led_display_test_imp_3(random_var, bar_height):
    # Scale the random value to lie between 0 and 7 as integer value
    random_var = round((random_var / 100) * 7, 0)
    random_var = int(random_var)
    # Add the new scaled value "random_scale" to the pre-defined list "bar_height"
    bar_height.append(random_var)
    # Remove the oldest scaled value from the list
    del bar_height[0]
    # Defining a canvas drawing environment
    with canvas(my_max7219_device) as draw:
        for i in range(8):
            draw.line([i, 7 - bar_height[i], i, 7 - bar_height[i]], fill="white")

# Import the sys library to control the system (e.g., pause, abort, exit, etc....)
import sys

# Here the program starts
# Define the system
def my_system():
    # Define and Initialize a summation of the first 10 measurements
    sum_s = 0
    # Define a time counter of 5 seconds but 5.1 seconds were added allowing for some wasted time
    t_end = time.time() + 5.1
    # Define the buzzer as an output GPIO-pin
    buzzer = 18
    RPI.setup(buzzer, RPI.OUT, pull_up_down = RPI.PUD_OFF)
    # Implement a while loop that lasts 5 seconds
    while time.time() < t_end:
        # Turn the buzzer on for 5 seconds
        RPI.output(buzzer, RPI.HIGH)
        for i in range(10):
            # Randomize a value for one of the 10 measurements
            s = random.random()
            s = s * 100
            s = round(s, 1)
            # apply 0.5 second between two successive measurements
            time.sleep(0.5)
            sum_s = sum_s + s
    # Turn off the buzzer
    RPI.output(buzzer, RPI.LOW)
    # Calculate the mean of the first 10 measurements
    s_mean = sum_s/10
    # Calculate alpha
    alpha = 100 / s_mean
    while True:
        # Initializing the 7SD
        sev_seg.begin()
        # Clear the actual time value on the 7SD screen
        sev_seg.clear()
        sev_seg.write_display()
        print("Cleaning the 7SD screen")

        # Clear the MLD before we display the measured samples on the MLD
        with canvas(my_max7219_device) as draw:
            draw.rectangle([0,0,7,7], fill = "black", outline = "black")
        print("Cleaning the MLD Matrix")

        # Inform the user regarding the possiblity to pause the system
        print("Press cntrl + c to pause the system")

        # Define a list of 8 indices and set the values to -1 (or any other value out of 0-7 range) instead of 0,
        # because we don't want the first sample values to appear in the MLD
        bar_height = [100, 50, 70, 111, 54, 96, 1000, -1]

        # Define a list of 100 zeroes to be used later for adding the samples
        count = 0
        fifo_list = []
        while count < 100:
            fifo_list.append(0)
            count = count + 1

        # Define and initialize an index for the fifo data buffer
        fifo_index = 0

        # Calling the update rate function
        update_rate = update_rate_keyboard_test()

        # Define a normal program pathway where the program should normally operates if it is not interferred with an event (e.g, cntrl + c)
        try:
            while True:
                # Get a random floating value
                random_var = generate_random_value_imp_3()
                # calculating the percentage value P[%]
                p_percent = alpha * random_var
                print(f"P[%] = {p_percent}")
                # Show the random floating value on the 7SD screen
                scale_distance_show_7SD_keyboard_imp_3(random_var)
                # Show the random floating value on the MLD screen
                matrix_led_display_test_imp_3(random_var, bar_height)
                # apply fifo concept
                fifo_list.pop()
                fifo_list.insert(0, random_var)
                time.sleep(update_rate)
        except KeyboardInterrupt:
            print("The system now is paused! You have three options:")
            print("1) Press cntrl+c to restart the system")
            print("2) Press A to navigate through the previous samples")
            print("3) Press E to exit from the system")
            while True:
                try:
                    # Ask the user to choose: 1) Exit the program 2) Archive 3) Restart
                    option = input("Please press one of the following: cntrl + c , A , E: ")
                    if option == 'A':
                        if fifo_index == 100:
                            # if it has reached 100 it should be assigned 99 so that it is stuck at the last value and the program will indicate that to the user
                            fifo_index = 99
                            print("This is the end of the archived values")
                        # Initializing the 7SD
                        sev_seg.begin()
                        # Show the archive number on the 7SD screen
                        archive_num = str(fifo_list[fifo_index])
                        sev_seg.print_number_str(archive_num)
                        sev_seg.write_display()
                        # Show the archive number on the MLD screen
                        mld_index = fifo_index
                        fifo_list[mld_index] = int(round((fifo_list[mld_index] / 100) * 7, 0))
                        with canvas(my_max7219_device) as draw:
                            for i in range(8):
                                if mld_index > -1:
                                    draw.line([i, 7 - fifo_list[mld_index], i, 7 - fifo_list[mld_index]], fill="white")
                                    mld_index = mld_index - 1
                                else:
                                    break
                        # Increment the fifo buffer index
                        fifo_index = fifo_index + 1
                    elif option == 'E':
                        # Exit the program
                        sys.exit()
                except KeyboardInterrupt:
                    print("Restarting")
                    my_system()
# Here the program ends
my_system()

# -------------------------------------------- Uncomment the above code for execution ---------------------------------------------------- #





























