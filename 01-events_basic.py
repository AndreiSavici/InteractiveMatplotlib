'''
Exploring matplotlib events:
- pressing any mouse button will print information
  like which button was clicked, if it was a double
  click or not, the position in figure and data
  coordinates, or if any key is pressed at the same 
  time
'''
from __future__ import print_function, absolute_import
import matplotlib.pyplot as plt
import numpy as np
plt.ion()


def event_printer(event):
    """Helper function for exploring events.
    Prints all public attributes
    """
    for k, v in sorted(vars(event).items()):
        print('{}: {!r}'.format(k, v))
    print('-'*25)


th = np.linspace(0, 2*np.pi, 64)
fig, ax = plt.subplots()
# the `picker=5` kwarg turns on pick-events for this artist
# if clicked at a distance < 5 points from the artist
ax.plot(th, np.sin(th), 'o-', picker=5)

# - The callback registry is an attribute of FigureCanvasBase,
#   thus we need to fetch the canvas to create the connection
# - pick_event is one of the built-in event names
#   https://matplotlib.org/users/event_handling.html
# - cid : Connection ID, uniquely defines an event:callback pair
cid = fig.canvas.mpl_connect('button_press_event', event_printer)
#fig.canvas.mpl_disconnect(cid)

"""EXERCISE
Add additional connections to the canvas by connecting all 'active' events
to event_printer.
Active events: ['button_press_event', 'button_release_event', 'scroll_event',
                'key_press_event', 'key_release_event', 'pick_event']
"""


