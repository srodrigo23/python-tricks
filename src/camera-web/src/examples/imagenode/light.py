class Light:
    """ Methods and attributes of a light controlled by an RPi GPIO pin

    Each light is setup and started using the settings in the yaml file.
    Includes methods for turning the light on and off using the GPIO pins.

    Parameters:
        light (text): dictionary key of the current light being instantiated
        lights (dict): dictionary of all the lights in the YAML file
        settings (Settings object): settings object created from YAML file
    """

    def __init__(self, light, lights, settings):
        """ Initializes a specific light using settings in the YAML file.
        """

        if 'name' in lights[light]:
            self.name = lights[light]['name']
        else:
            self.name = light
        if 'gpio' in lights[light]:
            self.gpio = lights[light]['gpio']
        else:
            self.gpio = 18   # GPIO pin 18 is the default for testing
        if 'on' in lights[light]:
            self.on = lights[light]['on']
        else:
            self.on = 'continuous'

        GPIO.setup(self.gpio, GPIO.OUT)
        if self.on == 'continuous':
            self.turn_on()
        else:  # set up light on/off cyclying other than continuous
            pass  # for example, during certain hours

    def turn_on(self):
        """ Turns on the light using the GPIO pins
        """
        GPIO.output(self.gpio, True)  # turn on light

    def turn_off(self):
        """ Turns off the light using the GPIO pins
        """
        GPIO.output(self.gpio, False)  # turn off light
