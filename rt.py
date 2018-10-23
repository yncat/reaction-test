# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from dialog import *
import sys
import random

class TriggerHandler:
	results=[]#Results list
	tries=5#Number of tries, overwritten by constructor parameter
	triggerTick=0#Tick value where the pop event is fired
	triggerStartTick=0#The actual tick that the pop event was fired
	isActive=False#Being popped?
	popSound=None
	pushSound=None
	errorSound=None
	def __init__(self,numTries):
	#Parameter: Number of Tries.
		self.tries=numTries
		self.popSound=pygame.mixer.Sound("snd/pop.wav")
		self.pushSound=pygame.mixer.Sound("snd/push.wav")
		self.errorSound=pygame.mixer.Sound("snd/error.wav")
	#end def __init__
	def getTries(self):
		return self.tries
	#end def getTries
	def update(self):
		#Must be called once per frame
		tick=pygame.time.get_ticks()
		if not self.isActive and tick>=self.triggerTick: self.pop()
	#end def update
	def pop(self):
		#Must not be called from outside
		self.triggerStartTick=pygame.time.get_ticks()
		self.popSound.play()
		self.isActive=True
	#end def pop
	def push(self):
		# Must call this function when the trigger key is pressed. If it's not popping, makes the current result to 0 (fail). Returns True if the main loop should end.
		if self.isActive:
			self.results.append(pygame.time.get_ticks()-self.triggerStartTick)
			self.pushSound.play()
		else:
			self.results.append(0)
			self.errorSound.play()
		#end if
		self.isActive=False
		return len(self.results)==self.tries
	#end def push
	def setNext(self):
		#Sets the next trigger (in between 1000-20000 msec)
		self.triggerTick=pygame.time.get_ticks()+random.randint(1000,20000)
	#end def setNext
	def makeResultString(self):
	#Prints average / each time to the return value
		ret=""
		num=0
		total=0
		for elem in self.results:
			if elem>0:
				num+=1
				total+=elem
			#end if
		#end for
		if num==0:
			ret+="Average: None\n"
		else:
			average=total/num
			ret+="Average: %d ms\n" % average
		#end if num==0
		count=0
		for elem in self.results:
			count+=1
			ret+="%d: " % count
			if elem==0:
				ret+="Fail"
			else:
				ret+="%d ms" % elem
			#end if
			ret+="\n"
		#end for
		return ret
	#end def makeResultString
#end class

def main():
	pygame.mixer.pre_init(44100,-16,2,512)
	pygame.init()
	if pygame.mixer.get_init() is None: raiseError("Mixer is not initialized.")
	trigger=TriggerHandler(5)
	dialog("How to play","Press enter or spacebar as soon as possible when you hear a beep. You have %d tries and the average of your response time will be given." % trigger.getTries())
	clock=pygame.time.Clock()
	screen = pygame.display.set_mode((600, 400))
	pygame.display.set_caption("Reaction test")
	trigger.setNext()
	ended=False
	while(True):
		clock.tick(60)
		trigger.update()
		screen.fill((255,63,10,))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE : onexit()
				if event.key in (K_RETURN, K_SPACE):
					ended=trigger.push()
					if not ended: trigger.setNext()
				#end push
			#end keydown
			if event.type == QUIT: onexit()
		#end event
		if ended: break
	#end main loop
	dialog("Result",trigger.makeResultString())
#end def main
def onexit():
	pygame.quit()
	sys.exit()

def raiseError(msg):
	dialog("Error",msg)
	sys.exit()

#global schope
if __name__ == "__main__": main()