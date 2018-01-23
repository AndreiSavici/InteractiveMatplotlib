'''
Default matplotlib interaction:
- move mouse over the plotting area. You can see
  the cursor position in the x and y coordinates
- while the mouse is over the figure, press keys
  'k' and 'l' to toggle the logarithmic x,y axes
'''
# This may be required if you are on a Mac and default to using OSX as
# your backend
# import matplotlib
# matplotlib.use('qt5agg')
from __future__ import print_function, absolute_import
import matplotlib.pyplot as plt
import numpy as np
plt.ion()

th = np.linspace(0, 2*np.pi, 64)
fig, ax = plt.subplots()
ax.plot(th, np.sin(th), 'o-')

