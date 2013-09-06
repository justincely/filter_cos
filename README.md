filter_cos
==========

Filter out times of high airglow in COS timetag data.


Description
===========

Filter out data with SUN_ALT > 20, and re-combine the data back into x1dsum datasets.


Dependencies (Non standard library)
============
calcos
costools
astroraf

Also, this will only work internally to STScI unless you change the lref keyword to somewhere on your system.

