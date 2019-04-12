class SensorManager:
    def __init__(self):
        pass

    # make a thread
    # listen for new sensors to connect
    # create a new thread for each sensor that connects
    # sensor data will be received separately for each thread
    # for two-way sensors a separate thread for output_stream is created
    def handle_sensors(self):
    
    # separate thread for each sensor type
    # sensor data will be received in this thread
    def input_stream(self, sensor_type):

    # separate thread for listening to incoming services
    # register and unregister a service for receiving data from a particular sensor type
    def listen_services(self):

    # route the output data to the appropriate sensor
    def output_stream(self):

if __name__ == "__main__":
    sensor_manager = SensorManager()
    sensor_manager.handle_sensors()
    sensor_manager.listen_services()
