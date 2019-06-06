import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

# Setup figure
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)

# Initialise data
t = np.arange(0.0, 1.0, 0.001)
a0 = 5
f0 = 3
delta_f = 5.0
s = a0 * np.sin(2 * np.pi * f0 * t)

# Plot object
l, = plt.plot(t, s, lw=2)
plt.axis([0, 1, -10, 10])

axcolor = 'lightgoldenrodyellow'
axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axamp  = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

# Create the sliders
sfreq = Slider(axfreq, 'Freq', 0.1, 30.0, valinit=f0, valstep=delta_f)
samp  = Slider(axamp, 'Amp', 0.1, 10.0, valinit=a0)


# This function recalculates the data
def update(val):
    amp = samp.val
    freq = sfreq.val
    l.set_ydata(amp*np.sin(2*np.pi*freq*t))
    fig.canvas.draw_idle()

# Link the sliders to the updater function
sfreq.on_changed(update)
samp.on_changed(update)

# Reset button
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button  = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

# Reset function
def reset(event):
    sfreq.reset()
    samp.reset()
button.on_clicked(reset)

# Buttons to change the color of the line
rax = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)
radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)

def colorfunc(label):
    l.set_color(label)
    fig.canvas.draw_idle()
radio.on_clicked(colorfunc)

plt.show()