import os
from os.path import join

# Grab environment variables or set default local ones
if os.getenv('ROOTDIR'):
    ROOTDIR = os.getenv('ROOTDIR')      # root directory
    SRCDIR = os.getenv('SRCDIR')        # source code directory
    RESULTS = os.getenv('RESULTS')      # resulting video directory
    TEMPIMG = os.getenv('TEMPIMG')      # temporary image directory

    PRCMODE = os.getenv('PRCMODE')      # either 'linear' or 'cluster'
    VIDEO = os.getenv('VIDEO')          # location of prerecorded video

else:
    ROOTDIR = os.path.abspath("../")
    SRCDIR = os.path.join(ROOTDIR, "src/")
    RESULTS = os.path.join(ROOTDIR, "src/videos/processed/")
    TEMPIMG = os.path.join(ROOTDIR, "src/videos/tempimages/")

    PRCMODE = "linear"
    VIDEO = os.path.join(ROOTDIR, "src/videos/<video_name>") # CHANGE THIS TO FIT VIDEO NAME

os.chdir(SRCDIR)
saved_models_dir = join("..", "saved_models")
os.makedirs(saved_models_dir, exist_ok=True)

import wget
saved_model_url_root = "https://marhamilresearch4.blob.core.windows.net/stego-public/saved_models/"
saved_model_name = "cocostuff27_vit_base_5.ckpt"
if not os.path.exists(join(saved_models_dir, saved_model_name)):
    wget.download(saved_model_url_root + saved_model_name, join(saved_models_dir, saved_model_name))

from train_segmentation import LitUnsupervisedSegmenter

model = LitUnsupervisedSegmenter.load_from_checkpoint(join(saved_models_dir, saved_model_name)).cuda()

from PIL import Image
import requests
from io import BytesIO
from torchvision.transforms.functional import to_tensor
from utils import get_transform
import cv2
import torch.nn.functional as F
from crf import dense_crf
import torch
import time
import numpy as np

# Pre-recorded video
vid = cv2.VideoCapture(VIDEO)

# TODO: Fix resolution to fit 1920 x 1080
# Resolution of vid
# size = (
#     int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
#     int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
# )

# Works defaultly since STEGO processes images with shape (448, 448, 3)
size = (448, 448)

# Set properties of output video/image to be read in
codec = cv2.VideoWriter_fourcc(*'mp4v')
output = cv2.VideoWriter(os.path.join(RESULTS, 'ProcessedVidSTEGOWIPP.avi'), codec, 30.0, size)

filename = 'tempimage.png'
os.chdir(TEMPIMG)

starttime = time.time()

while(True):
    ret, frame = vid.read()
    if ret == False:
        break
        
    # Read in images/video
    
#    # APPROACH #1
# --------------------------------------------------------------------------------------------------
#    # This approach is interesting because its got a blue tint with some edge/object identification
#     img = Image.fromarray(frame, mode="RGB")
#     transform = get_transform(448, False, "center")
#     img = transform(img).unsqueeze(0).cuda()
# --------------------------------------------------------------------------------------------------
    
    # APPROACH #2
# --------------------------------------------------------------------------------------------------
    # Save frame as 'tempimage.png' each time and process that file
    cv2.imwrite(filename, frame)
    img = cv2.imread(os.path.join(TEMPIMG, filename))
    img = Image.fromarray(img, mode="RGB")
    transform = get_transform(448, False, "center")
    img = transform(img).unsqueeze(0).cuda()
# --------------------------------------------------------------------------------------------------
    
    # Process images/video
    with torch.no_grad():
        code1 = model(img)
        code2 = model(img.flip(dims=[3]))
        code  = (code1 + code2.flip(dims=[3])) / 2
        code = F.interpolate(code, img.shape[-2:], mode='bilinear', align_corners=False)
        
        if PRCMODE == "linear":
            linear_probs = torch.log_softmax(model.linear_probe(code), dim=1).cpu()
            single_img = img[0].cpu()
            linear_pred = dense_crf(single_img, linear_probs[0]).argmax(0)
            linearres = model.label_cmap[linear_pred].astype('uint8')

            # Save processed images/video
            output.write(linearres)
            cv2.imshow('Linear Predictions', linearres)

        if PRCMODE == "cluster":
            cluster_probs = model.cluster_probe(code, 2, log_probs=True).cpu()
            single_img = img[0].cpu()
            cluster_pred = dense_crf(single_img, cluster_probs[0]).argmax(0)
            clusterres = model.label_cmap[cluster_pred].astype('uint8')

            # Save processed images/video
            output.write(clusterres)
            cv2.imshow('Cluster Predictions', clusterres)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

vid.release()
output.release()
cv2.destroyAllWindows()

endtime = time.time()
totaltime = endtime - starttime
print('Total Time Taken:', totaltime / 60, 'min(s)')