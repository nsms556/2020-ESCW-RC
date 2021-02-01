# 2020-ESWC-RC
주행보조 기능을 탑재한 RC카
 - 개발 기간 : 2020.02 ~ 2020.10.02
 - 2020 임베디드 소프트웨어 경진대회 자유 공모 참가
 - Wii-RCCAR 프로젝트 종료 이후 추가 개발 

---
- NVIDIA Jetson Nano Development Kit
- Intel Dual Band Wireless - AC 8265
- Wii Remote Controller
- HC-SR04P Ultrasonic Wave Sensor
- ODROID S604HD Webcam
- DC모터, 서보모터, LED 등 기타 하드웨어
- Python
- OpenCV, PyTorch, cwiid, GPIO 라이브러리
- PyTorch-YOLO 객체 탐지 모델

## 개요
 - 카메라를 통해 전방의 영상을 촬영
 - GPU 기반 머신러닝을 활용한 표지판 탐지 기능
 - OpenCV를 사용한 영상처리로 차선 유지 기능
 - 초음파 센서를 사용한 후방 충돌 방지 기능
 - Google Colabolatory를 통해 모델 학습, 학습된 모델을 탐지 알고리즘에 적용
 
## Need Library
 + PyTorch-YOLOv3
 + cwiid

## Reference
 + https://github.com/eriklindernoren/PyTorch-YOLOv3
 + https://github.com/abstrakraft/cwiid
 + https://pypi.org/project/cwiid/
 + https://github.com/dctian/DeepPiCar
