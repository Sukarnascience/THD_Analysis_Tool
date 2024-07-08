import socket
import threading
import random
import time

# Custom configuration module
#import config

def broadcast_random_data(host, port):
    # Create UDP socket for broadcasting data
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        # Generate random sensor values
        voltage = random.uniform(210, 230)
        frequency = random.uniform(49.5, 50.5)
        charge = random.uniform(0, 100)
        pressure = random.uniform(0, 10)
        moisture = random.uniform(0, 100)
        temperature = random.uniform(20, 30)
        air_quality = random.uniform(0, 50)
        partial_discharge = random.uniform(0, 1)
        oil_level = random.uniform(50, 100)

        # Create a comma-separated string of values
        data = f"{voltage},{frequency},{charge},{pressure},{moisture},{temperature},{air_quality},{partial_discharge},{oil_level}"
        
        # Broadcast the data
        broadcast_socket.sendto(data.encode('utf-8'), (host, port))
        
        # Wait for a second before broadcasting again
        time.sleep(1)

if __name__ == "__main__":
    broadcast_host = "localhost"  # Set the broadcast host
    broadcast_port = 12345  # Set the broadcast port

    # Start a separate thread to continuously broadcast random data
    broadcast_thread = threading.Thread(target=broadcast_random_data, args=(broadcast_host, broadcast_port))
    broadcast_thread.daemon = True
    broadcast_thread.start()

    # Keep the main thread alive
    while True:
        time.sleep(1)
