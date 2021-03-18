import math
import numpy as np 

a, b =  list(map(int, input("enter dimensions of DH matrix - ").strip().split()))
dh_marrix = np.zeros((a,b))

print("Enter DH matrix - ")
for i in range(a) :
  dh_marrix[i] = list(map(int, input().strip().split()))

#this function returns transformation matrix T_ij
def transform(i , j):
   theta_i = np.deg2rad(dh_marrix[i][3])
   link_length_j = dh_marrix[j][1]
   twist_j = np.deg2rad(dh_marrix[j][0])
   link_offset_i = dh_marrix[i][2]
   return np.array([[np.cos(theta_i), np.sin(theta_i), 0, link_length_j],
                    [np.cos(twist_j) * np.sin(theta_i), np.cos(twist_j) *
                     np.cos(theta_i), np.sin(twist_j), -link_offset_i * np.sin(twist_j)],
                    [np.sin(twist_j) * np.sin(theta_i), np.sin(twist_j) *
                     np.cos(theta_i), np.cos(twist_j), link_offset_i * np.cos(twist_j)],
                    [0, 0, 0, 1]])

matrix = np.identity((4));

for i in range(1, 7):
  matrix = matrix@(transform(i, i - 1))

point = np.array(list(map(int, input("enter point - ").strip().split())))

print(matrix@point)