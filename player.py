import sys, os, time
import subprocess
import serial
import random
import signal as syssig
from HDmx import DmxPy


# NOTES
NOTES = ["Do", "Fa", "Sol", "Do_aigu"]

# CONFIG
CONFIG = []

CONFIG.append([ [2, 259, "Do"], [3, 258, "Fa"], [4, 257, "Sol"], [5, 256, "Do_aigu"]  ])
CONFIG.append([ [6, 263, "Do"], [7, 262, "Fa"], [8, 261, "Sol"], [9, 260, "Do_aigu"]  ])
CONFIG.append([ [10, 267, "Do"], [11, 266, "Fa"], [12, 265, "Sol"], [13, 264, "Do_aigu"]  ])
CONFIG.append([ [14, 271, "Do"], [15, 270, "Fa"], [16, 269, "Sol"], [17, 268, "Do_aigu"]  ])
CONFIG.append([ [18, 275, "Do"], [19, 274, "Fa"], [20, 273, "Sol"], [21, 272, "Do_aigu"]  ])
CONFIG.append([ [22, 279, "Do"], [23, 278, "Fa"], [24, 277, "Sol"], [25, 276, "Do_aigu"]  ])

CONFIG.append([ [26, 291, "Do"], [27, 290, "Fa"], [28, 289, "Sol"], [29, 288, "Do_aigu"]  ])
CONFIG.append([ [30, 295, "Do"], [31, 294, "Fa"], [32, 293, "Sol"], [33, 292, "Do_aigu"]  ])
CONFIG.append([ [34, 299, "Do"], [35, 298, "Fa"], [36, 297, "Sol"], [37, 296, "Do_aigu"]  ])
CONFIG.append([ [38, 303, "Do"], [39, 302, "Fa"], [40, 301, "Sol"], [41, 300, "Do_aigu"]  ])
CONFIG.append([ [42, 307, "Do"], [43, 306, "Fa"], [44, 305, "Sol"], [45, 304, "Do_aigu"]  ])
CONFIG.append([ [46, 311, "Do"], [47, 310, "Fa"], [48, 309, "Sol"], [49, 308, "Do_aigu"]  ])


SEGMENT_PRE = 1		# Number of Segment to introduce (minimum 1)
SEGMENT_KEEP = 0	# Number of Segment to keep playing while note active anymore
SEGMENTS_STATE = []

#SWITCH Combinaison
PIANO_MODE = [5,9,13]

LED_OFF = 0
LED_READY = 5
LED_ACTIVE = 200
LED_ERROR = 0

DMX_ENABLE = True

# SONS
SOUND_PATH = os.path.join(os.getcwd(), "sons")

# CTRL-C Handler
RUN = True
def quit(signal=None, frame=None):
	global RUN
	RUN = False
	if DMX_ENABLE:
		#dmx_interface.setall(0)
		#dmx_interface.render()
		pass
	print '.:: MUSICALL Ciao !::.'
	sys.exit(0)

