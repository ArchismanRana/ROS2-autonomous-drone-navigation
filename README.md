# ROS2 Autonomous Drone Navigation

This project demonstrates an autonomous drone navigation system built using **ROS2, PX4 SITL, and Gazebo Sim**. The system is designed to operate in **GPS-denied environments**, where the drone relies on onboard perception, mapping, and path planning to navigate through complex environments such as mazes.

The repository includes multiple modules that demonstrate the full robotics pipeline—from algorithm prototyping to drone simulation.

To simplify development and testing, navigation algorithms are first implemented and validated using **ROS2 Turtlesim**, which provides a lightweight environment for testing control strategies and planning algorithms. These algorithms are then extended to a simulated drone using **PX4 SITL** and **Gazebo Sim**.

## Key Features

• ROS2-based modular robotics architecture
• Algorithm prototyping using Turtlesim
• Autonomous drone simulation with PX4 SITL and Gazebo Sim
• Global path planning using A* algorithm
• Offboard drone control through ROS2 nodes
• Modular package structure for perception, planning, and control

## System Architecture

Algorithm Prototyping (Turtlesim)
↓
Path Planning and Control Algorithms
↓
Gazebo Simulation Environment
↓
PX4 Offboard Control
↓
Autonomous Drone Navigation

## Technologies Used

* ROS2
* PX4 Autopilot
* Gazebo Sim
* Path planning algorithms (A*)
* Drone offboard control

This project aims to demonstrate how modern robotics frameworks can be used to develop autonomous aerial systems capable of navigating complex environments without relying on GPS.
