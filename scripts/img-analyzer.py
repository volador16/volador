# -*- coding: utf-8 -*-
"""
这个脚本用于接收kafka screen topic消息，并对捕获的屏幕进行分析
@author: voloader
"""
import os
from kafka import KafkaConsumer
import cv2
import numpy as np