# SEGMENT
class Segment:
	def __init__(self, config):
		self.dmx = config[1]
		self.note = config[2]
		self.pin = config[0]

		self.player = None

	# Music STOP
	def stop(self):
		if self.player:
			self.player.terminate()
			self.player = None

	# Music PLAY
	def play(self, note=None):
		if self.player:
			self.stop()
		if not note:
			note = self.note
		audiofile = os.path.join(SOUND_PATH, note+".wav")
		self.player = subprocess.Popen(["aplay", audiofile], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

	# State OFF
	def off(self):
		if DMX_ENABLE:
			dmx_interface.set(self.dmx, LED_OFF)
			dmx_interface.render()
		self.stop()

	# State READY
	def ready(self, percent=1.0):
		if DMX_ENABLE:
			dmx_interface.set(self.dmx, int(LED_READY*percent) )
			dmx_interface.render()

	# State ACTIVE
	def active(self):
		if DMX_ENABLE:
			dmx_interface.set(self.dmx, LED_ACTIVE)
			dmx_interface.render()
		self.play()

	# State ERROR
	def error(self):
		if DMX_ENABLE:
			dmx_interface.set(self.dmx, LED_ERROR)
			dmx_interface.render()
		self.play("error")


# BARREAU
class Barreau:
	def __init__(self, config):
		self.segments = []
		self.target = -1
		self.state = 0
		for seg_conf in config:
			self.segments.append( Segment(seg_conf) )
			SEGMENTS_STATE[seg_conf[0]] = 0;

	# Stop all segments, and remove target
	def stop(self):
		self.target = -1
		self.init()
		for seg in self.segments:
			seg.off()

	# Init target segment
	def init(self, target=-1):
		if target == -1:
			target = random.randint(0, len(self.segments)-1)
		self.target = target

	# State READY
	def ready(self, percent=1.0):
		self.segments[self.target].ready(percent)

	# Event TOUCH
	def touch(self, pin):
		# Good segment touched
		if self.segments[self.target].pin == pin:
			self.segments[self.target].active()
			print 'Touched the good SEG'
			return True

		# Wrong segment touched
		for seg in self.segments:
			if seg.pin == pin:
				self.segments[self.target].error()
				print 'Touched the wrong SEG'
				return True

		# print 'Touched outside the BAR'
		return False

	# Event RELEASE
	def release(self, pin):
		# Inner segment released
		for seg in self.segments:
			if seg.pin == pin:
				print 'Released BAR'
				return True

		return False


# BARRIERE
class Barriere:
	def __init__(self, config):
		self.barreaux = []
		self.readybar = -1
		for bar_conf in config:
			self.barreaux.append( Barreau(bar_conf) )
		self.size = len(self.barreaux)

	# Stop all
	def stop(self):
		self.readybar = -1
		for bar in self.barreaux:
			bar.stop()

	# Init every BAR and start sequence
	def start(self):
		self.stop()
		self.next()

	def next(self):
		# STOP N-SEGMENT_KEEP BAR
		indexStop = (self.readybar+self.size-1-SEGMENT_KEEP) % self.size
		self.barreaux[indexStop].stop()

		# INCREASE ready index
		self.readybar = (self.readybar + 1) % self.size

		# READY next BAR
		percent = 1.0
		for indexReady in range(self.readybar, self.readybar+SEGMENT_PRE):
			self.barreaux[ (indexReady % self.size) ].ready(percent)
			percent -= 1.0/(SEGMENT_PRE+1)

	def touch(self, pin):
		SEGMENTS_STATE[pin] = 1;
		doNext = self.barreaux[self.readybar].touch(pin)
		if doNext:
			self.next()

		# Switch to other mode
		if self.checkSwitch():
			print 'SWITCH TO PIANO MODE'


	def release(self, pin):
		SEGMENTS_STATE[pin] = 0;


	def checkSwitch(self):
		for p in PIANO_MODE:
			if not SEGMENTS_STATE[p]: return False
		return TRUE




if __name__ == '__main__':

	# Handle CTRL-C
	syssig.signal(syssig.SIGINT, quit)

	# DMX INTERFACE
	try:
		dmx_interface = DmxPy.DmxPy('/dev/ttyUSB0')
	except:
		DMX_ENABLE = False
		print "DMX disabled"

	if DMX_ENABLE:
		dmx_interface.setall(0)
		dmx_interface.render()


	# ARDUINO INTERFACE
	try:
		arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=0.01)
	except:
		print "No Arduino found at "+"/dev/ttyACM0"
		quit()

	# CREATE BARRIERE
	barriere = Barriere(CONFIG)

	# TEST Sequence
	print ".:: MUSICALL Started ::."
	INIT_STATE = True
	CALIBRATING = True

	# TEST DMX
	if DMX_ENABLE:
		sys.stdout.write  ("Testing DMX ... ")
		dmx_interface.setall(20)
		dmx_interface.render()
		print "done"

	# TEST Sound
	sys.stdout.write ("Testing SOUND ... ")
	for n in NOTES:
		seg = Segment([0,0,n]);
		seg.play()
		time.sleep(0.3)
		seg.stop()
	seg.play("error")
	time.sleep(0.3)
	seg.stop()
	print "done"

	while RUN:

		# Read arduino serial
		val_read_raw = arduino.readline().strip()
		if val_read_raw != "":
			print val_read_raw
			val_read = val_read_raw.split(":")

			if CALIBRATING:
				if val_read[0] == 'Calibrated':
					if DMX_ENABLE:
						dmx_interface.setall(2)
						dmx_interface.render()
					CALIBRATING = False
					print "Now ready to play !"

			else:
				if val_read[0] == 'PIN':

					#Touch event
					if val_read[2] == '1':

						# Start Barriere on first touch
						if INIT_STATE:
							if DMX_ENABLE:
								dmx_interface.setall(0)
								dmx_interface.render()
							barriere.start()
							INIT_STATE = False

						# Transfer Touch Event
						else:
							barriere.touch(int(val_read[1]))

					#Release event
					else:
						if !INIT_STATE:
							barriere.release(int(val_read[1]))
