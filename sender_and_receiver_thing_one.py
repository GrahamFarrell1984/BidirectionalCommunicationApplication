import dweepy # Import the dweepy module
import time # Import the time module
import grovepi # Import the grovepi module
from grovepi import * # Import everything from the grovepi module
from threading import Thread # Import the Thread class from the threading module

from config import thingOneName # Import thingOneName from the configuration file
from config import thingTwoName # Import thingTwoName from the configuration file

dht_sensor = 7 # Connect the DHT sensor to digital port D7
dht_sensor_type = 0 # Use 0 for the blue-colored sensor

publisher_state = False # Set the publisher state to false. This is used in the while loop in the publish() method

def read_temperature():
    [ temp_sensor_value,hum_sensor_value ] = dht(dht_sensor,dht_sensor_type) # Read the temperature and humidity sensor values
    temperature = str(temp_sensor_value) # Convert temperature sensor value to a String and store in a variable called temperature
    return temperature

def read_humidity():
    [ temp_sensor_value,hum_sensor_value ] = dht(dht_sensor,dht_sensor_type) # Read the temperature and humidity sensor values
    humidity = str(hum_sensor_value) # Convert humidity sensor value to a String and store in a variable called humidity
    return humidity

# Method to listen for dweets from a specific thing called TestThingTwo
def listen(publisher_thread): # The listen() method takes the publisher thread as a parameter
    print(listener_thread_name + " is Listening!") # Print Starting Listening!
    global publisher_state # Set publisher state as a global variable
    publisher_state = True # Set publisher state to true
    if not publisher_thread.is_alive(): # If publisher thread is not running execute the following code
        publisher_thread.start() # Start publisher thread
    for dweet in dweepy.listen_for_dweets_from(thingTwoName): # For loop listens for dweets from a specific thing called TestThingTwo
        content = dweet["content"] # Store the content from each dweet into a variable called content
        thing = dweet["thing"] # Store the thing from each dweet into a variable called thing
        # print("Reading from " + listener_thread_name + ": " + str(content)) # Print the variable called content
        print("Reading from TestThingTwo: " + str(content))
        print(thing) # Print the variable called thing
        print("")
    print("Listening Ending!") # Print Listening Ending!

# Method to publish dweets from a specific thing called TestThingOne
def publish(): # The publish() method takes no parameters
    num = 0 # Set a variable called num to 0
    print(publisher_thread_name + " is Publishing!") # Print Starting Publishing!
    while publisher_state: # While publisher state is true execute the following code
        temperature = read_temperature()
        humidity = read_humidity()
        result = dweepy.dweet_for(thingOneName, {"Temperature": temperature, "Humidity": humidity}) # Send a dweet from a specific thing called TestThingOne with a key of TestNum and value of the variable called num and store it in a variable called result
        print("TestThingOne published: " + str(result)) # Print the variable called result
        time.sleep(1) # Call the sleep() method from the time module and pass in 1 second as a parameter
        num = num + 1 # Increment the variable called num by 1
        print("")
    print("Publishing Ending!") # Print Publishing Ending!

publisher_thread = Thread(target=publish) # Create a new publisher thread passing in the publish() method as a parameter
listener_thread = Thread(target=listen, args=(publisher_thread,)) # Create a new listener thread passing in the listen() method and publisher thread as parameters

publisher_thread_name = publisher_thread.getName() # Get publisher thread name
listener_thread_name = listener_thread.getName() # Get listener thread name

listener_thread.start() # Start listener thread
