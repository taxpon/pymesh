import sys
import os

this = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, "/".join(this.split("/")[:-1]))
# sys.path.append("/".join(this.split("/")[:-1]))
