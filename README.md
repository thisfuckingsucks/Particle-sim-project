# Particle Simulation

## Description
This a particle simulation you can play around with where you can edit the properties of particles.

## How to run
Just download all python files together and run 'simulation.py' to start the simulation.

## Usage

## Project design and implementation

### Provided code uses
The provided event driven simulation code was modified to a time driven simulation one due to the provided code sometimes not working correctly when implementing curved particle movement at the start of the project.
And the code for user interactivities were used as a reference for implementing features of the same manner in this project.
### Testing
After getting the simulation to not have any obvious errors, physics was used to ensure everything was working correctly, such as code to record the total kinetic energy before a perfectly elastic collision and after the collision. If the number didn't remain the same then there had to be an error. Testing the features and set properties of the simulation were also done at different values of other properties to ensure things would work the same in different situations. However, since the simulation only suggests a range and does not limit the value inputs of properties for experimentation, inputs at extreme values can still push the simulation to it's limits and break things.

## Rating
95
