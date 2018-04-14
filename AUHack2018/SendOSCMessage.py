import time
from pythonosc import osc_message_builder
from pythonosc import udp_client


class NoteSender:
    def __init__(self, track, bass):
        self.notes = []
        self.arrayOfInstruments = []
        self.pitchArray = []
        self.arrayToSend = []
        self.ampArray = []
        self.track = track
        self.useBase = bass
        self.sender = udp_client.SimpleUDPClient('127.0.0.1', 4559)

    def notes(self, noteArray):
        self.notes.append(noteArray)

    def pitch(self, pitchArray):
        self.pitchArray = pitchArray

    def amp(self, ampArray):
        self.ampArray = ampArray

    def sendToSonicPi(self):
        self.arrayToSend.append(self.track)
        for note in self.notes:
            self.arrayToSend.append(note)
        for amp in self.ampArray:
            self.arrayToSend.append(amp)
        for pitch in self.pitchArray:
            self.arrayToSend.append(pitch)
        print(self.arrayToSend)
        self.sender.send_message('/trigger/prophet', self.arrayToSend)
