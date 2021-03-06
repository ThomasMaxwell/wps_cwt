import os
import json
import random
import cdms2
from data_collections import CollectionManager
from wps import settings
from modules.utilities import wpsLog

cdms2.setNetcdfShuffleFlag(0)
cdms2.setNetcdfDeflateFlag(0)
cdms2.setNetcdfDeflateLevelFlag(0)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))

class DataAnalytics:

    def __init__( self, operation ):
        self.operation = operation

    def location2cdms(self,region):
        kargs = {}
        for k,v in region.iteritems():
            if k not in ["id","version"]:
                kargs[str(k)] = float( str(v) )
        return kargs

    def region2cdms(self,region):
        kargs = {}
        for k,v in region.iteritems():
            if k in ["id","version"]:
                continue
            if isinstance( v, float ) or isinstance( v, int ):
                kargs[str(k)] = (v,v,"cob")
            else:
                system = v.get("system","value").lower()
                if isinstance(v["start"],unicode):
                    v["start"] = str(v["start"])
                if isinstance(v["end"],unicode):
                    v["end"] = str(v["end"])
                if system == "value":
                    kargs[str(k)]=(v["start"],v["end"])
                elif system == "index":
                    kargs[str(k)] = slice(v["start"],v["end"])
        return kargs

    def loadFileFromCollection( self, collection, id=None ):
        collectionManager = CollectionManager.getInstance( settings.CDAS_APPLICATION )
        url = collectionManager.getURL( collection, id )
        wpsLog.debug( "loadFileFromCollection: '%s' '%s': %s " % ( collection, id, url ) )
        return self.loadFileFromURL( url )

    def loadFileFromURL(self,url):
        ## let's figure out between dap or local
        if url[:7].lower()=="http://":
            f=cdms2.open(str(url))
        elif url[:7]=="file://":
            f=cdms2.open(str(url[6:]))
        else:
            # can't figure it out skipping
            f=None
        return f

        # self.envs = {
        #         "path":"PATH",
        #         "addonPath":"GRASS_ADDON_PATH",
        #         "version":"GRASS_VERSION",
        #         "gui":"GRASS_GUI",
        #         "gisbase": "GISBASE",
        #         "ldLibraryPath": "LD_LIBRARY_PATH"
        # }


    def saveVariable(self,data,dest,type="json"):
        cont = True
        while cont:
            rndm = random.randint(0,100000000000)
            fout = os.path.join(BASE_DIR,"%i.nc" % rndm)
            fjson = os.path.join(BASE_DIR,"%i.json" % rndm)
            cont = os.path.exists(fout) or os.path.exists(fjson)
        f=cdms2.open(fout,"w")
        f.write(data)
        f.close()
        out = {}
        out["url"] = "file:/"+fout
        out["id"]=data.id
        Fjson=open(fjson,"w")
        json.dump(out,Fjson)
        Fjson.close()
        dest.setValue(fjson)

    # def breakpoint(self):
    #     try:
    #         import pydevd
    #         pydevd.settrace('localhost', port=8030, stdoutToServer=False, stderrToServer=True)
    #     except: pass


if __name__ == "__main__":
    da = DataAnalytics('')
    id = 'clt'
    ds = da.loadFileFromCollection( 'MERRA/mon/atmos', id )
    v = ds[id]