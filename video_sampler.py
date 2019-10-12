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

def adaptive_resize(img):
    h, w, _ = img.shape
    if min(h, w) >= 1080:
        fac = max(h, w) // 1080
        return cv2.resize(img, (w // fac, h // fac))


def sample(**kwargs):
    vid_dir = kwargs.get("vid_dir")
    interval = kwargs.get("interval")
    output_dir = kwargs.get("output_dir")
    print(kwargs)
    assert os.path.exists(vid_dir)

    for i, file in enumerate(os.listdir(vid_dir)):
        if file.split(".")[-1] in ["avi", "mp4"]:
            file_path = os.path.join(vid_dir, file)
            output_subdir = os.path.join(output_dir, f"{i:04d}")
            if output_subdir not in os.listdir(output_dir):
                os.mkdir(output_subdir)
            cap = cv2.VideoCapture(file_path)
            assert interval < cap.get(cv2.CAP_PROP_FRAME_COUNT)
            c = 0
            with tqdm(total=cap.get(cv2.CAP_PROP_FRAME_COUNT) // interval) as t:
                t.set_description(f"Capturing {cap.get(cv2.CAP_PROP_FRAME_COUNT) // interval} frames from {file}")
                ret = True
                while ret:
                    ret, frame = cap.read()
                    if not c % interval:
                        # img = frame[: (7 * len(frame)) // 8, :, :]
                        img = frame
                        cv2.imwrite(f"{output_subdir}/{c // interval}.jpg", adaptive_resize(img))
                        t.update(1)
                    c += 1
            cap.release()

def resize(**kwargs):
    in_dir = kwargs.get("in_dir")
    out_dir = kwargs.get("out_dir")
    assert os.path.exists(in_dir)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    for i, file in enumerate(os.listdir(in_dir)):
        file_path = os.path.join(in_dir, file)
        wtie_path = os.path.join(out_dir, file)
        cv2.imwrite(wtie_path, adaptive_resize(cv2.imread(file_path)))
        

if __name__ == "__main__":
    import fire
    fire.Fire()
