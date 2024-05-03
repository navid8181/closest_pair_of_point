
# %% import file
import math
import random
from matplotlib import pyplot as plt

# points = [(0, 0), (1, 3), (2, 5), (3, 2), (4, 2), (5, -1), (6, 3), (7, 1)]
# points = [(0, 5), (0, 0), (1, 2), (1, -6), (2, 0), (3, 5), (5, 3)]
# points = [(0, 5), (0, 0), (0, 2), (0, -7), (0, -2), (0, -5), (0, 6)]
#points = [(0, 0), (1, 30), (2, 50), (3, 20), (4, 2), (5, -1), (6, 3), (7, 1)]




# %% import function


def generatePoint(size=200):
    generatePoint = []
    for i in range(size):
        x = random.random() * 10000
        y = random.random() * 10000
        generatePoint.insert(0,(x, y))
    return generatePoint


def getDistance(pointA=(0, 0), pointB=(0, 0)):
    xDistance = (pointA[0]-pointB[0])**2.0
    yDistance = (pointA[1]-pointB[1])**2.0
    return float(math.sqrt(xDistance + yDistance))


# %%show plot

points = generatePoint(1000)
x = (list(zip(*points))[0])
y = (list(zip(*points))[1])

plt.grid()
plt.plot(x, y, 'o')
plt.show()
# O(n^2) Time Complexity

def bruteForceApproach(points=[]):
    j = 0

    minDistance = 99999
    miniumPoints = [(), ()]
    for i in range(len(points)):
        j = i + 1
        while j < len(points):

            if (getDistance(points[i], points[j]) < minDistance):
                minDistance = getDistance(points[i], points[j])
                miniumPoints[0] = points[i]
                miniumPoints[1] = points[j]

            j += 1

    return miniumPoints


