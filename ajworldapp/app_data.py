from django.test import TestCase
import pandas as pd
import pyodbc 
import os
import glob
# Create your tests here.

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=192.168.0.117;'
                      'Database=AJWorldWide;'
                      'UID=ajview;'
                      'PWD=aj$%^World@123;'
                      'Trusted_Connection=no;'
                      )