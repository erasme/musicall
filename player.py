#!usr/bin/env python  
#coding=utf-8 

import serial
import subprocess
import os

from threading import Thread
import time


sounds = ["Sol.wav", "Do.wav", "Do_aigu.wav", "Fa.wav"]
NB_BARREAU = 2
BPM = 0.5


SOUND_PATH = os.path.join(os.getcwd(), "sons")

sequence = [ None for b in range(0, NB_BARREAU)]

class Player(Thread): 

    def __init__(self, nom = ''): 
        Thread.__init__(self) 
        self.Terminated = False 
    
    def run(self): 
        i = 0 
        while not self.Terminated: 
            
            time.sleep(BPM)
            print "Barreau %s/%s"%(i,NB_BARREAU)
            if i < NB_BARREAU: 
                print i, sequence[i]
                if sequence[i] != None:
                    path = os.path.join(SOUND_PATH, sounds[sequence[i]])
                    proc = play(path)
                    # self.stdout, self.stderr = proc.communicate()
                    
                i += 1 
            else :
                i = 0
 
        print "le thread "+self.nom +" s'est termine proprement" 
    
    def stop(self): 
        self.Terminated = True

# Création des threads
player = Player()

# Lancement des threads
player.start()

def play(audio_file_path):

    print "Playing sound : %s"%(audio_file_path)
                    
    
    # apple
    proc = subprocess.Popen(["afplay", audio_file_path])

    return proc

    # linux
    # subprocess.call(["ffplay", "-nodisp", "-autoexit", audio_file_path])

RUN = True

# Main
if __name__ == '__main__':

    # Open arduino Serial // timeout for the readline function (adjust to prevent sound chop)
    arduino = serial.Serial('/dev/tty.usbmodem1411', 9600, timeout=0.1)

    # Main LOOP
    while RUN:
        
        # Read arduino serial
        val_read_raw = arduino.readline().strip()

        if val_read_raw != "":
            val_read = val_read_raw.split(":")
            
            barreau_id = int(val_read[0])-1
            note = int(val_read[1])
            sequence[barreau_id] = note


            # path = os.path.join(SOUND_PATH, sounds[sequence[barreau_id]])
            # print path
            # play(path)
            


        print sequence

