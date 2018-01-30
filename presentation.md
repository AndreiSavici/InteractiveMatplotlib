Interactive Matplotlib
======================

Parts of a figure
-----------------
![anatomy of matplotlib](https://matplotlib.org/_images/anatomy.png)

There are several components of a matplotlib image:

* **Figure** - the base container (think the page)
* **Axes** - a set of coordinates. You can have several axes per figure
* **Axis** - the spines, ticks, labels on an axis
* **Artist** - every object that can be rendered


User Interface events
---------------------

If you have used the pan / zoom tools or the 'g', 'l', 'k', etc keys in mpl, you have used the mpl event framework

* Events are available at the figure canvas level


|------------------------|----------------------------------------|
| Event name             | Description                            |
|------------------------|----------------------------------------|
| `button_press_event`   | mouse button is pressed                |
| `button_release_event` | mouse button is released		             |
| `draw_event`           | canvas draw (but before screen update) |
| `key_press_event`      | key is pressed			                      |
| `key_release_event`    | key is released			                     |
| `motion_notify_event`  | mouse motion				                       |
| `pick_event`           | an object in the canvas is selected	   |
| `resize_event`         | figure canvas is resized		             |
| `scroll_event`         | mouse scroll wheel is rolled		         |
| `figure_enter_event`   | mouse enters a new figure		            |
| `figure_leave_event`   | mouse leaves a figure			               |
| `axes_enter_event`     | mouse enters a new axes		              |
| `axes_leave_event`     | mouse leaves an axes                   |
|------------------------|----------------------------------------|



Processing events
-----------------

One needs to connect an event to a callback function

```python
 cid = canvas.mpl_connect(event_name, callback)
 #canvas.mpl_disconnect(cid)
```
