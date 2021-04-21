import numpy as np
import math
import sys
import copy
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
plt.style.use('seaborn-whitegrid')


def getVect(vector):
    return vector / np.linalg.norm(vector)


class LineSegment:
    def __init__(self, referenceX, referenceY, length, angle):
        self.angle = angle
        self.length = length
        deltaX = math.cos(math.radians(angle)) * length
        deltaY = math.sin(math.radians(angle)) * length
        newX = referenceX + deltaX
        newY = referenceY + deltaY
        self.point = np.array([newX, newY])


class Fabrik:
    def __init__(self, baseX=0, baseY=0, marginOfError=0.01):
        self.basePoint = np.array([baseX, baseY])
        self.segments = []
        self.history = []
        self.armLength = 0
        self.marginOfError = marginOfError

    def addRaw(self, length, angle):
        if len(self.segments) > 0:
            segment = LineSegment(
                self.segments[-1].point[0], self.segments[-1].point[1], length, angle + self.segments[-1].angle)
        else:
            segment = LineSegment(
                self.basePoint[0], self.basePoint[1], length, angle)

        self.armLength += segment.length

        self.segments.append(segment)

    def isReachable(self, targetX, targetY):
        if np.linalg.norm(self.basePoint - np.array([targetX, targetY])) < self.armLength:
            return True
        return False

    def isInMarginOfError(self, targetX, targetY):
        if np.linalg.norm(self.segments[-1].point - np.array([targetX, targetY])) < self.marginOfError:
            return True
        return False

    def iterate(self, targetX, targetY):
        target = np.array([targetX, targetY])
        for i in range(len(self.segments) - 1, 0, -1):

            if i == len(self.segments) - 1:
                self.segments[i-1].point = (getVect(
                    self.segments[i-1].point - target) * self.segments[i].length) + target
            else:
                self.segments[i-1].point = (getVect(self.segments[i-1].point -
                                                    self.segments[i].point) * self.segments[i].length) + self.segments[i].point
        for i in range(len(self.segments)):
            if i == 0:
                self.segments[i].point = (getVect(
                    self.segments[i].point - self.basePoint) * self.segments[i].length) + self.basePoint

            elif i == len(self.segments) - 1:
                self.segments[i].point = (getVect(
                    self.segments[i-1].point - target) * self.segments[i].length * -1) + self.segments[i-1].point

            else:
                self.segments[i].point = (getVect(
                    self.segments[i].point - self.segments[i-1].point) * self.segments[i].length) + self.segments[i-1].point

    def reachTarget(self, targetX, targetY):
        self.history.append(copy.deepcopy(self.segments))
        if self.isReachable(targetX, targetY):
            while not self.isInMarginOfError(targetX, targetY):
                self.iterate(targetX, targetY)
                self.history.append(copy.deepcopy(self.segments))
        else:
            print('Target not reachable.')

    def getAngle(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        dX = x2 - x1
        dY = y2 - y1
        rads = math.atan2(-dY, dX)  
        return math.degrees(rads)

    def length(self, line):
        return ((line[0][0] - line[1][0])**2 + (line[0][1] - line[1][1])**2)**(0.5)

    def angleFromLines(self, lines):
        for line1 in lines:
            for line2 in lines:
                if line1 == line2:
                    continue
                line1StPnt, line1EndPnt = line1
                line2StPnt, line2EndPnt = line2
                angle1 = self.getAngle(line1StPnt, line1EndPnt)
                angle2 = self.getAngle(line2StPnt, line2EndPnt)
                angle = abs(angle1 - angle2)
                return angle

    def addWithLines(self, lastLine, currentLine):
        linkLength = self.length(currentLine)
        angle = self.angleFromLines([lastLine, currentLine])
        self.addRaw(linkLength, angle)

    def plotIterations(self):
        for i in range(len(self.history)):
            x = [0]
            y = [0]
            for segment in self.history[i]:
                x.append(segment.point[0])
                y.append(segment.point[1])

            plt.plot(x, y, label=("line " + str(i + 1)))
        plt.xlabel('x - axis')
        plt.ylabel('y - axis')
        plt.title('Iterations history')
        plt.legend()
        plt.show()
    def plot(self, segments=None, save=False, name="graph", xMin=-300, xMax=300, yMin=-300, yMax=300):
        if segments == None:
            segments = self.segments
        for i in range(len(segments)):
            plt.plot([segments[i].point[0]], [
                     segments[i].point[1]], 'ro')
            plt.text(segments[i].point[0], segments[i].point[1] + 1, '(x:{}, y:{})'.format(
                int(segments[i].point[0]), int(segments[i].point[1])))
        plt.plot([self.basePoint[0]], [self.basePoint[1]], 'bo')
        plt.text(self.basePoint[0], self.basePoint[1], 'Base')

        plt.axis([xMin, xMax, yMin, yMax])
        plt.grid(True)

        if save == True:
            plt.savefig('{}.png'.format(name))

        plt.show(block=True)


lines = []
totalLinks = int(input("Total links: "))
for i in range(totalLinks):
    text = input("Enter coord[" + str(i) + "]: ")
    coord = tuple(float(x) for x in text.split())
    lastCoord = (0, 0)
    if (len(lines) > 0):
        lastCoord = lines[-1][1]
    lines.append(((lastCoord, coord)))

arm = Fabrik()

for i in range(len(lines)):
    lastLine = ((-1, 0), (0, 0))
    if i != 0:
        lastLine = lines[i - 1]
    arm.addWithLines(lastLine, lines[i])

final_coord = tuple(float(x) for x in input(
    "Enter end effector final position: ").split())

arm.reachTarget(final_coord[0], final_coord[1])

print("total iterations: ", len(arm.history) - 1)

for segments in arm.history:
    text = ''
    for segment in segments:
        text += "[" + str(segment.point[0]) + ", " + \
            str(segment.point[1]) + "], "
    print(text[0:-2])

arm.plotIterations()
