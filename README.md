# Blimp Vision System

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white)
![Blender](https://img.shields.io/badge/blender-%23F5792A.svg?style=for-the-badge&logo=blender&logoColor=white)

Detection and pose estimation of an autonomous blimp using machine learning with CG training and testing images, for use in a navigation system.

![detection 1](https://github.com/ChickenKorma/Blimp-Vision-System/assets/35520562/68bfa983-05b6-4bd6-b086-fd863fb9e514)

## Describe the problem

The University of Southampton wanted a small, autonomous, indoor blimp in the sports hall to be used as advertising for the Aeronautics/Astronautics course on open days. This project was tasked to design a vision based navigation system for collision avoidance using only fixed, external, optical (as opposed to depth) cameras, therefore it had to be real time and a lot of conventional pose estimation was unsuitable. Furthermore, the blimp had not been made and so any training/testing had to be done using synthetic data (CG images of the blimp).

## System Architecture

I used a combination of two neural networks, splitting the task into an object detection stage (identifying the blimp in a video frame) and a pose estimation stage (predicting the 6D pose of the blimp). It was hoped that extracting only the necessary area of the video frame would improve the pose estimation performance since neural networks typically use depth sensors or depth cameras, while our application only considers the use of standard cameras. For the object detection stage I used the existing YOLO v5 model but created a custom model for pose estimation. There was also camera normalization to remove any distortion.

![System Architecture](https://github.com/ChickenKorma/Blimp-Vision-System/assets/35520562/05a48fb7-a57d-4574-9ae3-537de83d106f)

## Blender and CG image generation

A synthetic data set (CGI) was made using python scripting in Blender, by applying constrained, random positions and orientations. Pose and bounding box data was extracted using the Blender Python API.

![image_596](https://github.com/ChickenKorma/Blimp-Vision-System/assets/35520562/001ed4a1-bc5f-436a-84a6-b558616b8ed2)
