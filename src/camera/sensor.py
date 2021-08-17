class Sensor:
    """ Methods and attributes of a sensor, such as a temperature sensor

    Each sensor is setup and started using the settings in the yaml file.
    Includes methods for reading, and closing the sensor and GPIO pins.

    Parameters:
        sensor (text): dictionary key of current sensor being instantiated
        sensors (dict): dictionary of all the sensors in the YAML file
        settings (Settings object): settings object created from YAML file

    """

    def __init__(self, sensor, sensors, settings, tiny_image, send_q):
        """ Initializes a specific sensor using settings in the YAML file.
        """

        self.tiny_image = tiny_image
        self.send_q = send_q
        if 'name' in sensors[sensor]:
            self.name = sensors[sensor]['name']
        else:
            self.name = sensor
        if 'gpio' in sensors[sensor]:
            self.gpio = sensors[sensor]['gpio']
        else:
            self.gpio = 4   # GPIO pin 4 is default for testing
        if 'type' in sensors[sensor]:
            self.type = sensors[sensor]['type']
        else:
            self.type = 'Unknown'
        if 'unit' in sensors[sensor]:
            self.unit = sensors[sensor]['unit'].upper()
        else:
            self.unit = 'F'
        if 'read_interval_minutes' in sensors[sensor]:
            self.interval = sensors[sensor]['read_interval_minutes']
        else:
            self.interval = 10  # how often to read sensor in minutes
        if 'min_difference' in sensors[sensor]:
            self.min_difference = sensors[sensor]['min_difference']
        else:
            self.min_difference = 1  # minimum difference to count as reportable
        self.interval *= 60.0  # convert often to check sensor to seconds

        # self.event_text is the text message for this sensor that is
        #   sent when the sensor value changes
        # example: Barn|Temperaure|85 F
        # example: Barn|Humidity|42 %
        # example: Garage|Temperature|71 F
        # example: Compost|Moisture|95 %
        # self.event_text will have self.current_reading appended when events are sent
        # self.event_text = '|'.join([settings.nodename, self.name]).strip()
        self.event_text = settings.nodename
        # Initialize last_reading and temp_sensor variables
        self.last_reading_temp = -999  # will ensure first temp reading is a change
        self.last_reading_humidity = -999  # will ensure first humidity reading is a change
        self.temp_sensor = None

        # Sensor types
        if self.type == 'DS18B20':
            # note that DS18B20 requires GPIO pin 4 (unless kernel is modified)
            global W1ThermSensor  # for DS18B20 temperature sensor
            from w1thermsensor import W1ThermSensor
            self.temp_sensor = W1ThermSensor()

        if (self.type == 'DHT11') or (self.type == 'DHT22'):
            global adafruit_dht  # for DHT11 & DHT22 temperature sensor
            import adafruit_dht
            if self.type == 'DHT11':
                self.temp_sensor = adafruit_dht.DHT11(self.gpio)
            if self.type == 'DHT22':
                self.temp_sensor = adafruit_dht.DHT22(self.gpio)

        if self.temp_sensor is not None:
            self.check_temperature()  # check one time, then start interval_timer
            threading.Thread(daemon=True,
                             target=lambda: interval_timer(self.interval, self.check_temperature)).start()

    def check_temperature(self):
        """ adds temperature & humidity (if available) value from a sensor to senq_q message queue
        """
        if self.type == 'DS18B20':
            if self.unit == 'C':
                temperature = int(self.temp_sensor.get_temperature(W1ThermSensor.DEGREES_C))
            else:
                temperature = int(self.temp_sensor.get_temperature(W1ThermSensor.DEGREES_F))
            humidity = -999
        if (self.type == 'DHT11') or (self.type == 'DHT22'):
            for i in range(5):  # try for valid readings 5 times; break if valid
                try:
                    if self.unit == 'C':
                        temperature = self.temp_sensor.temperature
                    else:
                        temperature = self.temp_sensor.temperature * (9 / 5) + 32
                    temperature = float(format(temperature, '.1f'))
                    humidity = self.temp_sensor.humidity
                    humidity = float(format(humidity, '.1f'))
                    break  # break out of for loop if got valid readings
                except RuntimeError:
                    sleep(3)  # wait 3 seconds and try again
                    pass  # this will retry up to 5 times before exiting the for loop

        if abs(temperature - self.last_reading_temp) >= self.min_difference:
            # temperature has changed from last reported temperature, therefore
            # send an event message reporting temperature by appending to send_q
            temp_text = str(temperature) + " " + self.unit
            text = '|'.join([self.event_text, 'Temp', temp_text])
            text_and_image = (text, self.tiny_image)
            self.send_q.append(text_and_image)
            self.last_reading_temp = temperature
        if abs(humidity - self.last_reading_humidity) >= self.min_difference:
            # humidity has changed from last reported humidity, therefore
            # send an event message reporting humidity by appending to send_q
            humidity_text = str(humidity) + " %"
            # Spelling of humidity all lower case is intentional to avoid
            # first letter test of "Heartbeat" in imagehub
            text = '|'.join([self.event_text, 'humidity', humidity_text])
            text_and_image = (text, self.tiny_image)
            self.send_q.append(text_and_image)
            self.last_reading_humidity = humidity
