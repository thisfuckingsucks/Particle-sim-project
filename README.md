# Particle Simulation

## Description
This a particle simulation you can play around with where you can edit the properties of particles. Features include setting particle properties such as amount, size, mass, velocity, gravity, and elasticity. Indivual particles can also be modified before simulation begins. During simulation, a pulling force can also be applied to the scene using your mouse.

## How to run
Just download all python files together and run 'simulation.py' to start the simulation. Editing the global parameters will require interacting with the console output.

## Usage
https://www.youtube.com/watch?v=crOnPfwzDtM&authuser=0
### Controls
start screen '0' and '1' for options\
simulation set up screen 'Left' and 'Right' to select particle\
'q' 'w' 'e' 'r' 't' 'y' 'u' 'i' 'o' 'p' to select particle property\
'Up' and 'Down' to adjust property\
'0' to start simulation\
During simulation 'LMB' to creat pulling force\
'RMB' to cancel

## Project design and implementation
![Untitled683_20241216234150](https://github.com/user-attachments/assets/4b129da4-b4ef-447b-9dc1-1cf468309a42)
The Ball class is supposed to be a particle that will be used for simulation in the Simulation class. And the Text class provides and easier way to display text than python turtle in the Simulation class.
### Provided code uses
The provided event driven simulation code was modified to a time driven simulation one due to the provided code sometimes not working correctly when implementing curved particle movement at the start of the project.
And the code for user interactivities were used as a reference for implementing features of the same manner in this project.
### Testing
After getting the simulation to not have any obvious errors, physics was used to ensure everything was working correctly, such as code to record the total kinetic energy before a perfectly elastic collision and after the collision. If the number didn't remain the same then there had to be an error. Testing the features and set properties of the simulation were also done at different values of other properties to ensure things would work the same in different situations. However, since the simulation only suggests a range and does not limit the value inputs of properties for experimentation, inputs at extreme values can still push the simulation to it's limits and break things.

## Rating
95
