import os
import yaml

"""
Load settings from YAML file

Note that there is currently almost NO error checking for the YAML
settings file. Therefore, by design, an exception will be raised
when a required setting is missing or misspelled in the YAML file.
This stops the program with a Traceback which will indicate which
setting below caused the error. Reading the Traceback will indicate
which line below caused the error. Fix the YAML file and rerun the
program until the YAML settings file is read correctly.

There is a "print_settings" option that can be set to TRUE to print
the dictionary that results from reading the YAML file. Note that the
order of the items in the dictionary will not necessarily be the order
of the items in the YAML file (this is a property of Python dictionaries).
"""

class Settings:    
    def __init__(self):
        userdir = os.path.expanduser("~")
        with open(os.path.join(userdir, "imagenode.yaml")) as f:
            self.config = yaml.safe_load(f)
        self.print_node = False
        if 'node' in self.config:
            if 'print_settings' in self.config['node']:
                if self.config['node']['print_settings']:
                    self.print_settings()
                    self.print_node = True
                else:
                    self.print_node = False
        else:
            self.print_settings('"node" is a required settings section but not present.')
            raise KeyboardInterrupt
        if 'hub_address' in self.config:
            self.hub_address = self.config['hub_address']['H1']
            # TODO add read and store H2 and H3 hub addresses
        else:
            self.print_settings('"hub_address" is a required settings section but not present.')
            raise KeyboardInterrupt

        if 'name' in self.config['node']:
            self.nodename = self.config['node']['name']
        else:
            self.print_settings('"name" is a required setting in the "node" section but not present.')
            raise KeyboardInterrupt
        if 'patience' in self.config['node']:
            self.patience = self.config['node']['patience']
        else:
            self.patience = 10  # default is to wait 10 seconds for hub reply
        if 'queuemax' in self.config['node']:
            self.queuemax = self.config['node']['queuemax']
        else:
            self.queuemax = 50
        if 'heartbeat' in self.config['node']:
            self.heartbeat = self.config['node']['heartbeat']
        else:
            self.heartbeat = None
        if 'stall_watcher' in self.config['node']:
            self.stall_watcher = self.config['node']['stall_watcher']
        else:
            self.stall_watcher = False
        if 'REP_watcher' in self.config['node']:
            self.REP_watcher = self.config['node']['REP_watcher']
        else:
            self.REP_watcher = True
        if 'send_threading' in self.config['node']:
            self.send_threading = self.config['node']['send_threading']
        else:
            self.send_threading = False
        if 'send_type' in self.config['node']:
            self.send_type = self.config['node']['send_type']
        else:
            self.send_type = 'jpg'  # default send type is jpg
        if 'cameras' in self.config:
            self.cameras = self.config['cameras']
        else:
            self.cameras = None
        if 'sensors' in self.config:
            self.sensors = self.config['sensors']
        else:
            self.sensors = None
        if 'lights' in self.config:
            self.lights = self.config['lights']
        else:
            self.lights = None

    def print_settings(self, title=None):
        """ prints the settings in the yaml file using pprint()
        """
        if title:
            print(title)
        print('Contents of imagenode.yaml:')
        pprint.pprint(self.config)
        print()