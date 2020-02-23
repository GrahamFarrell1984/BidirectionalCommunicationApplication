import dweepy # Import the dweepy module
import time # Import the time module

from threading import Thread # Import the Thread class from the threading module

publisher_state = True # Set the publisher state to true. This is used in the while loop in the publish() method

# Method to listen for dweets from a specific thing called TestThing
def listen(): # Listen method takes no parameters
    for dweet in dweepy.listen_for_dweets_from('TestThing'): # For loop listens for dweets from a specific thing called TestThing
        content = dweet["content"] # Store the content from each dweet into a variable called content
        thing = dweet["thing"] # Store the thing from each dweet into a variable called thing
        print(content) # Print the variable called content
        print(thing) # Print the variable called thing
    print("Listening Ending!") # Print Listening Ending!

# Method to publish dweets from a specific thing called TestThing
def publish(): # Publish method takes no parameters
    num = 0 # Set a variable called num to 0
    while publisher_state: # While publisher state is true execute the following code. This will always be true for the moment
        result = dweepy.dweet_for('TestThing', {"TestNum": num}) # Send a dweet from a specific thing called TestThing with a key of TestNum and value of the variable called num and store it in a variable called result
        print(result) # Print the variable called result
        time.sleep(1) # Call the sleep method from the time module and pass in 1 second as a parameter
        num = num + 1 # Increment the variable called num by 1
    print("Publishing Ending!") # Print Publishing Ending!

listener_thread = Thread(target=listen) # Create a new listener thread passing in the listen method as a parameter
publisher_thread = Thread(target=publish) # Create a new publisher thread passing in the publish method as a parameter
listener_thread_name = listener_thread.getName() # Get listener thread name
publisher_thread_name = publisher_thread.getName() # Get publisher thread name
print(listener_thread_name) # Print listener thread name
print(publisher_thread_name) # Print publisher thread name
listener_thread.start() # Start listener thread
print("Starting Listening!") # Print Starting Listening!
publisher_thread.start() # Start publisher thread
print("Starting Publishing!") # Print Starting Publishing!
