import time
from pythonosc import osc_message_builder
from pythonosc import udp_client



class NoteSender:

	def __init__(self, track, bass):
		self.notes = []
		self.arrayOfInstruments = []
		self.pitchArray = []
		self.arrayToSend = []
		self.durArray = [1]*8
		self.track = track
		self.useBase = bass
		self.sender = udp_client.SimpleUDPClient('127.0.0.1', 4559)

	def notes(self, noteArray):
		self.notes.append(noteArray)

	def pitch(self, pitchArray):
		self.pitchArray = pitchArray

	def duration(self, durArray):
		self.durArray = durArray

	def sendToSonicPi(self):
		self.arrayToSend.append(self.track)
		for note in self.notes:
			self.arrayToSend.append(note)

		self.arrayToSend.append("dur")

		for dur in self.durArray:
			self.arrayToSend.append(dur)
		print(self.arrayToSend)
		self.sender.send_message('/trigger/prophet', self.arrayToSend)


	def handlesucceedingnotes(self):
		#print(self.notes)
		#print(self.durArray)
		for i in range(0, len(self.notes)):
			j = i + 1
			if j < len(self.notes)-1:
				while self.notes[i] == self.notes[j]:
					self.notes[j] = "S"
					j += 1
					if(j == len(self.notes)):
						break
			self.durArray[i] = j - i

		for i in range(0, len(self.notes)):
			if self.notes[i] == "S":
				#print("note i: ", self.notes[i])
				self.durArray[i] = 1
		print(self.notes)
		print(self.durArray)
