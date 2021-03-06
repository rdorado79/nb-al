import random
import sys

def distance(point1, point2, d):
  dist = 0
  for i in range(d):
    dist+=(point1[i]-point2[i])**2
  return dist


k = 2
points = [[1,1,0,0,0,1], [1,1,0,0,0,0], [1,0,0,0,1,1], [0,0,0,1,1,1], [1,1,1,0,0,0], [1,1,0,0,0,1], [0,0,0,0,1,1], [0,0,0,1,1,1]]
n = len(points)
d = 6

centroids = [points[int((n-1)*(float(x)/k))] for x in range(k)]
assignments = [int(random.random()*k) for x in range(n)]
distances = [0.0 for x in range(n)]
#pi = [random.random() for x in range(5)]

  
print assignments

changed = True
while changed:
  changed = False

  ## calculate new assignments based on centroids:
  for i in range(n):
    distances[i] = sys.maxint
    for j in range(k):
      dist = distance(points[i],centroids[j],d) 
      if distances[i] > dist:
        best=j
        distances[i] = dist        

    if assignments[i] != best:
      assignments[i] = best
      changed = True

  print assignments

  ## calculate new centroids
  temp = [[0 for x in range(d)] for x in range(k)]
  npoints = [0 for x in range(k)]
  for i in range(n):
    for j in range(d):
      temp[assignments[i]][j]+=points[i][j]
    npoints[assignments[i]]+=1
 
  for i in range(k):
    centroids[i]=[x/float(npoints[i]) for x in temp[i]]


print assignments
print centroids 
print distances
