import paho.mqtt.client as mqtt
from MessageHandler import MessageHandler

class MQTT:
    def __init__(self, config, sensors):
        self.config = config
        self.sensors = sensors
        self.ip = config.getMqttIp()
        self.port = config.getMqttPort()
        self.client = None

        self.__createClient()
        self.__connect()

    def __createClient(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.__on_message

    def __on_connect(self, client, userdata, flags, rc):
        print('Connected with result code ' + str(rc))
        client.subscribe(self.config.getMqttTopic())

    def __on_message(self, client, userdata, message):
        MessageHandler(message.payload, self.config, self.sensors).handle()

    def __connect(self):
        self.client.connect(
            self.ip,
            self.port
        )

    def runLoop(self):
        self.client.loop_forever()
