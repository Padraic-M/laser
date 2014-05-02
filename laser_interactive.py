#!/usr/bin/env python

#    Copyright (C) Sam Berry 2014.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

prog_title = "HeNe Fabry-Perot Cavity"

# Switch for using Matplotlib or pylab default
use_mpl = True
try:
    # Import matplot lib
    import matplotlib as mpl
    
    if use_mpl:
        # Use Tkinter backend
        mpl.use('TkAgg')
        
        # Set the font used by matplotlib
        mpl.rc('font',**{'family':'serif', 'serif':['Times'], 'size':10,})
        mpl.rc('text', usetex=True)
        
        # Import Tkinter (TODO - module is renamed in Python3)
        import Tkinter as tk
        
        # Import the figure canvas backend
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    # If there was an error importing Matplot lib (Tkinter is installed by
    # default), print warning and set switch not to use matplotlib.
    print "Warning: Matplotlib not failed to import, check your modules."
    use_mpl = False

# Import PyLab
try:
    import pylab as pl
    import numpy as np
except ImportError:
    error("Pylab must be installed for these demos")

# Import Figure and Slider classes
from pylab import Figure
from pylab import Slider

#Physical constants
c = 3e8
hbar = 1.0546e-34

#Optical range
w1 = 400e12 # 400 THz -> 750 nm (Deep red)
w2 = 650e12 # 650 THz -> 462 nm (Deep blue)

# Laser cavity parameters
L = 30e-2
R = 0.9

# HeNe emission parameters
w_hene = c/632.8e-9
hene_width = 1e9

# Frequnecy scale
w_range = 4e9
resolution = 2**12
w = np.linspace(-w_range, w_range, resolution)

# HeNe emission lineshape function
A = np.sqrt(np.pi/hene_width)

F = A*np.exp(-(w/hene_width*2)**2)

# Fabry-Perot cavity modes
T = np.sqrt(1. - R**2)
D = T**4 + 4*R**2 * np.sin( 2*np.pi*(w+w_hene)/c * L)**2
I = T**4 /D

# Saturation radiation density
Ws = hbar * (w_hene)**3/np.pi**2/c**2

# Create the figure instance
if use_mpl:
    fig = Figure()
else:
    fig = pl.figure(prog_title)

# Create the axes for the main plot and plot the initial data
axes = fig.add_subplot(111)
fig.subplots_adjust(bottom=0.25)
plt, = axes.plot(c/(w+w_hene)*1e9,F*I* 1e6,'r')

# Declare the areas dedicated for the slider controls
axes_length = fig.add_axes([0.17, 0.12, 0.73, 0.03])
axes_reflect = fig.add_axes([0.17, 0.06, 0.73, 0.03])

# If using matplotlib, we must create the canvas area of the Window before
# creating the actual Sliders.
if use_mpl:
    # Create root Tk widget and set the title
    root = tk.Tk()
    root.title( prog_title )
    
    # Create and pack the renderable area of the widget, using the figure class
    plot_widget = FigureCanvasTkAgg(fig, master=root)
    plot_widget.show()
    plot_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    plot_widget._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create the sliders for the length and reflectivity parameters.
length = Slider(axes_length, 'Cavity length',0.01,1, valinit=L)
reflect = Slider(axes_reflect, 'Reflectivity',0.1,1, valinit=R)

# Create a callback function for the slider controls
def update(val):
    # Replot the graph using the new values
    R = reflect.val
    L = length.val
    T = np.sqrt(1. - R**2)
    D = T**4 + 4*R**2 * np.sin( 2*np.pi*(w+w_hene)/c * L)**2
    I = T**4 /D
    plt.set_ydata(F*I *1e6)
    
    # Render the result on the canvas
    fig.canvas.draw()
    
# Assign the callback function to the sliders
length.on_changed(update)
reflect.on_changed(update)

# Either show via PyLab or enter the Tk loop
if use_mpl:
    tk.mainloop()
else:
    pl.show()
