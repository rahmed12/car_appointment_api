'''
Runner for all tests.py in each directory
'''

# set the path of the file (one dir up of the file) into sys path
import os, sys
sys.path.append(os.path.abspath((os.path.join(os.path.dirname(__file__), '..'))))


import unittest

# import from the file tests.py of the folder app_auth and appt
# so we can run all tests.py
from app_auth.tests import AppAuthTest
from appt.tests import ApptsTest


if __name__ == '__main__':
    unittest.main()
