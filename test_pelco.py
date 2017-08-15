# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 17:14:54 2017

@author: yuriy
"""

from Pelco import PelcoDevice




p=PelcoDevice(port='COM2', baudrate=2400,timeout_=0)

p.move_while_stop('DOWN')

p.move_while_stop('UP')
p.move_while_stop('RIGHT')
p.move_while_stop('LEFT')
p.move_while_stop('STOP')

p.move_by_step('RIGHT',0.001)

p.go_to_home()

p.set_preset('\x4D')

p.go_to_preset('\x0B')

p.unconnect()
