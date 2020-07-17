# Robot-Arm-Placing
This project provides two algorithms to insert FPCB in tray with Robot arm.


# Environment
##### Robot arm : HCR-3
##### Camera : Realsense2
##### GPU : GTX 1060 3g


# INDEX
### Optical Flow
### Polar coordinate
### Optical Flow + Polar coordinate


# Optical Flow

First algorithm is based on Optical Flow using [FlowNet2.0](https://github.com/lmb-freiburg/flownet2-docker).

There are three pre-processing steps and six processing steps.

![Untitled_Diagram_(1)](https://user-images.githubusercontent.com/54461378/87745856-010c8200-c82a-11ea-9b03-6b4bf5c5da06.jpg)

It is accurate, but can't specify running time, because in large displacement, it runs several time to get accurate angle.

If you want to see example processing of optical flow algorithm, see pdf file name 'processing.pdf' I attached. The file is written in Korean for presentation, but you can easily follow step by step with many example pictures.


# Polar coordinate

Second algorithm is based on polar coordinate using skimg library.

It is more faster than optical flow algorithm, but has consistent error because of 1d correlation. You can use this algorithm when you don't care about small error, or adjusting consistent error value.

If you want to see example processing of optical flow algorithm, see pdf file name 'processing.pdf' I attached. The file is written in Korean for presentation, but you can easily follow step by step with many example pictures.


# Optical Flow + Polar coordinate

This algorithm is for worse case. First and second algorithms are assuming perfect FPCB catching, but I don't provide catching algorithm, so it can be bad.

Algorithm is simple. Calculate optical flow for y axis translation once to calibrate reference image to bad case. Then, run polar coordinate algorithm with new reference image.

I don't attach code because our catching was good enough. However, I tested in several environment, so I have some example pictures. In 'processing.pdf', there are sample examples you can see.