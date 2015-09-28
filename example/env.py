import sys
import os

this = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
sys.path.append("/".join(this.split("/")[:-1]))
