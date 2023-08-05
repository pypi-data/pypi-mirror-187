'''
Date         : 2022-12-18 12:32:53
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-01-20 13:11:17
LastEditors  : BDFD
Description  : 
FilePath     : \WES_Calculation\__init__.py
Copyright (c) 2022 by BDFD, All Rights Reserved. 
'''

from .templateproj import add_one
from .templateproj import add_two
from .gumbel import gumbel
from .greenampt import greenampt
from .wavespectra import wave
from .windspeed import windspeed
from .preprocess.pre_gumbel import pre_gumbel as gu
from .preprocess.pre_greenampt import pre_greenampt as ga 
from .preprocess.pre_wavespectra import pre_wavespectra as wa
from .preprocess.pre_windspeed import pre_windspeed as ws



