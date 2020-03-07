import dweepy # Import the dweepy module
import time # Import the time module
import grovepi # Import the grovepi module
from grovepi import * # Import everything from the grovepi module
from threading import Thread # Import the Thread class from the threading module

from config import thingOneName # Import thingOneName from the configuration file
from config import thingTwoName # Import thingTwoName from the configuration file

dht_sensor = 7 # Connect the DHT sensor to digital port D7
dht_sensor_type = 0 # Use 0 for the blue-colored sensor

sound_sensor = 2 # Connect the Grove Sound Sensor to analog port A2
grovepi.pinMode(sound_sensor,"INPUT") # Set pin mode for port A2 as an input

potentiometer_sensor = 1 # Connect the Grove Rotary Angle Sensor to analog port A1
grovepi.pinMode(potentiometer_sensor,"INPUT") # Set pin mode for port A1 as an input

led = 6 # Connect the LED to digital port D6
grovepi.pinMode(led,"OUTPUT") # Set pin mode for port D6 as an output

publisher_state = False # Set the publisher state to false. This is used in the while loop in the publish() method
button_clicked = 0

def read_temperature():
    [ temp_sensor_value,hum_sensor_value ] = dht(dht_sensor,dht_sensor_type) # Read the temperature and humidity sensor values
    temperature = str(temp_sensor_value) # Convert temperature sensor value to a String and store in a variable called temperature
    return temperature # Return the value from the dht sensor

def read_sound():
    sound_sensor_value = grovepi.analogRead(sound_sensor) # Read the sound sensor value and store it in a variable called sound_sensor_value
    return sound_sensor_value # Return the value from the sound sensor

def read_potentiometer():
    potentiometer_sensor_value = grovepi.analogRead(potentiometer_sensor) # Read the potentiometer sensor value and store it in a variable c$
    return potentiometer_sensor_value # Return the value from the potentiometer

# Method to listen for dweets from a specific thing called TestThingTwo
def listen(publisher_thread): # The listen() method takes the publisher thread as a parameter
    print(listener_thread_name + " is Listening!") # Print Starting Listening!
    global publisher_state # Set publisher state as a global variable
    publisher_state = True # Set publisher state to true
    global button_clicked
    print(str(button_clicked))
    if not publisher_thread.is_alive(): # If publisher thread is not running execute the following code
        publisher_thread.start() # Start publisher thread
    for dweet in dweepy.listen_for_dweets_from(thingTwoName): # For loop listens for dweets from a specific thing called TestThingTwo
        content = dweet["content"] # Store the content from each dweet into a variable called content
        print(str(content))
        try:
            button_clicked = content["ButtonClicked"]
            print("Button Clicked: " + str(button_clicked))
        except:
            print("An exception occurred")
        thing = dweet["thing"] # Store the thing from each dweet into a variable called thing
        print("Reading from TestThingTwo: " + str(content))
        print(thing) # Print the variable called thing
        print("")
        try:
            if str(button_clicked) == 1:
                brightness = 255
            else:
                brightness = 0
                grovepi.analogWrite(led,brightness) # Give PWM output to LED
        except:
            print("An exception occurred")
    print("Listening Ending!") # Print Listening Ending!

# Method to publish dweets from a specific thing called TestThingOne
def publish(): # The publish() method takes no parameters
    print(publisher_thread_name + " is Publishing!") # Print Starting Publishing!
    while publisher_state: # While publisher state is true execute the following code
        temperature = read_temperature()
        sound = read_sound()
        potentiometer = read_potentiometer()
        result = dweepy.dweet_for(thingOneName, {"Temperature": temperature, "Sound": sound, "Potentiometer": potentiometer}) # Send a dweet$
        print("TestThingOne published: " + str(result)) # Print the variable called result
        time.sleep(1) # Call the sleep() method from the time module and pass in 1 second as a parameter
        print("")
    print("Publishing Ending!") # Print Publishing Ending!

publisher_thread = Thread(target=publish) # Create a new publisher thread passing in the publish() method as a parameter
listener_thread = Thread(target=listen, args=(publisher_thread,)) # Create a new listener thread passing in the listen() method and publishe$

publisher_thread_name = publisher_thread.getName() # Get publisher thread name
listener_thread_name = listener_thread.getName() # Get listener thread name

listener_thread.start() # Start listener thread
