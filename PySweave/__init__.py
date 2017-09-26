
# import os, pkg_resources
import pkg_resources
version = pkg_resources.require(__package__)[0].version
print """
              This is {:s} version {:s} 
""".format( __package__, version )


## Import Classes
from .texFileHandler     import texFileHandler

