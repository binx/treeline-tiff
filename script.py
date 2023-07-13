import rasterio
from rasterio.plot import show, show_hist
from bresenham import bresenham
import matplotlib.pyplot as plt
import numpy as np



def findClearLineOfSight(e, trees):
    # to do: optimize this to stop finding points if we exceed elevation
    # instead of calling bresenham()

  for testIndex in range(len(trees)):
    tree1 = trees[testIndex]
    z1 = e[tree1[0], tree1[1]]

    for i in range(testIndex, len(trees)):
      if (i != testIndex):
        tree2 = trees[i]
        z2 = e[tree2[0], tree2[1]]

        # test x or y axis depending on which is greater
        axis = 0
        if (abs(tree2[1] - tree1[1]) > abs(tree2[0] - tree1[0])):
          axis = 1

        slope = (z2 - z1)/(tree2[axis] - tree1[axis])
        pixelsBetween = list(bresenham(tree1[0], tree1[1], tree2[0], tree2[1]))
        # try to throw out the more useless ones
        if (len(pixelsBetween) < 10):
          break

        clearLineOfSight = True
        for j in range(len(pixelsBetween)):
          zPixel = e[pixelsBetween[j][0], pixelsBetween[j][1]]
          zTreeline = slope*(pixelsBetween[j][axis] - tree1[axis]) + z1

          if (zPixel > zTreeline):
            clearLineOfSight = False
            break
        
        if (clearLineOfSight):
          print("clear line of sight for", tree1, tree2)
          fig, ax = plt.subplots()

          graphXAxis = map(lambda x: x[axis], pixelsBetween)

          heights = []
          for point in pixelsBetween:
            heights.append(e[point[0], point[1]])

          plt.title("line of sight for [" + ", ".join(str(e) for e in tree1) + "], [" + ", ".join(str(e) for e in tree2) + "]")
          ax.plot(list(graphXAxis), heights)
          # fig.savefig("test.png")
          plt.show()

def readTiff(clearance):
  with rasterio.open('./sample.tif') as src:
    e = src.read()[0]
    print(e.shape)
    rows = e.shape[1]
    cols = e.shape[0]

    trees = []

    points = []

    plt.pcolormesh(e)

    s = 2

    for x in range(2, cols - 2):
      for y in range(2, rows - 2):
        # surrounding = [e[x-1, y-1], e[x, y-1], e[x+1, y-1], e[x-1, y], e[x+1, y], e[x-1, y+1], e[x, y+1], e[x+1, y+1]]
        surrounding = [e[x, y-s], e[x-s, y], e[x+s, y], e[x, y+s]]

        # print(x, y, e[x,y], surrounding)
        if (all(i + clearance < e[x][y]  for i in surrounding)):
          trees.append([x,y])
          # reverse y and x for drawing geotiff lat/lng
          plt.plot(y, x, marker = 'o', color = "red", markersize = 1)

    plt.show()

    print("treeList", trees)
    # findClearLineOfSight(e, trees)

if __name__ == '__main__':
  # I have this clearance variable for how much higher the tree needs to be
  # than it's neighbors. Right now this is largely just fudging to get
  # enough data to test. Some points are very close to each other and
  # should possibly be thrown out?
  readTiff(clearance=5)
      