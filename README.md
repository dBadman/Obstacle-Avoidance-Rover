# Obstacle-Avoidance-Rover
# 
# There is a 3-wheeled rover, driven by a 12V DC motor and steered by a 6V Servo Motor. The rover contains 4 ultrasonic sensors that determine distance of obstacles in 4 directions: straight ahead, 30 degrees to the left and right, and straight behind. 
# The sensors and motors are wired to a Raspberry Pi, all powered by two batteries, one 12V and one 6V. There is a driver motor to handle forward and backward driving.
# A shell (startWalk.sh) script starts the Python program (Robot_Walk.py). Robot_Walk.py brings the robot into forward motion and starts polling the ultrasonic sensors and performing distance calculations. The rover's movements are determined by the distance information. 
# The idea is that the rover navigates an unknown course while avoiding obstacles. The ideal maneuverability is smooth and accurate. 

# A future state is that the rover also maps its environment in real time. 