# divide and conquer Approach
# O(n*log(n)) Time Complexity
def FindMiniumPoints(points, start, end):

    if start >= end:
        return [start]

    mid = (start + end)//2

    leftPointsMinimum = FindMiniumPoints(points, start, mid)
    rightPointsMinimum = FindMiniumPoints(points, mid+1, end)

    if len(leftPointsMinimum) == 1 and len(rightPointsMinimum) == 1:
        return [leftPointsMinimum[0], rightPointsMinimum[0]]

    elif len(leftPointsMinimum) == 1 and len(rightPointsMinimum) == 2:
        pointL1 = points[leftPointsMinimum[0]]
        pointR1 = points[rightPointsMinimum[0]]
        pointR2 = points[rightPointsMinimum[1]]

        distanceR1toR2 = getDistance(pointR1, pointR2)
        distanceL1toR1 = getDistance(pointL1, pointR1)
        distanceL1toR2 = getDistance(pointL1, pointR2)

        minDistance = min(distanceL1toR1, distanceL1toR2, distanceR1toR2)

        if minDistance == distanceR1toR2:
            return [rightPointsMinimum[0], rightPointsMinimum[1]]

        if minDistance == distanceL1toR1:
            return [leftPointsMinimum[0], rightPointsMinimum[0]]

        if minDistance == distanceL1toR2:
            return [leftPointsMinimum[0], rightPointsMinimum[1]]

    elif len(leftPointsMinimum) == 2 and len(rightPointsMinimum) == 1:
        pointR1 = points[rightPointsMinimum[0]]
        pointL1 = points[leftPointsMinimum[0]]
        pointL2 = points[leftPointsMinimum[1]]

        distanceL1toL2 = getDistance(pointL1, pointL2)
        distanceR1toL1 = getDistance(pointR1, pointL1)
        distanceR1toL2 = getDistance(pointR1, pointL2)

        minDistance = min(distanceR1toL2, distanceR1toL1, distanceL1toL2)

        if minDistance == distanceL1toL2:
            return [leftPointsMinimum[0], leftPointsMinimum[1]]

        if minDistance == distanceR1toL1:
            return [leftPointsMinimum[0], rightPointsMinimum[0]]

        if minDistance == distanceR1toL2:
            return [leftPointsMinimum[1], rightPointsMinimum[0]]

    else:
        # pointR1 = points[rightPointsMinimum[0]]
        # pointR2 = points[rightPointsMinimum[1]]
        # pointL1 = points[leftPointsMinimum[0]]
        # pointL2 = points[leftPointsMinimum[1]]

        localPoints = [leftPointsMinimum[0], leftPointsMinimum[1],
                       rightPointsMinimum[0], rightPointsMinimum[1]]

        # find minimum between 4 points

        j = 0
        minDistance = 99999
        miniumPoints = [-1, -1]
        for i in range(len(localPoints)):
            j = i + 1

            while j < len(localPoints):
                if (getDistance(points[localPoints[i]], points[localPoints[j]]) < minDistance):
                    minDistance = getDistance(
                        points[localPoints[i]], points[localPoints[j]])
                    miniumPoints[0] = localPoints[i]
                    miniumPoints[1] = localPoints[j]

                j += 1

        # get minimum of middle points

        leftIndex = localPoints[1] + 1
        rightIndex = localPoints[2] - 1
        minimumMiddlePoints = [-1, -1]
        minDistance = 99999

        if leftIndex > rightIndex:
            return miniumPoints

        while leftIndex <= rightIndex:

            nextIndex = leftIndex + 1

            continuousDistance = getDistance(
                points[leftIndex], points[nextIndex])

            distanceMiddleToOuter1 = 0
            distanceMiddleToOuter2 = 0

            if leftIndex < mid:
                distanceMiddleToOuter1 = getDistance(
                    points[leftIndex], points[rightPointsMinimum[0]])

                distanceMiddleToOuter2 = getDistance(
                    points[leftIndex], points[rightPointsMinimum[1]])
            else:
                distanceMiddleToOuter1 = getDistance(
                    points[leftIndex], points[leftPointsMinimum[0]])

                distanceMiddleToOuter2 = getDistance(
                    points[leftIndex], points[leftPointsMinimum[1]])

            minimumMiddleDistance = min(
                distanceMiddleToOuter1, distanceMiddleToOuter2, continuousDistance)

            if minimumMiddleDistance == continuousDistance:
                if leftIndex == localPoints[1] + 1:
                    minimumMiddlePoints[0] = leftIndex
                    minimumMiddlePoints[1] = nextIndex
                else:
                    if getDistance(points[minimumMiddlePoints[0]], points[minimumMiddlePoints[1]]) > minimumMiddleDistance:
                        minimumMiddlePoints[0] = leftIndex
                        minimumMiddlePoints[1] = nextIndex

            elif minimumMiddleDistance == distanceMiddleToOuter1:
                if leftIndex < mid:
                    if leftIndex == localPoints[1]+1:
                        minimumMiddlePoints[0] = leftIndex
                        minimumMiddlePoints[1] = rightPointsMinimum[0]
                    else:
                        if getDistance(points[minimumMiddlePoints[0]], points[minimumMiddlePoints[1]]) > minimumMiddleDistance:

                            minimumMiddlePoints[0] = leftIndex
                            minimumMiddlePoints[1] = rightPointsMinimum[0]
                else:
                    if leftIndex == localPoints[1]+1:
                        minimumMiddlePoints[0] = leftIndex
                        minimumMiddlePoints[1] = leftPointsMinimum[0]
                    else:
                        if getDistance(points[minimumMiddlePoints[0]], points[minimumMiddlePoints[1]]) > minimumMiddleDistance:
                            minimumMiddlePoints[0] = leftIndex
                            minimumMiddlePoints[1] = leftPointsMinimum[0]

            elif minimumMiddleDistance == distanceMiddleToOuter2:
                if leftIndex < mid:
                    if leftIndex == localPoints[1]+1:
                        minimumMiddlePoints[0] = leftIndex
                        minimumMiddlePoints[1] = rightPointsMinimum[1]
                    else:
                        if getDistance(points[minimumMiddlePoints[0]], points[minimumMiddlePoints[1]]) > minimumMiddleDistance:
                            minimumMiddlePoints[0] = leftIndex
                            minimumMiddlePoints[1] = rightPointsMinimum[1]
                else:
                    if leftIndex == localPoints[1]+1:
                        minimumMiddlePoints[0] = leftIndex
                        minimumMiddlePoints[1] = leftPointsMinimum[1]
                    else:
                        if getDistance(points[minimumMiddlePoints[0]], points[minimumMiddlePoints[1]]) > minimumMiddleDistance:
                            minimumMiddlePoints[0] = leftIndex
                            minimumMiddlePoints[1] = leftPointsMinimum[1]

            leftIndex += 1

        dis1 = getDistance(points[minimumMiddlePoints[0]],
                           points[minimumMiddlePoints[1]])

        dis2 = getDistance(points[miniumPoints[0]],
                           points[miniumPoints[1]])

        if dis1 < dis2:
            return minimumMiddlePoints
        else:
            return miniumPoints


# %% test Code
out = bruteForceApproach(points)
print(out)
print(getDistance(out[0],out[1]))
# sort in O(n*log(n))
points.sort(key=lambda x: (x[0], x[1]))

indexes = FindMiniumPoints(points, 0, len(points)-1)
print([points[indexes[0]], points[indexes[1]]])
print(getDistance(points[indexes[0]], points[indexes[1]]))

# %%
