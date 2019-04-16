class PlatformOutputStream(IO_Stream):
    def __init__(self):
        description = "Platform Output Stream"
        IO_Stream.__init__(description)

    # function to listen to output data from the services
    # route the data to the destinations according to configuration
    def handle_output_stream(self):

if __name__ == "__main__":
    platform_output_stream = PlatformOutputStream()
    platform_output_stream.handle_output_stream()
