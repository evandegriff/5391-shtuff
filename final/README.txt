Final Project NOTES:

Package dependencies:

argparse
spacepy
pickle
matplotlib
os
numpy
glob
scipy.signal
kneed

to get spacey:
$ sudo port install py38-spacepy

to get the kneed Python package, navigate to your python path and run the following code:
$ git clone https://github.com/arvkevi/kneed.git
$ sudo python setup.py install

note: kneed is a package that computes the "elbow point" of a curve, aka, the location at which the curve is optimized.

IMPORTANT NOTE: you cannot recreate the plots in my LaTex doc with the three mag files uploaded to git. you can make plots, but they will not be the same

To run the AE calculation for all magnetometers:
$ python calc_ae.py mag_files_debug/ ae_pkls/

To repeatedly run AE calculation for different magnetometer numbers 
(after specifying start, stop, and step vars in create_range_pkls.py file):
$ python create_range_pkls.py

To make all plots:
$ python plot_ae.py ae_pkls_debug_10_361_10/ ae_plots/
