# -*- coding: utf-8 -*-

## \package functions.commandcheck


import os, commands


## Check if a command is available on the system
#  
#  The system's 'whereis' command is used to
#    find locations for the target command.
#    If one of those locations is found to
#    be an executable file, a tuple containing
#    a True value & the location to the executable
#    is returned.
#  \param cmd
#        \b \e unicode|str : Command to check for
#  \return
#        \b \e tuple : Tuple containing True/False value &, if True, the string location of the command
def CommandExists(cmd):
    locations = commands.getoutput(u'whereis {}'.format(cmd)).split(u':'.format(cmd))[-1]
    
    if len(locations):
        locations = locations.split(u' ')
        
        l_index = 0
        for L in locations:
            l_index += 1
            
            if not os.path.isdir(L) and os.access(L, os.X_OK):
                # Use the first instance found
                return (True, L)
    
    return (False, None)
