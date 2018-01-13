def cuboid_data(center, size):
	# suppose axis direction: x: to left; y: to inside; z: to upper
	# get the (left, outside, bottom) point
	o = [a - b / 2 for a, b in zip(center, size)]
	# get the length, width, and height
	l, w, h = size
	x = [[o[0], o[0] + l, o[0] + l, o[0], o[0]],  # x coordinate of points in bottom surface
	     [o[0], o[0] + l, o[0] + l, o[0], o[0]],  # x coordinate of points in upper surface
	     [o[0], o[0] + l, o[0] + l, o[0], o[0]],  # x coordinate of points in outside surface
	     [o[0], o[0] + l, o[0] + l, o[0], o[0]]]  # x coordinate of points in inside surface
	y = [[o[1], o[1], o[1] + w, o[1] + w, o[1]],  # y coordinate of points in bottom surface
	     [o[1], o[1], o[1] + w, o[1] + w, o[1]],  # y coordinate of points in upper surface
	     [o[1], o[1], o[1], o[1], o[1]],          # y coordinate of points in outside surface
	     [o[1] + w, o[1] + w, o[1] + w, o[1] + w, o[1] + w]]    # y coordinate of points in inside surface
	z = [[o[2], o[2], o[2], o[2], o[2]],                        # z coordinate of points in bottom surface
	     [o[2] + h, o[2] + h, o[2] + h, o[2] + h, o[2] + h],    # z coordinate of points in upper surface
	     [o[2], o[2], o[2] + h, o[2] + h, o[2]],                # z coordinate of points in outside surface
	     [o[2], o[2], o[2] + h, o[2] + h, o[2]]]                # z coordinate of points in inside surface
	return x, y, z



def test():
	import matplotlib as mpl
	from mpl_toolkits.mplot3d import Axes3D
	import numpy as np
	center = [0, 0, 0]
	length = 32 * 2
	width = 50 * 2
	height = 100 * 2
	import matplotlib.pyplot as plt
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	X, Y, Z = cuboid_data(center, (length, width, height))
	ax.plot_surface(X, Y, Z, color='b', rstride=1, cstride=1, alpha=0.1)
	ax.set_xlabel('X')
	ax.set_xlim(-100, 100)
	ax.set_ylabel('Y')
	ax.set_ylim(-100, 100)
	ax.set_zlabel('Z')
	ax.set_zlim(-100, 100)
	plt.show()


test()