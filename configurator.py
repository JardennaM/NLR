import os
import sys

current_directory = os.getcwd()
sys.path.insert(0, '%s/config'%current_directory)
sys.path.insert(0, '%s/objects'%current_directory)