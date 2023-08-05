# -*- coding: utf-8 -*-
# written by Ralf Biehl at the Forschungszentrum Jülich ,
# Jülich Center for Neutron Science 1 and Institute of Complex Systems 1
#    Jscatter is a program to read, analyse and plot data
#    Copyright (C) 2015-2021  Ralf Biehl
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
#

"""
Fluid like and crystal like structure factors (sf) and directly related functions for scattering
related to interaction potentials between particles.

Fluid like include hard core SF or charged sphere sf and more.
For RMSA an improved algorithm is used based on the original idea (see Notes in RMSA).

For lattices of ordered mesoscopic materials (see :ref:`Lattice`) the analytic sf can be calculated in
powder average or as oriented lattice with domain rotation.

Additional the structure factor of atomic lattices can be calculated using atomic scattering length.
Using coordinates from CIF (Crystallographic Information Format) file allow calculation of atomic crystal lattices.


"""

from .fluid import *
from .ordered import *
from .lattices import *

