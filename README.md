# Temperaturas segun estación meteorológica en chile
Proyecto Webscraping temperaturas absolutas maxima chile.

Se extrae la informacion desde el INE, chile.

Se requieren las siguientes bibliotecas, las cuales se deben instalar mediante pip

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import undetected_chromedriver as uc
import time
import re
import os

el script se debe ejecutar con el siguiente codigo:

  python max_abs_temp_chile.py


