########################### Map dose ###################
import Globals
import tkinter as tk
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL, simpledialog, PhotoImage, BOTH
import os
from os.path import normpath, basename
import cv2
from cv2 import imread, IMREAD_ANYCOLOR, IMREAD_ANYDEPTH, imwrite
import numpy as np
import SimpleITK as sitk
import pydicom
from PIL import Image, ImageTk



#laste opp bilde og markere i bildene, egen funksjon
#gammatest, lese opp på det og implementere
#Eksportere figurer og dataset ut av programmet
#må lagre siste kalibrering (spørre hvilken kalibrering bruker vil bruke)
# hvordan er doseplanene lagret.


# Laste opp doseplan (for nå er det en enkel matrise, selvkonstruert.)
# laste opp skannet film, korriger automatisk.
# brukeren spesifiserse posisjon på film
# gjøre film om til dose map (bruke dose response)
# tegne dose plan og dose map fra film
# regne gamma
# tegne gamma pass/fail og variasjoner
# skriv ut all info vi får fra gammatest
