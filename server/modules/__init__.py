import os
import traceback
import importlib
from utilities import wpsLog

class ModuleRegistry:

    def __init__( self, name, directory, package_path ):
        wpsLog.debug( "Init '%s' Module Registry:  dir='%s' package='%s'" % ( name, directory, package_path ) )
        self.name = name
        self._registry = {}
        subdirs = [ o for o in os.listdir(directory) if os.path.isdir(os.path.join(directory,o)) ]

        for modulename in subdirs:
            try:
                module = importlib.import_module( "."+modulename, package_path )
                if hasattr( module, 'getConstructor' ):
                    constructor = module.getConstructor()
                    self._registry[modulename] = constructor
                    wpsLog.debug( "Registering %s '%s'" % ( self.name, modulename ) )
            except Exception:
                wpsLog.warning( "\n --------------- Error Registering %s '%s' --------------- \n %s" % ( self.name, modulename, traceback.format_exc() ) )

    def getInstance( self, key  ):
        constructor = self._registry.get( key, None )
        wpsLog.debug( "  Using %s '%s': %s " % ( self.name, key, str(type(constructor)) ) )
        return constructor(key)


class Module:

    def __init__( self, id ):
        self.id = id


class Executable(Module):

    def execute( self, run_args ):
        raise Exception( "Attempt to execute virtual Executable base class" )




