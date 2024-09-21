import configparser
import time
from typing import Any
import meshtastic.stream_interface
import meshtastic.serial_interface
import meshtastic.tcp_interface
import serial.tools.list_ports
import argparse

import threading
from pubsub import pub
    
    
def initialize_config() -> dict[str, Any]:
    """
    Function reads and parses system configuration file

    Returns a dict with the following entries:
    config - parsed config file
    interface_type - type of the active interface
    hostname - host name for TCP interface
    port - serial port name for serial interface
    bbs_nodes - list of peer nodes to sync with

    Args:
        config_file (str, optional): Path to config file. Function reads from './config.ini' if this arg is set to None. Defaults to None.

    Returns:
        dict: dict with system configuration, ad described above
    """
    config = configparser.ConfigParser()

    config_file = "config.ini"
    config.read(config_file)

    interface_type = config['interface']['type']
    hostname = config['interface'].get('hostname', None)
    port = config['interface'].get('port', None)


    return {
        'config': config,
        'interface_type': interface_type,
        'hostname': hostname,
        'port': port,
        'mqtt_topic': 'meshtastic.receive'
    }



def get_interface(system_config:dict[str, Any]) -> meshtastic.stream_interface.StreamInterface:
    """
    Function opens and returns an instance meshtastic interface of type specified by the configuration
    
    Function creates and returns an instance of a class inheriting from meshtastic.stream_interface.StreamInterface.
    The type of the class depends on the type of the interface specified by the system configuration.
    For 'serial' interfaces, function returns an instance of meshtastic.serial_interface.SerialInterface,
    and for 'tcp' interface, an instance of meshtastic.tcp_interface.TCPInterface.

    Args:
        system_config (dict[str, Any]): A dict with system configuration. See description of initialize_config() for details.

    Raises:
        ValueError: Exception raised in the following cases:
                - Type of interface not provided in the system config
                - Multiple serial ports present in the system, and no port specified in the configuration
                - Serial port interface requested, but no ports found in the system
                - Hostname not provided for TCP interface

    Returns:
        meshtastic.stream_interface.StreamInterface: An instance of StreamInterface
    """
    while True:
        try:
            if system_config['interface_type'] == 'serial':
                if system_config['port']:
                    return meshtastic.serial_interface.SerialInterface(system_config['port'])
                else:
                    ports = list(serial.tools.list_ports.comports())
                    if len(ports) == 1:
                        return meshtastic.serial_interface.SerialInterface(ports[0].device)
                    elif len(ports) > 1:
                        port_list = ', '.join([p.device for p in ports])
                        raise ValueError(f"Multiple serial ports detected: {port_list}. Specify one with the 'port' argument.")
                    else:
                        raise ValueError("No serial ports detected.")
            elif system_config['interface_type'] == 'tcp':
                if not system_config['hostname']:
                    raise ValueError("Hostname must be specified for TCP interface")
                return meshtastic.tcp_interface.TCPInterface(hostname=system_config['hostname'])
            elif system_config['interface_type'] == 'debug':
                return DebugInterface()
            else:
                raise ValueError("Invalid interface type specified in config file")
        except PermissionError as e:
            print(f"PermissionError: {e}. Retrying in 5 seconds...")
            time.sleep(5)

class DebugInterface:
    def __init__(self, *argv, **kwargs):
        print(argv)
        print(kwargs)
        
        self._rxThread = threading.Thread(target=self.__reader, args=(), daemon=True)
        self._rxThread.start()

        self.fake_packet = {
            'decoded': {
                'portnum': 'TEXT_MESSAGE_APP',
                'payload': b''
            },
            'from': 'test_from',
            'to': '123',
            'fromId': 'test_from_id'
        }

        self.nodes = {
            'test_from_id': {
                'user': {
                    'shortName': 'from'
                },
                'num': '456'
            },
            'test_to_id': {
                'user': {
                    'shortName': 'to'
                },
                'num': '123'
            }
        }

        class myTempInfo:
            def __init__(self):
                self.my_node_num = '123'

        self.myInfo = myTempInfo()

    def __contains__(self, item):
        return item in self.fake_packet
    
    def __getitem__(self, key):
        return self.fake_packet[key]
    
    def __reader(self):
        while True:
            data = input("Enter Text: ")
            self.fake_packet['decoded']['payload'] = bytes(data, 'utf-8')
            pub.sendMessage("meshtastic.receive", packet=self.fake_packet, interface=self)

    def sendText(self, text, destinationId, wantAck, wantResponse):
        print()
        print(text)
        print()

        class fakeReturn:
            def __init__(self):
                self.id = '456'

        return fakeReturn()