import numpy as np
import math


def rotateX(theta, matrix):
  Rx = np.array([[1, 0, 0], [0, np.cos(theta), -np.sin(theta)],
                  [0, np.sin(theta), np.cos(theta)]])
  return matrix @ Rx


def rotateY(theta, matrix):
  Ry = np.array([[np.cos(theta), 0, np.sin(theta)], [
                0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
  return matrix @ Ry


def rotateZ(theta, matrix):
    Rz = np.array([[np.cos(theta),  -np.sin(theta), 0],
                   [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
    return matrix @ Rz


matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
cordinates = np.array(list(map(int, input("Enter cordinates: ").split())))

for i in range((3)):
    axis = input("Enter axis(x,y,z): ")
    angle = np.deg2rad(float(input("Enter Angle of rotation: ")))
    if axis == 'x':
        matrix = rotateX(angle, matrix)
    if axis == 'y':
        matrix = rotateY(angle, matrix)
    if axis == 'z':
        matrix = rotateZ(angle, matrix)

print("Final Cordinates: ",  matrix @ cordinates)
