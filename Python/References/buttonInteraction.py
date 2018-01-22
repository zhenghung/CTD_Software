from tkinter import *
from tkinter import ttk
global cs_config, ser

"""
States
---------
'STARTUP'
'COM_STANDBY'
'COM_M1'
'COM_M2'
'COM_DONE'
'COM_RESET'
'MOI_STANDBY'
'MOI_M!'
'MOI_M2'
'MOI_M3'
'MOI_DONE'
'MOI_RESET'

Buttons
---------
 0: 'connectArduino'
 1: 'comStandby'
 2: 'com_reset'
 3: 'com_m1'
 4: 'com_m2'
 5: 'com_done'
 6: 'moi_standby'
 7: 'moi_reset'
 8: 'moi_m1'
 9: 'moi_m2'
10: 'moi_m3'
11: 'moi_done'



"""
global state
state = 'STARTUP'

class buttonInteraction(object):
	def startup(allbuttons):
		for i in range(1, 12): 
			allbuttons[i].config(state=DISABLED)

	def refreshButtons(lastButton, state, allbuttons):
		if(state=='STARTUP'):
			if(lastButton=='connectArduino'):
				somefunction()
			elif(lastButton=='comStandby'):
				somefunction()
			elif(lastButton=='com_m1'):	
				somefunction()		
			elif(lastButton=='com_m2'):
				somefunction()
		elif(state=='COM_STANDBY'): 
			if(lastButton=='connectArduino'):
				somefunction()
			elif(lastButton=='comStandby'):
				somefunction()
			elif(lastButton=='com_m1'):	
				somefunction()		
			elif(lastButton=='com_m2'):
				somefunction()
		elif(state=='COM_M1'):
			if(lastButton=='connectArduino'):
				somefunction()
			elif(lastButton=='comStandby'):
				somefunction()
			elif(lastButton=='com_m1'):	
				somefunction()		
			elif(lastButton=='com_m2'):
				somefunction()
		elif(state=='COM_M2'):
			if(lastButton=='connectArduino'):
				somefunction()
			elif(lastButton=='comStandby'):
				somefunction()
			elif(lastButton=='com_m1'):	
				somefunction()		
			elif(lastButton=='com_m2'):
				somefunction()
		elif(state=='COM_DONE'):
			if(lastButton=='connectArduino'):
				somefunction()
			elif(lastButton=='comStandby'):
				somefunction()
			elif(lastButton=='com_m1'):	
				somefunction()		
			elif(lastButton=='com_m2'):
				somefunction()
		elif(state=='COM_RESET'):
			if(lastButton=='connectArduino'):
				somefunction()
			elif(lastButton=='comStandby'):
				somefunction()
			elif(lastButton=='com_m1'):	
				somefunction()		
			elif(lastButton=='com_m2'):
				somefunction()
		elif(state=='MOI_STANDBY'):
			if(lastButton=='connectArduino'):
				somefunction()
			elif(lastButton=='comStandby'):
				somefunction()
			elif(lastButton=='com_m1'):	
				somefunction()		
			elif(lastButton=='com_m2'):
				somefunction()
	def somefunction():
		print(1)