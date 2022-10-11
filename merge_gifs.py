#!/usr/bin/env python
# coding: utf-8

# Import required libraries
from PIL import Image, ImageSequence
import pandas as pd
import numpy as np
import time
import os
import random
import progressbar

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# transparent_foreground = Image.open(...)
background_gif = Image.open('./gifs/background_layer.gif')
bird_gif = Image.open('./gifs/bird_layer.gif')
weather_gif = Image.open('./gifs/weather_icon_layer.gif')

background_frames = []
bird_frames = []
weather_frames = []
frames = []
for frame in ImageSequence.Iterator(background_gif):
    frame = frame.copy()
    background_frames.append(frame)
for frame in ImageSequence.Iterator(bird_gif):
    frame = frame.copy()
    bird_frames.append(frame)
    # frame.paste(transparent_foreground, mask=transparent_foreground)
    # frames.append(frame)
for frame in ImageSequence.Iterator(weather_gif):
    frame = frame.copy()
    weather_frames.append(frame)

print(f'background frames: {len(background_frames)}')
print(f'bird frames: {len(bird_frames)}')
print(f'weather frames: {len(weather_frames)}')

if ((len(bird_frames) == len(weather_frames)) and (len(weather_frames) == len(background_frames))):
    bar = progressbar.ProgressBar(max_value=len(bird_frames))
    final_frames = []
    for n in range(len(bird_frames)):
        background_frame = background_frames[n]
        frame = background_frame.copy()

        bird_frame = bird_frames[n].convert("RGBA")
        x, y = bird_frame.size
        frame.paste(bird_frame, (0, 0, x, y), bird_frame)

        weather_frame = weather_frames[n].convert("RGBA")
        x, y = weather_frame.size
        frame.paste(weather_frame, (0, 0, x, y), weather_frame)

        final_frames.append(frame)
        bar.update(n)
    final_frames[0].save('./gifs/output.gif', save_all=True, append_images=final_frames[1:])
else:
    print('frames have differnt frame counts')
