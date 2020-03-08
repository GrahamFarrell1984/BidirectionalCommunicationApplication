import dweepy # Import the dweepy module
import time # Import the time module
import grovepi # Import the grovepi module
from grovepi import * # Import everything from the grovepi module
from threading import Thread # Import the Thread class from the threading module

from config import thingOneName # Import thingOneName from the configuration file
from config import thingTwoName # Import thingTwoName from the configuration file

dht_sensor = 8 # Connect the DHT sensor to digital port D8
dht_sensor_type = 0 # Use 0 for the blue-colored sensor

light_sensor = 0 # Connect the Grove Light Sensor to analog port A0
grovepi.pinMode(light_sensor,"INPUT") # Set pin mode for port A0 as an input

led = 5 # Connect the LED to digital port D5
grovepi.pinMode(led,"OUTPUT") # Set pin mode for port D5 as an output

adc_ref = 5 # Reference voltage of ADC is 5v

grove_vcc = 5 # Vcc of the grove interface is normally 5v

full_angle = 300 # Full value of the rotary angle is 300 degrees, as per it's specs (0 to 300)

publisher_state = False # Set the publisher state to false. This is used in the while loop in the publish() method

# Functions / Methods
# Method to read from humidity sensor
def read_humidity():
    [ temp_sensor_value,hum_sensor_value ] = dht(dht_sensor,dht_sensor_type) # Read the temperature and humidity sensor values
    humidity = str(hum_sensor_value) # Convert humidity sensor value to a String and store in a variable called humidity
    return humidity # Return the humidity value from the dht sensor

# Method to read from light sensor
def read_light():
    light_sensor_value = grovepi.analogRead(light_sensor) # Read the light sensor value and store it in a variable called light_sensor_value
    return light_sensor_value # Return the value from the light sensor

# Method to listen for dweets from a specific thing called GrahamThingOne
def listen(publisher_thread): # The listen() method takes the publisher thread as a parameter
    print(listener_thread_name + " is Listening!") # Print Starting Listening!
    global publisher_state # Set publisher state as a global variable
    publisher_state = True # Set publisher state to true
    if not publisher_thread.is_alive(): # If publisher thread is not running execute the following code
        publisher_thread.start() # Start publisher thread
    for dweet in dweepy.listen_for_dweets_from(thingOneName): # For loop listens for dweets from a specific thing called GrahamThingOne
        content = dweet["content"] # Store the content from each dweet into a variable called content
        sensor_value = content["Potentiometer"] # Get the value from the potentiometer
        print("Potentiometer Reading: " + str(sensor_value)) # Print the value from the potentiometer
        thing = dweet["thing"] # Store the thing from each dweet into a variable called thing
        print("Reading from " + str(thing) + ": " + str(content))
        print("") # Adds an empty line in the terminal below our output above
        voltage = round((float)(sensor_value) * adc_ref / 1023, 2) # Calculate voltage
        degrees = round((voltage * full_angle) / grove_vcc, 2) # Calculate rotation in degrees (0 to 300)
        brightness = int(degrees / full_angle * 255) # Calculate LED brightess (0 to 255) from degrees (0 to 300)
        grovepi.analogWrite(led,brightness) # Give PWM output to LED

    print("Listening Ending!") # Print Listening Ending!

# Method to publish dweets from a specific thing called GrahamThingTwo
def publish(): # The publish() method takes no parameters
    print(publisher_thread_name + " is Publishing!") # Print Starting Publishing!
    while publisher_state: # While publisher state is true execute the following code
        humidity = read_humidity() # Call the read_humidity() function / method and store result in a variable called humidity
        light = read_light() # Call the read_light() function / method and store result in a variable called light_sensor
        result = dweepy.dweet_for(thingTwoName, {"Humidity": humidity, "Light": light}) # Send a dweet from a specific thing called GrahamThingTwo
        print("GrahamThingTwo published: " + str(result)) # Print the variable called result
        time.sleep(1) # Call the sleep() method from the time module and pass in 1 second as a parameter
        print("") # Adds an empty line in the terminal below our output above
    print("Publishing Ending!") # Print Publishing Ending!

publisher_thread = Thread(target=publish) # Create a new publisher thread passing in the publish() method as a parameter
listener_thread = Thread(target=listen, args=(publisher_thread,)) # Create a new listener thread passing in the listen() method and publisher_thread

publisher_thread_name = publisher_thread.getName() # Get publisher thread name
listener_thread_name = listener_thread.getName() # Get listener thread name

listener_thread.start() # Start listener thread
