"""===================================
-*- coding: utf-8 -*-
    @Time    : 2019/10/8 19:45
    @Author  : Xu Kaixin
    @FileName: video_sampler.py
    @Software: PyCharm
======================================"""

import cv2
import os
from tqdm import tqdm
from fire import Fire


def sample(kwargs):
    file_path = kwargs.get("file_path")
    interval = kwargs.get("interval")
    output_dir = kwargs.get("output_dir")

    assert os.path.exists(file_path), f"{file_path} not exists"

    cap = cv2.VideoCapture(file_path)
    assert interval < cap.get(cv2.CAP_PROP_FRAME_COUNT)
    c = 0
    if output_dir not in os.listdir():
        os.mkdir(output_dir)
    with tqdm(total=cap.get(cv2.CAP_PROP_FRAME_COUNT) // interval) as t:
        t.set_description(f"Capturing {cap.get(cv2.CAP_PROP_FRAME_COUNT) // interval} frames from the video")
        while cap.isOpened():
            ret, frame = cap.read()
            if not c % interval:
                cv2.imwrite(f"{output_dir}/{c // interval}.jpg", frame)
                t.update(c)
                c += 1
    cap.release()


if __name__ == "__name__":
    Fire()
