import sys
import math
import numpy
import pyaudio
import signal as syssig
from scipy import signal
import serial

RUN = True
RATE = 44100

# CTRL-C Handler
def signal_handler(signal, frame):
	global RUN
	RUN = False
	print('You pressed Ctrl+C!')
	
# Prepare a sample array (frequency: Hz / length: Seconds)
def sample(frequency, length=0.1):
	length = int(RATE * length)
	factor = float(frequency) * (math.pi * 2) / RATE
	return numpy.arange(length) * factor

# Make a sample of Sinus wave
def sine(frequency):
    return numpy.sin( sample(frequency) )

# Make a sample of Square wave
def square(frequency, pulsewidth=0.5):
    return signal.square( sample(frequency), pulsewidth )

# Play sample on stream pipe
def play_tone(stream, sample):
    chunks = []
    chunks.append( sample )
    chunk = numpy.concatenate(chunks) * 0.25
    stream.write(chunk.astype(numpy.float32).tostring())

# Test if value is INT
def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

# Main
if __name__ == '__main__':

	# Open arduino Serial // timeout for the readline function (adjust to prevent sound chop)
	arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=0.1)
	
	# Handle CTRL-C
	syssig.signal(syssig.SIGINT, signal_handler)
	
	# Prepare audio interface
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paFloat32, channels=1, rate=RATE, output=1)
	
	waves = []
	values = []
	
	# Main LOOP
	while RUN:
		
		# Read arduino serial
		val_read = arduino.readline().strip().split('/');
		if val_read[-1] == '$':
			del val_read[-1]
			
			# New values received
			if values != val_read:
				values = val_read
				print values
				waves = []
				
				# Populate array of samples (waves)
				for i, val in enumerate(values):
					if isInt(val) and int(val) > 0:
						ha = 220+(220/12)*2*i
						print ha
						waves.append( sine( int( ha ) )
						
				# print waves
				# Apply volume to each sample	
				if len(waves) :
					for k, wav in enumerate(waves):
						waves[k] = wav*1.5/len(waves)
		
		# Play mixed samples
		if len(waves) > 0:
			play_tone(stream, sum(waves))

	# Close & Exit
	stream.close()
	p.terminate()
	sys.exit(0)
    
	
