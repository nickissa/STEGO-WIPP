# Unsupervised Autonomous Inspection of the Waste Isolation Pilot Plant Using STEGO
Autonomous Object and Creep Prediction for the Department of Energy's (DOE) Waste Isolation Pilot Plant (WIPP) Using STEGO (https://github.com/mhamilton723/STEGO)

## Compatability Notes
- Built on Python 3.8.16 with Ubuntu 22.04
- Pytorch 2.0
- Cuda v11.7
- Maximum of sm_86 GPU architecture (Built based on Geforce RTX 3060)
- NVIDIA v530 drivers (CUDA 12.1 built in)
- cuDNN v8.8.1

## Start
1. Open the file /src/STEGO_WIPP.py
2. Change the directory variables and video name to fit your system
3. Run code
4. Results will be in src/videos

## Docker Start
1. Create Docker image locally:
```
docker build -t stegowipp # stegowipp can be replaced with any name you want
```
2. Run Docker image to create Docker container:
```
docker run stegowipp # if stegowipp wasn't used on image name, use the name chosen in the previous step
```

## TODO
1. Fix resolution to fit 1920 x 1080.
2. Get working with GPU.
3. Grab the numpy arrays before they are processed.
