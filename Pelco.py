# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 15:19:33 2017

@author: yuriy
"""
import serial
import time
import io


class PelcoDevice:
     
   
    
    _device=[]
    _command=[]
    
    #connect
    def __init__(self,port='',baudrate=2400,timeout_=0):
        
        if port !='':
            self._device=serial.Serial(port,baudrate,timeout=timeout_)
            self._command=Frame()
        else: 
            print('No device is specified for connection')
    
    def unconnect(self):
        self._device.close()
    
    
    def move_while_stop(self,side):
        """ 'DOWN', 'UP'.'LEFT','RIGHT', 'STOP'"""
        cmd=self._command._construct_cmd(command2=side, pan_speed='\x00',tilt_speed='\x00')
        self._device.write(cmd)
        
    def move_by_step(self, side,time_step=0):
        """'DOWN', 'UP'.'LEFT','RIGHT', 'STOP', step= in microsec """
        self.move_while_stop(side)
        time.sleep(time_step)
        self.move_while_stop('STOP')
        
    def set_home_position(self):
        """As HOME Preset 11  - \x0B """
        cmd=self._command._construct_cmd(command2='\x03', pan_speed='\x00',tilt_speed='\x0B')
    
    def go_to_home(self):
        """As HOME Preset 11  - \x0B """
        cmd=self._command._construct_cmd(command2='\x07', pan_speed='\x00',tilt_speed='\x0B')
        self._device.write(cmd)
        
        
    def set_preset(self, num_preset):
        """ preset 1 - 255 . 11 used as Home"""
        cmd=self._command._construct_cmd(command2='\x03', pan_speed='\x00',tilt_speed=num_preset)
        self._device.write(cmd)
        
    def go_to_preset(self, num_preset):
        """ preset 1 - 255 . 11 used as Home"""
        cmd=self._command._construct_cmd(command2='\x07', pan_speed='\x00',tilt_speed=num_preset)
        self._device.write(cmd)
    
    def manual_command(self, com1,com2,data1,data2):
        cmd=self._command._construct_cmd(command1 = com1,command2=com2, pan_speed=data1, tilt_speed=data2)
        self._device.write(cmd)
        
        
class Frame:     
    # Frame format:		|synch byte|address|command1|command2|data1|data2|checksum|
	# Bytes 2 - 6 are Payload Bytes
    _frame = {
            'synch_byte':'\xFF',		# Synch Byte, always FF		-	1 byte
            'address':	'\x00',		# Address			-	1 byte
		     'command1':	'\x00',		# Command1			-	1 byte
		     'command2':	'\x00', 	# Command2			-	1 byte
		     'data1':	'\x00', 	# Data1	(PAN SPEED):		-	1 byte
		     'data2':	'\x00', 	# Data2	(TILT SPEED):		- 	1 byte 
		     'checksum':	'\x00'		# Checksum:			-       1 byte
             }
       
    _command2_code = {
			  'DOWN':	'\x10',
			  'UP':		'\x08',	
			  'LEFT':	'\x04',
			  'RIGHT':	'\x02',
			  'UP-RIGHT':	'\x0A',
			  'DOWN-RIGHT':	'\x12',
			  'UP-LEFT':	'\x0C',
			  'DOWN-LEFT':	'\x14',
			  'STOP':	'\x00',
            'ZOOM-IN':	'\x00',
            'ZOOM-OUT':	'\x00',
            'FOCUS-FAR':	'\x00',
            'FOCUS-NEAR':	'\x00'
              
			   }
     
    def __init__(self, adress=1):
        
        self._frame['address']=chr(adress)
        
    def _construct_cmd(self, command1 = '\x00',command2='\x00', pan_speed='\x00', tilt_speed='\x00' ):
        
        self._frame['command1']=command1
                   
        if command2 not in self._command2_code:
            if (type(command2) == str and (ord(command2)<255 and ord(command2)>=0)):
                self._frame['command2']=command2
            else:
                print('not command')
        else:
           self._frame['command2']=self._command2_code[command2] 
      
            
        
        self._frame['data1']=pan_speed
        self._frame['data2']=tilt_speed

        self._checksum(self._payload_bytes())
        cmd_str=self._frame['synch_byte']+self._payload_bytes()+self._frame['checksum']
        cmd=bytes('',encoding = 'utf-8')
        
        #Error result function bytes('\xFF',encoding = 'utf-8') is b'\xc3\xbf'
        for ch in cmd_str:
            if ch=='\xFF':
                cmd=b'\xFF'
            else:
                cmd=cmd+bytes(ch,encoding = 'utf-8')
        return cmd
 
   
    def _payload_bytes(self):
        return self._frame['address']+self._frame['command1']+\
                    self._frame['command2']+self._frame['data1'] +\
                    self._frame['data2']
    
    def _checksum(self,payload_bytes_string):
        self._frame['checksum']=chr(sum(map(ord, payload_bytes_string))% 256)
        



    
