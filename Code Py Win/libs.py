from tkinter import *
import tkinter
from tkinter.ttk import * #for combobox
import cv2
import PIL.Image, PIL.ImageTk
from threading import Thread
from datetime import datetime

import os
import time
import argparse # Library support Command Line Interface (CLI)
import numpy as np
import serial

import cv2
import pycuda.autoinit  # This is needed for initializing CUDA driver

from utils.yolo_classes import get_cls_dict
from utils.camera import add_camera_args, Camera
from utils.display import open_window, set_display, show_fps
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO