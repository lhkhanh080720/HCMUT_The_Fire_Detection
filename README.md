# HARDWARE 
#### Block diagram system
![example1](Pic/SoDoKhoi.png)
- **Source Block**: Automatic power switching from the main to backup source when main source has the problem.
- **System Block**: Use Jetson Nano combines with some basic circuits for control servos and water pump.
- **Display Block**: Using an ethernet wire to connect from Jetson Nano to Laptop to control and monitor the system in Jetson Nano. 
#### Using "Altium Designer" to make a circuit
![example1](Pic/line12.png)
- Source link: ..... 
#### Result    
![example1](Pic/line11.png)
![example1](Pic/line9.png)
![example1](Pic/line10.png)
***
# SOFTWARE 
#### AI
- Using model YOLOv4-tiny and training in Google Colab with:
  - 1 class: fire
  - Epochs: 6000
  - Dataset: ~1000 images
![example1](Pic/line13.png)
*(Accuracy ~ 80%)*
  - Testing the model by images, not in dataset:
![example1](Pic/line24.png)
![example1](Pic/line25.png)
  - Testing the model by actual video: [Resultvideo.mp4][1]


[1]: <https://github.com/lhkhanh080720/Code_DetectFire/blob/main/Pic/Resultvideo.mp4>

#### GUI

