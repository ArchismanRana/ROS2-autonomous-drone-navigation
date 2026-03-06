# ROS2 Autonomous Drone Navigation (Work in Progress)

This repository documents the development of an **autonomous drone navigation system using ROS2, PX4 SITL, and Gazebo Sim**. The goal of this project is to build a drone capable of navigating **GPS-denied environments** using onboard perception, mapping, and path planning algorithms.

----Project Status-----
This project is currently in the **early development stage**. Initial work focuses on learning and implementing the core robotics components such as ROS2 communication, simulation environments, and algorithm prototyping.

The long-term objective is to develop a complete autonomous navigation pipeline where a drone can explore and navigate complex environments such as **mazes or indoor spaces without relying on GPS**.

## Project Roadmap

The project will be developed step-by-step through the following stages:

1. **ROS2 Fundamentals**

   * Implement basic ROS2 nodes and communication
   * Test control algorithms using **ROS2 Turtlesim**

2. **Algorithm Prototyping**

   * Implement path planning algorithms (A*, Dijkstra, etc.)
   * Test navigation behaviors in simple simulated environments

3. **Drone Simulation**

   * Integrate **PX4 SITL** with **Gazebo Sim**
   * Simulate drone sensors such as LiDAR and depth cameras

4. **Autonomous Navigation**

   * Implement global and local path planning
   * Enable autonomous navigation in maze-like environments

5. **GPS-Denied Navigation**

   * Integrate mapping and localization
   * Enable fully autonomous drone navigation indoors

## Key Technologies

* **ROS2** – Robotics middleware and communication
* **PX4 Autopilot** – Drone flight control software
* **Gazebo Sim** – Robotics simulation environment
* **Python / C++** – Algorithm and control implementation

## Vision

The final goal of this project is to create a **fully autonomous drone system capable of navigating complex environments without GPS**, demonstrating the integration of perception, planning, and control within the ROS2 ecosystem.
