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
This module contains the scattering functions.

"""

from collections import defaultdict
import numbers
import multiprocessing as mp

import numpy as np
import numpy.linalg as la
from scipy import constants as co
from scipy.special import sph_harm as Ylm
from scipy.special import spherical_jn as Jl

from ..dataarray import dataArray as dA
from ..dataarray import dataList as dL
from . import mda
from .. import data
from .. import formel
# noinspection PyUnresolvedReferences
from .. import fscatter

__all__ = ['prepScatGroups', 'scatIntUniv', 'xscatIntUniv', 'nscatIntUniv', 'scatIntUnivYlm',
           'diffusionTRUnivTensor', 'diffusionTRUnivYlm',
           'intScatFuncYlm', 'intScatFuncPMode', 'intScatFuncOU']

pi = np.pi
identity3x3 = np.identity(3)
zero3x3 = np.zeros((3, 3))
QLIST = data.QLIST

#: H2O configuration
h2o = 0.1 * np.array([[0, 0, 0],  # oxygen
                      [0.95908, -0.02691, 0.03231],  # hydrogen
                      [-0.28004, -0.58767, 0.70556]])  # hydrogen

_ff = np.c_[QLIST, np.ones_like(QLIST)].T
_fan0_OHH = [data.Nscatlength['h'][0], data.Nscatlength['o'][0], data.Nscatlength['o'][0]]
_fanH2O = fscatter.cloud.scattering_debye(QLIST,
                                          h2o - h2o.mean(axis=0),  # positions
                                          _fan0_OHH,  # fan for atoms
                                          [1] * 3,  # all same constant formfactor row 1
                                          _ff,  # normalized formfactor
                                          1)  # ncpu parallel execution

_fanH2O[1] = (_fanH2O[1] / _fanH2O[1, 0]) ** 0.5

# using Levi-Civita symbols   antisymmetric  for cross product
eijk = np.zeros((3, 3, 3))
eijk[0, 1, 2] = eijk[1, 2, 0] = eijk[2, 0, 1] = 1
eijk[0, 2, 1] = eijk[2, 1, 0] = eijk[1, 0, 2] = -1


def coarseGraining(uni, position, ff, ffi2, nm=None, cubesize=1):
    """
    internal, output same as input

    Uses the return of prepScatGroups to do a coarse graining for speeding up some computations.

    The coordinates will be used on a cubic grid to average in respective cubes and use the grid as a coarse grained
    model of the input data.

    Using the geometric mean position instead of cube center improves the approximation for partial filled
    cubes at the border of a protein.

    formfactor amplitudes are approximated by root of Debye function which is valid only at small Q
    where position interferences in a single grain are negligible.
    Anyway a coarse graining is only useful in small Q SANS region.

    Because the formfactors ff reflect the contrast(q) the sign of the average contrast needs to be recovered
    which is lost in Debye equation .

    Parameters
    ----------
    cubesize : float cube size in units of position
    uni : universe
    position : Nx3 array of positions
    ff : formfactor amplitudes at positions
    ffi2 : incoherent scattering, q dependent
    nm : nxNx3 array as e.g. n normal mode displacements
         the average is done on the N dimension

    Returns
    -------
        averaged position, ff, ffi2, nm=None

    """
    if cubesize is None:
        return position, ff, ffi2, nm

    pos = position - np.min(position, axis=0)
    # fm = pos.max()/f
    # generate keys describing a cubic grid
    keys = np.floor(pos / cubesize).astype(int).astype('U5')
    keys = np.char.add(np.char.add(keys[:, 0], keys[:, 1]), keys[:, 2])
    # keys for occupied cubes
    ukeys = np.unique(keys)

    # some comments
    if len(ukeys) < 10:
        print('Less than 10 grains in coarse graining. Original values are used.')
        return position, ff, ffi2, nm
    elif len(ukeys) > 0.5 * position.shape[0]:
        print('More than 50% of original points. Coarse graining not useful.')

    # prepare return arrays
    npos = np.zeros([ukeys.shape[0], 3])
    nff = np.zeros([ukeys.shape[0], ff.shape[1]])
    nffi2 = np.zeros([ukeys.shape[0], ffi2.shape[1]])
    if nm is not None:
        nshape = list(nm.shape)
        nshape[-2] = ukeys.shape[0]
        nnm = np.zeros(nshape)
    else:
        nnm = nm
    # do averages for occupied cubes
    for i, key in enumerate(ukeys):
        select = (keys == key)
        # mean position => partial filled cubes get mean atom and not center cube
        npos[i] = position[select].mean(axis=0)
        # get scattering amplitude of atoms
        nffi = fscatter.cloud.mda_scattering_debye(uni.qlist, position[select] - npos[i], ff[select], ncpu=4)[1] ** 0.5
        # recover sign of contrast
        nff[i] = np.sign(ff[select][:, 0].sum()) * nffi
        # incoherent scattering
        nffi2[i] = ffi2[select].sum(axis=0)
    if nm is not None:
        # same for modes if present
        for i, key in enumerate(ukeys):
            nnm[..., i, :] = nm[..., select, :].mean(axis=-2)

    return npos, nff, nffi2, nnm


# noinspection PyIncorrectDocstring
def prepScatGroups(objekt, *args, **kwargs):
    """
    Prepare the objekt for calculations. Exchanged hydrogen, calc contrasts, volumes and position vectors.

    It is **NOT** necessary to call this function. It is called automatically in the module functions before each
    computation with respective parameters. It can be called for inspection directly.

    Parameters
    ----------
    objekt : atomgroup
    mode : 'n', 'x', 'nvac','xvac','nshape','xshape'
       Mode describing the type of scattering for neutron and xrays.
       - 'n','x' -> neutron or xray scattering embedded in a solvent resulting in contrast,
       - 'nshape','xshape' -> the shape filled with solvent (no surface layer)
       - 'nvac','xvac' -> scattering in vacuum without solvent

    solvent : string or list of string default ['1D2O1','0H2O1']
       Description of solvent as in  jscatter.formel.scatteringLengthDensityCalc
        A chemical formula with fraction+[lettercode+number]+.....
         - eg 'D2O1' or 'H2O1' for water and heavy water
         - ['0.6D2O1','0.4H2O1'] for a mixture of 0.6 hwater and 0.4 water
         - ['6D2O1','4H2O1']     for a mixture of 0.6 hwater and 0.4 water
         - default is h2o/d2o solvent according to setUnivProp
    solventDensity : float
        Density of the solvent, see scatteringUniverse.
    surfdensity : float, optional
       Surface layer density relative to bulk solvent if it is equal for all atoms on surface.
        - 1, None no change, no layer included
        - >< 1   lower or higher density
       The universe attribute surfdensity can be set for individual atoms/residues for specific settings
       as e.g. according to hydrophobicity or charge. See :py:func:`~jscatter.bio.scatteringUniverse` .
    refreshVolume : bool
        Refresh Volume calculation.
    point_density : int, default 5
        Point density on surface for SES and SAS calculation
        See getSurfaceVolumePoints

    Returns
    -------
        list of :[
            positions : positions relative to center of geometry, unit nm, shape Nx3
            formfactor : formfactor amplitudes, unit nm, shape Nxm, for q values in u.qlist
            I0 : forward scattering, unit nm²/particle
            inc : incoherent scattering squared, unit nm², q dependent, shape Nxm, for q values in u.qlist
            contrast : neutron scattering length density [1/nm²] or electron density [e/nm³]
            sld solvent : neutron sld [1/nm²]  or electron density [e/nm³]
            ]
        m : length qlist
        N : number of atoms or residues in objekt

    Notes
    -----
    **Surface layer density according to hydrophobicity**
    ::

     import jscatter as js
     import numpy as np

     uni=js.bio.scatteringUniverse('3pgk')
     for res in uni.residues:
         try:
             name = res.resname.lower()
             # 10% change scaled according to Kyte J, Doolittle RF. J Mol Biol. 1982 May 5;157(1):105-32.
             res.atoms.surfdensity =  1 + 0.1 * js.data.aaHydrophobicity[name][0]/4.5
         except:
             res.atoms.surfdensity = 1
     # calculate scattering
     S=js.bio.scatIntUniv(u,mode='x')


    """
    # our universe
    # TODO check if objekt is universe
    u = objekt.universe

    # get parameters and defaults
    u.solvent = kwargs.pop('solvent', u.solvent)
    u.solventDensity = kwargs.pop('solventDensity', u.solventDensity)
    point_density = kwargs.pop('point_density', 5)
    # mode for type of contrast
    mode = kwargs.pop('mode', 'n').lower()
    sd = kwargs.pop('surfdensity', None)
    if sd:
        u.atoms.surfdensity = sd
    refreshVolume = kwargs.pop('refreshVolume', True)
    output = kwargs.pop('output', True)
    suppressSurface = kwargs.pop('suppressSurface', False)

    # Volume occupied by a single water molecule with 55.51 mol/liter
    water_Vol = 1e8 ** 3 / (1000 / (data.Elements['h'][1] * 2 + data.Elements['o'][1]) * co.N_A)

    if objekt.n_atoms == objekt.n_residues:
        # is a Ca atom model
        u.iscalphamodel = True
        if refreshVolume or not hasattr(u, 'SESVolume'):
            # the task is to get the correct SESVolume for absolute scattering
            # -> see surfaceVolumePoints
            # get SASVolume and SESVolume of obj in u with surfdata atomAttribute
            mda.getSurfaceVolumePoints(objekt, point_density, u.probe_radius, '1',
                                       defaultdict(lambda: u.calphaCoarseGrainRadius), u.shellThickness)
    else:
        # default atomic behaviour with default vdWradii (None)
        u.iscalphamodel = False
        if refreshVolume or not hasattr(u, 'SESVolume'):
            mda.getSurfaceVolumePoints(objekt, point_density, u.probe_radius, '1', None, u.shellThickness)

    # factor between total displaced volume (SESVolume) and sum(vdW_Volume)
    # atom.vdW_Volume*Vfactor   distributes the excluded Volume scattering with
    # the final sum equal to the total volume of the protein
    u._Vfactor = u.SESVolume / np.sum(4 / 3 * pi * objekt.vdWradiinm ** 3)

    withSLayer = False
    # check if surfdensity !=1
    # surface atoms
    try:
        surfatoms = objekt.select_atoms('surface 1')  # surface atoms
    except AttributeError:
        # we have residue objekt
        surfatoms = objekt.atoms.select_atoms('surface 1').residues
    if np.any(surfatoms.surfdensity != 1) and not suppressSurface:
        withSLayer = True
    if output:
        if withSLayer:
            print(f'Use surface layer with {surfatoms.n_atoms} of total {objekt.atoms.n_atoms} atoms')
        else:
            print('No surface layer')

    mode = mode.lower()
    if mode[0] == 'x':
        # xray scattering contrast
        xsldensity = objekt.fax0().sum() / u.SESVolume
        edensity = xsldensity / data.felectron
        edensityExclSolvent = objekt.fax0dumy().sum() / u.SESVolume / data.felectron
        # rescale factor to have edensityExclSolvent==u.edensitySolvent
        edensityfactor = u.edensitySolvent / edensityExclSolvent
        edensityExclSolvent = objekt.fax0dumy().sum() / u.SESVolume / data.felectron * edensityfactor
        if mode == 'xshape':
            # xray excluded volume scattering
            formfactor = objekt.faxdumys * edensityfactor
            I0 = objekt.fax0dumy().sum() * edensityfactor
            ffinc2 = 0  # incoherent scattering
            surfdensity = 1
        elif mode == 'xvac':
            # xray in vacuum
            formfactor = objekt.faxs
            I0 = objekt.fax0().sum()
            ffinc2 = objekt.fi2xs
            surfdensity = surfatoms.surfdensity
        else:
            # mode == 'xray':
            # xray with contrast to solvent
            formfactor = objekt.faxs - objekt.faxdumys * edensityfactor
            I0 = (objekt.fax0() - objekt.fax0dumy() * edensityfactor).sum()
            ffinc2 = objekt.fi2xs
            surfdensity = (surfatoms.surfdensity - 1)
        if withSLayer:
            # add surface layer atoms with xray h2o formfactor
            h2ofax = data.getxrayFFatomicdummy('h2o').interp(u.qlist)
            shellVolume = surfatoms.surfdata[:, 2]
            faxs_surf = (shellVolume / water_Vol * surfdensity * h2ofax[:, None]).T
            # sum up fi2n over (solvent density deviation)
            fi2xs_surf = data.getxrayFFatomicdummy('h2o').interp(u.qlist, col=2) * (shellVolume * surfdensity)[:, None]
            formfactor = np.vstack([formfactor, faxs_surf])
            I0 = (I0 + (shellVolume / water_Vol * surfdensity).sum() * data.getxrayFFatomicdummy('h2o').Y[0]) ** 2
            ffinc2 = np.vstack([ffinc2, fi2xs_surf])
            # add position in surface
            positions = np.vstack([objekt.posnm, + surfatoms.surfdata[:, 3:6]])
        else:
            I0 = I0 ** 2
            # TODO check of posnm improves by using sld weight for coarse graining
            positions = objekt.posnm
        return positions - positions.mean(axis=0), formfactor, I0, ffinc2, edensity, edensityExclSolvent

    else:
        # neutron scattering contrast
        bv = u._Vfactor * 4 / 3 * pi * objekt.vdWradiinm ** 3 * u.bcDensitySol
        sld = objekt.fan0().sum() / u.SESVolume  # scattering length density
        sldDensityExclSolvent = bv.sum() / u.SESVolume
        fanH2O = np.interp(np.r_[u.qlist], _fanH2O[0], _fanH2O[1])
        if mode == 'nvac':
            # neutron coherent in vacuum
            formfactor = objekt.fans
            I0 = objekt.fan0().sum()
            ffinc2 = objekt.fi2ns
            surfdensity = surfatoms.surfdensity
        elif mode == 'test':
            print('we do a test with neutron formfactor equal 1')
            withSLayer = False
            formfactor = np.ones_like(objekt.fans)
            I0 = formfactor[:, 0].sum()
            ffinc2 = formfactor[:, 0]
        elif mode == 'nshape':
            withSLayer = False
            formfactor = fanH2O * bv[:, None]
            I0 = formfactor[:, 0].sum()
            ffinc2 = formfactor[:, 0]
        else:  # contrast
            # neutron with contrast to solvent
            formfactor = objekt.fans - fanH2O * bv[:, None]
            I0 = (objekt.fan0() - bv).sum()
            ffinc2 = objekt.fi2ns
            surfdensity = (surfatoms.surfdensity - 1)
        if withSLayer:
            # fan for each atom with 2*probeRadius = bcdensity*volume*2 * (solvent density deviation) * formfactor
            h2ofan = u.bcDensitySol * fanH2O
            shellVolume = surfatoms.surfdata[:, 2]
            fans_surf = (shellVolume * surfdensity * h2ofan[:, None]).T
            # sum up fi2n over (solvent density deviation)
            fi2ns_surf = u.b2_incSol * shellVolume * surfdensity
            formfactor = np.vstack([formfactor, fans_surf])
            I0 = (I0 + (shellVolume * surfdensity * u.bcDensitySol).sum()) ** 2
            ffinc2 = np.r_[ffinc2, fi2ns_surf]
            # add position in surface
            positions = np.vstack([objekt.posnm, + surfatoms.surfdata[:, 3:6]])
        else:
            I0 = I0 ** 2
            positions = objekt.posnm
        ffinc2 = np.ones_like(u.qlist) * ffinc2[:, None]

        return positions - positions.mean(axis=0), formfactor, I0, ffinc2, sld, sldDensityExclSolvent


# noinspection PyIncorrectDocstring
def scatIntUniv(objekt, qlist=None, **kwargs):
    r"""
    Neutron/Xray scattering of an atomgroup as protein/DNA with contrast to solvent.

    Explicit spherical average based on atomic positions or center of mass position of residues.
    Scattering amplitudes for grains are calculated if not precalculated as for residues.
    Scattering amplitudes of residues are averages of several hundreds of configurations with highest resolution.
    Needed parameters are taken from universe.

    Parameters
    ----------
    objekt : atom group in MDA universe
        Atomgroup for calculation as atomgroup or residuegroup.
    qlist : array
        Scattering vectors in unit 1/nm.
        If None or not given uni.qlist is used.
    mode : 'n', 'x', 'nvac','xvac','nshape','xshape'
       Mode describing the type of scattering for neutron and xrays.
        - 'n','x' -> neutron or xray scattering embedded in a solvent resulting in contrast,
        - 'nshape','xshape' -> the shape filled with solvent (no surface layer)
        - 'nvac','xvac' -> scattering in vacuum without solvent
    refreshVolume : boolean, default True
         - True   refresh protein volume each time of calculation e.g. always after configuration changes.
         - False  volume is only calculated once, even if configuration is changed eg by normal modes -> faster
    cubesize : float, default None
        Cube length (in units nm) for coarse graining, None means no coarse graining.
        For larger proteins the computation takes some time.
        Cubesize defines the size of a cubic grid in which atomic data as positions, formfactor and normal modes
        are averaged in cubes to realize a coarse graining and speedup the computation.
        The size should be adjusted to the protein size. This works for residue and atomic modes.
    output: True,False
        write more output or no output
    error : int
        - int Number of Fibonacci points in sphereAverage.
        - 0 Debye function is used

    Returns
    -------
    dataArray : columns   [q; P_coh; beta; P_inc]
         - P =<|F(Q)|²>  formfactor in unit nm²/particle
         - beta = |<F(Q)>|²/<|F(Q)|²> asymmetry factor according to Kotlarchyk [1]_ for structure factor correction.
         - P_inc = incoherent scattering for neutron scattering and xray scattering (Compton scattering)
           in unit nm²/particle.
        Result contains parameter of universe:
         - .RgPos    Rg calculated from positions as mean(R^2)
         - .I0       forward scattering q=0
         - .RgInt    Rg calculated from Intensity as
                     `Rg(q)=sqrt(-log(S.Y/S.S0)/S.X**2*3.)` and `Rgs[result.X<1/Rg[0]].mean()`
         - .RgInt_err   standard deviation from above
         - .surfdensityAverage  average surfdensity

    Notes
    -----
    We calculate in vacuum for an atomgroup or residuegroup the single particle formfactor

    .. math:: F(Q) = \Big \langle \sum_{j,k}b_j(Q)b_k(Q)e^{-Q(r_j-r_k)} \Big \rangle

    with the atomic/residue scattering amplitudes :math:`b_j(Q)`.
    In a solvent, according to Babinet's principle, we subtract the excluded volume scattering filled with dummy atoms
    (similar to CRYSON/CRYSOL [2]_)

    .. math:: b_j(Q) = b_{j,atom}(Q) - b_{j,dummy}(Q)

    The accumulated scattering of the dummy atoms corresponds to the excluded volume scattering of the displaced volume.
    For neutrons a formfactor amplitude is assumed which corresponds to water scattering
    while for xrays dummy formfactors according to water molecules are assumed [2]_.
    Different to CRYSON/CRYSOL we use explicit included hydrogen atoms.

    To account for the protein hydration layer [3]_ the **surface layer** is calculated (if surfacedensity≠1)
    by a rolling ball algorithm (Shrake & Rupley see getSurfaceVolumePoints)
    using 0.3 nm as thickness of the layer.

    A dummy atom is added for each surface atom in the center of the surface layer with respective atomic
    surface layer volume. The atomic attribute ``.surfacedensity`` determines respective additional scattering and
    allows surface density changes with atomic resolution.

    The direct calculation on atomic positions using an explicit spherical average has the advantage of being
    accurate even on larger Q. Limitations depend on the used water structure volume in the surrounding.
    The Method of CRYSON (spherical harmonics) is limited to smaller Q dependent on lmax and does not include
    positions of hydrogens.

    - Conversion to 1/cm see js.formfactor
    - CRYSON [2]_ output is in units cm^2/mol (not Crysol)

       `cm²/mol=f*nm²  ==> f= 1E-14 * 6.023*10^23=6.023*10^9`


    Examples
    --------
    **Influence of the hydration layer**

    The hydration layer density for proteins is reported to be 1% to 18% higher than bulk water density [3]_.
    E.g. for Ribonuclease A the density is 3.2% above bulk density [4]_.

    The surface layer contribution can make a large contribution to the absolute scattering.
    Because of the different contrast of the surface layer in SAXS and SANS the total scattering
    shifts in different direction. Also, the radius of gyration changes, which is different for SAXS and SANS.

    The changes can be used for determination of the surface layer density as explained in [3]_ by doing a combined fit
    of SAXS and SANS data. THe opposite effects can be demonstrated here :

    ::

     import jscatter as js
     import numpy as np

     uni = js.bio.scatteringUniverse('3rn3')
     protein = uni.select_atoms('protein')
     # set attributes
     uni.qlist=js.loglist(0.1,10,150)
     uni.solvent=['1D2O1','0H2O1']
     uni.solventDensity=1.11

     p=js.grace()
     p.title('Influence of the surface layer density')
     p.yaxis(scale='l',label=r'I(Q) / nm\S2\N/particle')
     p.xaxis(scale='l',label='Q / nm\S-1')
     for c, sld in enumerate(np.r_[1:1.16:0.04],1):
         uni.atoms.surfdensity = sld
         Sx = js.bio.xscatIntUniv(protein)
         Sn = js.bio.nscatIntUniv(protein)
         p.plot(Sx,sy=0,li=[1,2,c],le=f'surfdensity={sld:.2f} R\\sgn\\N={Sn.RgInt:.2f} R\\sgx\\N={Sx.RgInt:.2f}')
         p.plot(Sn,sy=0,li=[3,2,c] )

     p.legend(x=0.12,y=5e-7)
     p.subtitle('Ribonuclease A with surface layer')
     p.text('neutron',x=0.2,y=5e-6)
     p.text('X-ray',x=1,y=4e-5)
     #p.save(js.examples.imagepath+'/hydrationlayerdensity.jpg')

    .. image:: ../../examples/images/hydrationlayerdensity.jpg
     :align: center
     :width: 50 %
     :alt: hydrationlayerdensity




    **Accuracy test spherical average**.

    Change number of points on Fibonacci lattice for spherical average.
    For larger proteins Debye gets much slower (order N²), here factor 2 for error=100.
    ::

     import jscatter as js

     uni = js.bio.scatteringUniverse('3RN3')
     # set attributes
     uni.qlist=js.loglist(0.1,10,340)
     uni.solvent=['1D2O1','0H2O1']
     uni.solventDensity=1.11
     u = uni.select_atoms("protein")

     p=js.grace()
     p.title('Spherical average accuracy')
     for ii in [300,200,100,50]:
         uni.error=ii
         S=js.bio.scatIntUniv(u,mode='xray')
         p.plot(S,sy=[-1,0.1,-1],le='error=%.3g' %(ii))
     uni.error=0
     S=js.bio.scatIntUniv(u,mode='xray')
     p.plot(S,sy=[-1,0.1,-1],le='Debye -> exact spherical average')

     p.yaxis(scale='l',label=r'I(Q) / nm\S2\N/particle',min =5e-8,max=5e-5)
     p.xaxis(scale='l',label='Q / nm\S-1')
     p.legend(x=0.15,y=1e-6)
     #p.save(js.examples.imagepath+'/accuracytestsphericalaverage.jpg')

    .. image:: ../../examples/images/accuracytestsphericalaverage.jpg
     :align: center
     :width: 50 %
     :alt: accuracytestsphericalaverage



    References
    ----------
    .. [1] M. Kotlarchyk and S.-H. Chen, J. Chem. Phys. 79, 2461 (1983).
    .. [2] CRYSOL– a Program to Evaluate X-ray Solution Scattering of Biological Macromolecules
           D. Svergun, C. Barberato and M. H. J. Koch
           J. Appl. Cryst. (1995). 28, 768–773
    .. [3] Protein hydration in solution: Experimental observation by x-ray and neutron scattering
           D. I. SVERGUN, S. RICHARD, M.H.J.KOCH, Z. SAYERS, S. KUPRIN, AND G. ZACCAI
           Proc. Natl. Acad. Sci. USA Vol. 95, pp. 2267–2272
    .. [4] Structure and Dynamics of Ribonuclease A during Thermal Unfolding: The Failure of the Zimm Model
           J. Fischer, A. Radulescu, P. Falus, D. Richter, R. Biehl
           The Journal of Physical Chemistry B  2021, 125, 3, 780-788, DOI: 10.1021/acs.jpcb.0c09476

    """
    # our universe
    u = objekt.universe

    mode = kwargs.pop('mode', 'n')
    ncpu = kwargs.pop('ncpu', 0 if mp.current_process().name == 'MainProcess' else 1)
    output = kwargs.pop('output', True)
    surfdensity = kwargs.pop('surfdensity', None)
    refreshVolume = kwargs.pop('refreshVolume', True)
    u.qlist = u.qlist if qlist is None else qlist
    u.error = kwargs.pop('error', u.error)
    cubesize = kwargs.pop('cubesize', None)

    if output:
        print('mode is ', mode)
    positions, formfactors, I0, ffinc2, sld, sldExclSolvent = \
        prepScatGroups(objekt, mode=mode, surfdensity=surfdensity, refreshVolume=refreshVolume, output=output, **kwargs)

    if cubesize is not None:
        # do a coarse graining to reduce computing time
        # average positions and formfactors according to cube grid
        positions, formfactors, ffinc2, _ = \
            coarseGraining(u, positions, formfactors, ffinc2, cubesize=cubesize)

    if output:
        print('unit is nm^2/particle')
        cubetxt = f'in {formfactors.shape[0]:.0f} cubes ' if cubesize is not None else ''
        if u.iscalphamodel:
            print(f'start integrating with {len(objekt):.0f} residues ' + cubetxt)
        else:

            print(f'start integrating with {len(objekt):.0f} atoms ' + cubetxt)
        print('')

    if u.error == 0 or u.error == 'debye':
        # for N>1000 slower than spherical average
        Slist = fscatter.cloud.mda_scattering_debye(u.qlist, positions, formfactors, ncpu=ncpu)
        columnname = 'q; P_coh; P_inc'
    else:
        assert isinstance(u.error, int)
        # call Fortran with parallel do loop and shared memory
        # this returns a list of [q,P(q)=F**2, F(q)]
        Slist = fscatter.cloud.mda_parallel_cohscaint(u.qlist, positions, formfactors, u.error, ncpu=ncpu)
        Slist = Slist.T
        # the third row is F(Q) but will be parameter beta according to Chen
        # which is beta=|<F(Q)>|²/<|F(Q)|²>   and scattering amplitude F(Q) and P(Q)=<|F(Q)|²>
        Slist[2] = (Slist[2] ** 2) / Slist[1]
        columnname = 'q; P_coh; beta; P_inc'

    result = dA(Slist, dtype=float)
    # add incoherent
    result = result.addColumn(1, ffinc2.sum(axis=0))
    result.columnname = columnname
    result.setColumnIndex(iey=None)
    mda.copyUnivProp(u, result)
    result.mode = mode
    result.I0 = I0
    result.sld = sld
    result.sldExclSolvent = sldExclSolvent
    result.contrast = sld - sldExclSolvent
    # positional Rg
    com = objekt.center_of_geometry() / 10  # in nm
    result.RgPos = (la.norm(objekt.posnm - com, axis=1) ** 2).mean() ** 0.5
    # some aminoacids have increasing Y because of contrast
    # the sign makes a proper Rg
    no = result.X > 0  # avoid zero
    Rgs = np.sqrt(-np.log((result.Y[no] / I0) ** np.sign(1 - result.Y[no] / I0)) / result.X[no] ** 2 * 3.)
    result.RgInt = Rgs[result.X[no] < 1 / result.RgPos].mean()  # mean only for R < Rg in Guinier range
    result.RgInt_err = Rgs[result.X[no] < 1 / result.RgPos].std()
    result.surfdensityAverage = objekt.atoms.surfdensity.mean()
    result.mass = objekt.total_mass()
    result.massdensity = result.mass / co.N_A / (result.SESVolume / 1e7 ** 3)

    return result


def xscatIntUniv(objekt, qlist=None, **kwargs):
    """
    Xray scattering intensity with contrast to solvent.

    See See :py:func:`scatIntUniv` with mode='x' for details.

    """
    kwargs.update(mode='x')
    return scatIntUniv(objekt, qlist=qlist, **kwargs)


def nscatIntUniv(objekt, qlist=None, **kwargs):
    """
    Neutron scattering intensity with contrast to solvent.

    See :py:func:`scatIntUniv` with mode='n' for details.

    """
    kwargs.update(mode='neutron')
    return scatIntUniv(objekt, qlist=qlist, **kwargs)


def _getjfylm(u, r, p, t, lmax=15):
    jl_q = []
    for iq, q in enumerate(u.qlist):
        # jl_q.append(transpose(map(lambda ra:np.array(Jl(lmax,ra*qlist[q])[0],float), r)))
        jl_q.append(np.r_[[Jl(range(lmax + 1), ra * q) for ra in r]].T)
    ylm = []
    for l in range(0, lmax + 1):
        ylm.append([])
        for m in range(0, 2 * l + 1):  # m-l ist die liste m= -l,.0...,l
            # ylm[l].append(map(lambda p,t:Ylm(m-l,l,p,t).conj(), np.array(p),np.array(t)) )
            ylm[l].append(np.r_[[Ylm(m - l, l, pp, tt).conj() for pp, tt in zip(p, t)]])
    return jl_q, ylm


def scatIntUnivYlm(objekt, qlist=None, lmax=15, **kwargs):
    r"""
    Neutron/Xray scattering intensity based on the Rayleigh expansion (Ylm).

    Similar to CRYSOL/CRYSON (see [1]_) except that we use here resolution of the atomgroup (atomic or residue).
    Surface layer if desired. See scatIntUniv for additional parameters and details.

    Parameters
    ----------
    objekt : MDAnalysis universe
        Atomgroup or universe.
    qlist : array
        Scattering vectors in unit 1/nm.
        If None or not given uni.qlist is used.
    lmax : int 15
        Maximum order of spherical bessel function.
        For larger Q this needs to be increased. See CRYSON for a estimate what is needed.
    output : 'partialAmplitudes', default 'normal'
        Coefficients of partial waves appended as result.partialAmplitude_lm
    mode : 'n', 'x', 'nvac','xvac','nshape','xshape'
       Mode describing the type of scattering for neutron and xrays.
        - 'n','x' -> neutron or xray scattering embedded in a solvent resulting in contrast,
        - 'nshape','xshape' -> the shape filled with solvent (no surface layer)
        - 'nvac','xvac' -> scattering in vacuum without solvent
    cubesize : float, default None
        Cube length (in units nm) for coarse graining, None means no coarse graining.
        For larger proteins the computation takes some time.
        Cubesize defines the size of a cubic grid in which atomic data as positions, formfactor and normal modes
        are averaged to realize a coarse graining and speedup the computation.
        The size should be adjusted to the protein size. This works for residue and atomic modes.

    Returns
    -------
    dataArray  [q, Fq]    unit is nm^2/particle

    Notes
    -----
    An extensive description can be found in [1]_.
    The scattering intensity is

    .. math:: I(Q) = \langle | A_a(Q) -\rho_0A_c(Q) +\delta\rho  A_b(Q) |^2 \rangle_\Omega

    with :math:`A_a(Q)` as particle scattering amplitude, :math:`A_c(Q)` scattering amplitude of excluded solvent
    and :math:`A_b(Q)` of the border hydration layer with densities  :math:`\rho` and excess hydration layer density
    :math:`\delta \rho` . Brackets indicate orientational averaging over orientational angle :math:`\Omega`.

    The scattering amplitudes for atoms j with atomic scattering amplitude :math:`f_j(Q)` can be expressed as

    .. math:: A(Q) = \sum_{j=1}^N f_j(Q)exp(iQR_j)

    and after multipole expansion

    .. math:: A(Q) = \sum_{l=0}^{\infty}\sum_{m=-l}^{l} A_{lm}(Q)Y_{lm}(\Omega)

    .. math:: A_{lm}(Q) = 4\pi i^l \sum_{j=1}^N f_j(Q)j_l(Qr_j)Y_{lm}^{*}(\Omega_j)

    with spherical Bessel function :math:`j_l(Qr_j)` and spherical harmonics :math:`Y_{lm}(\Omega_j)` .
    Coordinates are spherical coordinates :math:`r_j = (r_j,\theta_j,\phi_j) = (r_j, \Omega_j)` .

    The border hydration layer is here (different from (CRYSOL/CRYSON) depicted by dummy atoms
    placed at the center of the layer representing the layer volume.
    The dummy atoms of the excluded volume inside of the protein represent the excluded solvent at same positions
    as the real atoms. Inside and hydration layer dummy atoms have scattering amplitudes as described
    in [1]_ (equ 12 + 13) using atomic van der Waals volume scaled to equal the SES volume or layer volume.


    Examples
    --------
    ::

     import jscatter as js
     import numpy as np
     uni=js.bio.scatteringUniverse('3pgk')
     uni.qlist=np.r_[0.01,0.1:2:0.2]
     Sq = js.bio.scatIntUnivYlm(uni.residues)

    References
    ----------
    .. [1] Svergun   J.Appl.Cryst 28,768-773 (1995)

    """
    u = objekt.universe
    if isinstance(objekt, mda.scatteringUniverse):
        objekt = u.atoms
    mode = kwargs.pop('mode', 'n')
    ncpu = kwargs.pop('ncpu', 0 if mp.current_process().name == 'MainProcess' else 1)
    output = kwargs.pop('output', True)
    surfdensity = kwargs.pop('surfdensity', None)
    refreshVolume = kwargs.pop('refreshVolume', True)
    u.qlist = u.qlist if qlist is None else qlist
    u.error = kwargs.pop('error', u.error)
    cubesize = kwargs.pop('cubesize', None)

    positions, formfactors, I0, ffinc2, sld, sldExclSolvent = \
        prepScatGroups(objekt, mode=mode, surfdensity=surfdensity, refreshVolume=refreshVolume, output=output, **kwargs)

    if cubesize is not None:
        # do a coarse graining to reduce computing time
        # average positions and formfactors according to cube grid
        positions, formfactors, ffinc2, _ = \
            coarseGraining(u, positions, formfactors, ffinc2, cubesize=cubesize)

    # prepare single 1dim arrays from all universe objects in single 1dim arrays  -> faster
    # spherical coordinates
    r, p, t = formel.xyz2rphitheta(positions).T
    # partial amplitudes
    jl_q, ylm = _getjfylm(u, r, p, t, lmax)

    rI = []
    partialAmplitude_lm = []
    for iq, q in enumerate(u.qlist):
        b = formfactors[:, iq]
        I = 0.
        partialAmplitude_lm.append([])
        for l in range(0, lmax + 1):
            Sll = 0
            for m in range(0, 2 * l + 1):  # m-l ist die liste m= -l,.0...,l
                Amp = np.add.reduce(b * ylm[l][m] * jl_q[iq][l])
                I = I + 4. * pi * abs(1.j ** l * Amp) ** 2
                Sll += abs(1.j ** l * Amp) ** 2
            partialAmplitude_lm[-1].append(Sll)
        rI.append(I)

    result = dA(np.array([u.qlist, rI]))
    if isinstance(output, str) and output.startswith('par'):
        result.partialAmplitude_lm = np.r_[partialAmplitude_lm]
        result.partialAmplitude_lm_q = u.qlist

    mda.copyUnivProp(u, result)
    result.columnname = 'q; Fq'
    result.lmax = lmax
    result.setColumnIndex(iey=None)
    return result


def diffusionTRUnivTensor(objekt,
                          DTT=None,
                          DRR=None,
                          DTR=None,
                          DRT=None,
                          Dtrans=0., **kwargs):
    r"""
    Effective diffusion from 6x6 diffusion tensor.

    Calculate the effective diffusion of a rigid protein with 6x6 diffusion matrix D
    as measured in the initial slope of Neutron Spinecho Spectroscopy, Backscattering or TOF.
    Needed parameters as temperature or viscosity are taken from universe.

    Parameters
    ----------
    objekt : universe or atomgroup
        Atomgroup in a solvent.
    DTT : float, 3x3 array,
        3x3 matrices of translation diffusion tensor in nm^2/ps.
        If float  DTT = 𝟙 * value
    DRR : float, 3x3 array
        3x3 matrices of rotation diffusion tensor in    1/ps.
        If float  DRR = 𝟙 * value
    DRT : 3x3 array
        3x3 matrices r-t coupling in nm/ps.
    DTR : 3x3 array
        3x3 matrices t-r coupling    in nm/ps.
    Dtrans : float, default =0
        Translational diffusion in nm²/ps.
         - If *float* DTT and DRR are calculated based on Dtrans:
          - DTT= identity3x3*Dtrans    ( trace=Dtrans)
          - DRR= identity3x3*Drot       for same hydrodynamic radius as Dtrans
          - DRT=DTR=0
         - If Dtrans<0 the hydrodynamic radius (in nm) is calculated as a equivalent sphere
           with :math:`R_h=(\frac{3V_{SES}}{4\pi})^{1/3} + 0.3` as a rough estimate.
           In general the shape anisotropy needs to be accounted using :py:func:`~.libs.HullRad.hullRad`.
    cubesize : float, default None
        Cube length (in units nm) for coarse graining, None means no coarse graining.
        For larger proteins the computation takes some time.
        Cubesize defines the size of a cubic grid in which atomic data as positions, formfactor and normal modes
        are averaged to realize a coarse graining and speedup the computation.
        The size should be adjusted to the protein size. This works for residue and atomic modes.

    Returns
    -------
    dataArray with columns
        [q, D_coh, S_coh ,D_incoh, S_incoh, D_pol I_pol, D_int I_int, ...errors for each in same order ]
         - .DTTtrace is trace/3 = Dtrans
         - .DRRtrace is trace/3 = Drot
         - _pol is NSE measurement with polarised beam for larger Q where a coh/inc mixture is observed.
         - _int is unpolarised beam as for conventional BS or TOF.

    Notes
    -----
    The effective diffusion D0 of a rigid protein/DNA in a dilute limit is a combination
    of translational and rotational diffusion including coupling between both for non isotropic objects [1]_:

    .. math:: D_0(Q) = \frac{1}{Q^2F(Q)} \sum_{j,k}
                        \langle b_je^{-iQr_j} \begin{pmatrix} Q \\ r_j \times Q \end{pmatrix} D_{6x6}
                        \begin{pmatrix} Q \\ r_j \times Q \end{pmatrix}  b_ke^{-iQr_k}
                        \rangle

    with :math:`F(Q)=<\sum_{j,k}b_jb_ke^{-Q(r_j-r_k)}>` and
    :math:`D_{6x6} = \begin{pmatrix} D_{TT} D_{TR}  \\ D_{TR} D_{RR} \end{pmatrix}`

    For incoherent scattering the summation in D(Q) and F(Q) is only over indices :math:`j=k` with
    incoherent scattering length :math:`b_{i,inc}`

    DTT is the 3x3 translational diffusion matrix with :math:`D_{0,trans} = trace(D^{3x3}_{TT})/3`

    DRR is the 3x3 rotational diffusion matrix with :math:`D_{0,rot} = trace(D^{3x3}_{RR})/3`


    **Mixture of coherent and incoherent**:

    At low Q in the SANS regime it is assumed that the incoherent is negligible and D_coh,D_incoh can be used
    dependent on the used instrument.

    For larger Q we have:

    - Polarisation analysis (e.g. NSE = Neutron Spinecho Spectroscopy) with incoherent spin flip in cases where
      mixtures of coherent and incoherent are observed as for larger Q.

      .. math:: D_{pol}(Q)=\frac{D_{coh}(Q) F_{coh}(Q) - 1/3 D_{inc}(Q)F_{inc}(Q)} {F_{coh}(Q) - 1/3 F_{inc}(Q)}

    - Intensity is measured (eg backscattering or TOF) no polarisation

      .. math:: D_{int}(Q) = \frac{D_{coh}(Q) F_{coh}(Q) + D_{inc}(Q)F_{inc}(Q)} {F_{coh}(Q) +F_{inc}(Q)}

    Units :
     - S same as cohScatUniv =  nm^2/particle
     - q in nm^-1, time in ps
        - DTT in nm^2/ps
        - DRT,DTR in   nm/ps
        - DRR in 1/ps

    Examples
    --------
    ::

     import jscatter as js
     import numpy as np

     adh = js.bio.fetch_pdb('4w6z.pdb1')
     # the 2 dimers in are in model 1 and 2 and need to be merged into one.
     adhmerged = js.bio.mergePDBModel(adh)

     p = js.grace()
     for pdb in ['3rn3','3pgk', adhmerged]:
         uni = js.bio.scatteringUniverse(pdb, vdwradii={'M': 1.73,'Z':1.7},addHydrogen='pdb2pqr')
         uni.qlist=np.r_[0.01,0.1:3:0.03]
         D_hr = js.bio.hullRad(uni)
         Dt = D_hr['Dt'] * 1e2
         Dr = D_hr['Dr'] * 1e-12
         Dq = js.bio.diffusionTRUnivTensor(uni.residues, DTT=Dt, DRR=Dr)
         p.plot(Dq.X,Dq.Y/Dq.DTTtrace, le=pdb)
     p.xaxis(label='Q / nm\S-1', min=0, max=3)
     p.yaxis(label='D(Q)/D(0)',min=0.98,max=1.4)
     p.legend(x=1.5,y=1.35)
     #p.save(js.examples.imagepath+'/bioeffDiffusion.jpg', size=(700, 700))

    .. image:: ../../examples/images/bioeffDiffusion.jpg
     :align: center
     :width: 50 %
     :alt: bioeffDiffusion


    References
    ----------
    .. [1] Exploring internal protein dynamics by neutron spin echo spectroscopy
           R. Biehl, M. Monkenbusch and D. Richter
           Soft Matter, 2011, 7, 1299–1307; DOI: 10.1039/c0sm00683a

    """
    assert isinstance(Dtrans, numbers.Real), f'Dtrans should be real number but is {type(Dtrans)}.'

    u = objekt.universe
    if isinstance(objekt, mda.scatteringUniverse):
        objekt = u.atoms

    mode = kwargs.pop('mode', 'n')
    ncpu = kwargs.pop('ncpu', 0 if mp.current_process().name == 'MainProcess' else 1)
    output = kwargs.pop('output', True)
    surfdensity = kwargs.pop('surfdensity', None)
    refreshVolume = kwargs.pop('refreshVolume', True)
    u.qlist = kwargs.pop('qlist', u.qlist)
    u.error = kwargs.pop('error', u.error)
    cubesize = kwargs.pop('cubesize', None)

    if isinstance(DTT, dict) and 'DTT' in DTT:
        DRR = DTT['DRR']
        DTR = DTT['DTR']
        DRT = DTT['DRT']
        DTT = DTT['DTT']
    if isinstance(DTT, numbers.Real):
        DTT = identity3x3 * DTT
    if isinstance(DRR, numbers.Real):
        DRR = identity3x3 * DRR
    if DTR is None:
        DTR = zero3x3
    if DRT is None:
        DRT = DTR.T

    positions, formfactors, I0, ffinc2, sld, sldExclSolvent = \
        prepScatGroups(objekt, mode=mode, surfdensity=surfdensity, refreshVolume=refreshVolume, output=output, **kwargs)

    if cubesize is not None:
        # do a coarse graining to reduce computing time
        # average positions and formfactors according to cube grid
        positions, formfactors, ffinc2, _ = \
            coarseGraining(u, positions, formfactors, ffinc2, cubesize=cubesize)

    # calc viscosity of water in Pa*s = kg/m/s
    visc = (formel.viscosity(mat='d2o', T=u.temperature) * u.d2oFract +
            formel.viscosity(mat='h2o', T=u.temperature) * (1 - u.d2oFract))

    # Diffusion coefficients in nm^2/ps = 1e5 A^2/ns
    # calculate diagonal matrix if Dtrans and Drot >0
    if Dtrans != 0. or DTT is None:
        if Dtrans <= 0:
            # sphere with same Volume unit nm
            Rhydro = (3. * u.SESVolume / 4 / pi) ** (1. / 3.) + 0.3
        else:
            # in nm, ps units
            Rhydro = co.k * u.temperature / (6. * pi * visc * 1e-18 * Dtrans * 1e3)
        DTeff = co.k * u.temperature / (6. * pi * visc * 1e-18 * Rhydro) * 1e-3
        DTT = identity3x3 * DTeff
        DReff = co.k * u.temperature / (8. * pi * visc * 1e-18 * Rhydro ** 3) / 1e3
        DRR = identity3x3 * DReff
    # recalc Rhydro
    Rhydro = co.k * u.temperature / (6. * pi * visc * 1e-18 * np.trace(DTT) / 3 * 1e3)

    if output: print("start integrating")
    columnname = 'q; D_eff; S; Dinc_eff; Sinc; D_eff_spin; S_spin; D_eff_int; S_int'
    if output: print(columnname)
    results = []
    D66 = np.vstack([np.hstack([DTT, DTR]), np.hstack([DRT, DRR])])
    for iq, q in enumerate(u.qlist):
        bc = formfactors[:, iq]
        binc2 = ffinc2[:, iq]
        # integrate over sphere
        res = formel.sphereAverage(_deffDiffusionTensor, u.error / 5,
                                   r=positions, bc=bc, b2inc=binc2, q=q, D66=D66)

        # calc D(q)= DqqSq/S/q**2
        # spin flip mixing from polarisation analysis NSE
        res[5] = (res[1] - 1 / 3. * res[3])
        res[4] = (res[0] - 1 / 3. * res[2]) / res[5] / q ** 2
        # intensity added without polarisation analysis TOF or backscattering
        res[7] = (res[1] + res[3])
        res[6] = (res[0] + res[2]) / res[7] / q ** 2
        # separate coh inc, low Q approximation
        res[0] = res[0] / res[1] / q ** 2
        res[2] = res[2] / res[3] / q ** 2
        results.append(np.r_[q, res])
        if output:
            with np.printoptions(precision=2, threshold=7):
                print(f'{q:.3f}', res.real[:6], '...')
    result = dA(np.array(results).T, dtype=float)
    mda.copyUnivProp(u, result)
    result.columnname = columnname
    result.setColumnIndex(iey=None)
    result.DTTtrace = np.trace(DTT) / 3
    result.DRRtrace = np.trace(DRR) / 3
    result.Rh = Rhydro
    return result


def _deffDiffusionTensor(point, r, bc, b2inc, q, D66):
    """
    effective diffusion for direction point on sphere with length q

    for objects with positions r and contrast bc
    and diffusion 6x6 matrix (4 times 3x3 ) DTT,DRT,DTR,DRR
    calculates [D(q)*q*q*S(q) , S(Q)] + incoherent

    Parameters
    ----------
    point : array 1 x 3
        point on unit sphere as direction of q
    r: array N x 3
        positions for N atoms
    q : float
        scattering vector length
    bc : array N x 1
        contrast or scattering length
    b2inc : array N x 1
        incoherent scattering length squared
    D66 : array 6x6
        6x6 diffusion tensor with DTT,DRT,DTR,DRR as
        3x3 arrays for translational, rotational diffusion and cross terms between transrot and rottrans

    Notes
    -----
    needs further calculation for error and final diffusion value
    res[2]=res[2]/res[1]/q**2+res[3]*res[0]/res[1]**2/q**2
    res[0]=res[0]/res[1]/q**2

    see Equation 1
    Exploring internal protein dynamics by neutron spin echo spectroscopy
    R. Biehl, M. Monkenbusch and D. Richter
    Soft Matter, 2011, 7 (4), 1299 - 1307

    """

    ###############################################
    qx = q * point  # 3d q vector
    eiqr = np.exp(np.sum((qx * r) * 1j, axis=1))  # 169µs
    beiqr = bc * eiqr  # 4µs
    Nqx = np.tile(qx, (r.shape[0], 1))  # 11µs
    qxr = np.cross(r, qx)  # 60µs
    qqxr = np.hstack([Nqx, qxr])  # 23µs

    # main calculation
    # coherent
    qqxrDqqxr = np.einsum('ij,jl', qqxr, np.einsum('jk,lk', D66, qqxr))  # 17ms
    DqqSq = np.einsum('i,il,l', beiqr, qqxrDqqxr, beiqr.conj())  # 15ms
    Sq = np.abs(np.einsum('i->', beiqr)) ** 2  # 7µs
    # incoherent
    DqqSq_inc = np.einsum('i,ij,jk,ik', b2inc, qqxr, D66, qqxr)  # 530µs
    Sq_inc = np.sum(b2inc)

    return DqqSq.real, Sq.real, DqqSq_inc.real, Sq_inc.real


def diffusionTRUnivYlm(objekt, Dtrans=0., Drot=0., Rhydro=0., **kwargs):
    r"""
    Effective diffusion *Deff* of a rigid particle based on the Rayleigh expansion (Ylm).

    Mixed contribution from translational and rotational diffusion in the initial slope.
    Only SCALAR diffusion coefficients.  See [1]_.

    Parameters
    ----------
    objekt : atomgroup
        Objects  immersed in medium.
    qlist : array, list of float
        Scattering vectors in units 1/nm.
    Dtrans : float, default = 0
        Translational diffusion coefficient in nm^2/ps = 1e5 A^2/ns.
        If 0 calculated as :math:`D_{trans} = kT / (6\pi \eta R_{hydro})` .
    Drot : float , default = 0
        Rotational diffusion coefficient in 1/ps.
        If 0, calculated as :math:`D_{rot} = kT/ (8\pi\eta R_{hydro}^3)`.
    Rhydro : float, default = 0
        Hydrodynamic radius in nm.
        If negative, Rhydro is calculated from the SESVolume as equivalent sphere with
        :math:`R_h=(\frac{3V_{SES}}{4\pi})^{1/3} + 0.3` as a rough estimate.

        In general the shape anisotropy needs to be accounted using :py:func:`~.libs.HullRad.hullRad`.
    lmax : int; default=15
        Maximum order spherical harmonics. For larger Q this needs to be increased.
    cubesize : float, default None
        Cube length (in units nm) for coarse graining, None means no coarse graining.
        For larger proteins the computation takes some time.
        Cubesize defines the size of a cubic grid in which atomic data as positions, formfactor and normal modes
        are averaged to realize a coarse graining and speedup the computation.
        The size should be adjusted to the protein size. This works for residue and atomic modes.

    Returns
    -------
    dataArray [q, Deff]

    Notes
    -----
    According to [2]_ the field autocorrelation function (as measured by NSE) of a single particle :math:`I_1(Q,t)`
    (see :py:func:`~.bio.scatter.intScatFuncYlm` for details) is

    .. math:: I_1(Q,t) = e^{-D_{trans}Q^2t}\sum_l S_l(Q)e^{-l(l+1)D_{rot}t}

    Accordingly in the initial slope defined as
    :math:`\Gamma =  Q^2D = -\lim_{t \to 0 } \bigg[\frac{d}{dt} ln(\frac{I(Q,t)}{I(Q,0)})\bigg]`
    the effective diffusion Deff is [1]_

    .. math:: D_{eff} = D_{trans} + \frac{\sum_l S_l(Q) l(l+1)D_{rot}}{Q^2 \sum_l S_l(Q) }

    :math:`S_l(Q)` as defined in :py:func:`~.bio.scatter.intScatFuncYlm`.

    Examples
    --------
    Comparison using an equivalent sphere model :math:`R_h=(\frac{3V_{SES}}{4\pi})^{1/3} + 0.3` from SESVolume with an
    improved calculation taking the protein shape anisotropy from the pdb structure into account.
    Trans/rot diffusion is calculated using :py:func:`~.libs.HullRad.hullRad`.

    In general the shape anisotropy needs to be accounted.
    ::

     import jscatter as js
     import numpy as np
     p=js.grace()
     p.multi(1,2,hgap=0)
     for i,pdb in enumerate(['3pgk', '4f5s']):
         bioassembly = js.bio.fetch_pdb(pdb, biounit=True)
         uni = js.bio.scatteringUniverse(bioassembly)
         uni.qlist = np.r_[0.01,0.1:2:0.1,2:5:0.3]
         # Dtrans determined as sphere with SESVolume
         Dq = js.bio.diffusionTRUnivYlm(uni)
         # using hullRad which takes shape int account
         res = js.bio.hullRad(uni.select_atoms('protein'))
         # Dtrans/rot with conversion to nm²/ps and 1/ps
         Dtrans = res['Dt'] * 1e2  # nm²/ps
         Drot = res['Dr'] * 1e-12  # 1/ps
         Dq_hr = js.bio.diffusionTRUnivYlm(uni,Dtrans=Dtrans,Drot=Drot)
         p[i].plot(Dq,le='equivalent sphere')
         p[i].plot(Dq_hr, le='accounting shape ')
         p[i].xaxis(label='q / nm\S-1')
         p[i].legend(x=0.25,y=13e-5)

     p[0].yaxis(min=5e-5,max=14e-5,formula='$t*1e4',label=r'D\seff\N / 10\S-4\Nnm\S2\N/ps')
     p[1].yaxis(min=5e-5,max=14e-5,label='',ticklabel=False)
     p.title(' '*30+'Comparison equivalent sphere with shape anisotropy',size=1.4)
     p[0].subtitle('phosphoglycerate kinase')
     p[1].subtitle('bovine serum albumin')
     # p.save(js.examples.imagepath+'/DqYlm.jpg')

    .. image:: ../../examples/images/DqYlm.jpg
     :align: center
     :width: 50 %
     :alt: DqYlm


    References
    ----------
    .. [1] Exploring internal protein dynamics by neutron spin echo spectroscopy
           R. Biehl, M. Monkenbusch and D. Richter
           Soft Matter, 2011, 7, 1299–1307, DOI:10.1039/c0sm00683a
    .. [2] Effect of rotational diffusion on quasielastic light scattering from fractal colloid aggregates
           Lindsay H. Klein, R. Weitz, D. Lin, M. Meakin,
           Physical Review A  1988 vol: 38 (5) pp: 2614-2626

    """
    u = objekt.universe
    if isinstance(objekt, mda.scatteringUniverse):
        objekt = u.atoms

    mode = kwargs.pop('mode', 'n')
    output = kwargs.pop('output', 'True')
    surfdensity = kwargs.pop('surfdensity', None)
    refreshVolume = kwargs.pop('refreshVolume', True)
    u.qlist = kwargs.pop('qlist', u.qlist)
    u.error = kwargs.pop('error', u.error)
    lmax = kwargs.pop('lmax', 15)
    cubesize = kwargs.pop('cubesize', None)

    positions, formfactors, I0, ffinc2, sld, sldExclSolvent = \
        prepScatGroups(objekt, mode=mode, surfdensity=surfdensity, refreshVolume=refreshVolume, output=output, **kwargs)

    if cubesize is not None:
        # do a coarse graining to reduce computing time
        # average positions and formfactors according to cube grid
        positions, formfactors, ffinc2, _ = \
            coarseGraining(u, positions, formfactors, ffinc2, cubesize=cubesize)

    if Rhydro <= 0.:
        # sphere with same volume
        Rhydro = (3. * u.SESVolume / 4 / pi) ** (1. / 3.) + 0.3

    visc = (formel.viscosity(mat='d2o', T=u.temperature) * u.d2oFract +
            formel.viscosity(mat='h2o', T=u.temperature) * (1 - u.d2oFract))

    # Diffusion coefficients in nm^2/ps = 1e5 A^2/ns
    if Dtrans > 0.:
        Rhydro = co.k * u.temperature / (6. * pi * visc * 1e-18 * Dtrans * 1e3)
    DTeff = co.k * u.temperature / (6. * pi * visc * 1e-18 * Rhydro) * 1e-3
    if Drot <= 0.:
        DReff = co.k * u.temperature / (8. * pi * visc * 1e-18 * Rhydro ** 3) / 1e3
    else:
        DReff = Drot

    # spherical coordinates
    r, p, t = formel.xyz2rphitheta(positions).T
    # partial amplitudes
    jl_q, ylm = _getjfylm(u, r, p, t, lmax)

    # sum up partial amplitudes
    rGamma1 = []
    partialAmplitude_lm = []
    for iq, q in enumerate(u.qlist):
        b = formfactors[:, iq]
        partialAmplitude_lm.append([])
        for l in range(0, lmax + 1):
            Sll = 0.
            for m in range(0, 2 * l + 1):  # m-l ist die liste m= -l,.0...,l
                AProt = np.add.reduce(b * np.array(ylm[l][m], complex) * jl_q[iq][l])
                Sll += abs(AProt) ** 2
            partialAmplitude_lm[-1].append(Sll)
        Gamma1tr = 0.  # 1. Cumulant     trans +rot
        Gamma1d = 0.  # S(q)   divisor
        for l in range(0, lmax + 1):
            Gamma1tr += partialAmplitude_lm[-1][l] * (l * (l + 1) * DReff)
            Gamma1d += partialAmplitude_lm[-1][l]
        Gamma1 = (Gamma1tr / Gamma1d)
        rGamma1.append(DTeff + Gamma1 / q ** 2)  #

    result = dA(np.r_[[u.qlist, rGamma1]])
    mda.copyUnivProp(u, result)
    result.Rh = Rhydro
    result.Dtrans = DTeff
    result.Drot = DReff
    result.viscosity = visc
    result.lmax = lmax
    result.columnname = 'q; Deff'
    result.setColumnIndex(iey=None)
    if output.startswith('par'):
        # here we add partial amplitudes for later usage in other functions
        result.partialAmplitude_lm = np.r_[partialAmplitude_lm]
        result.partialAmplitude_lm_q = u.qlist
    return result


def intScatFuncYlm(objekt, Dtrans=0., Drot=0., Rhydro=0., **kwargs):
    r"""
    ISF based on the Rayleigh expansion for diffusing rigid particles with **scalar** Dtrans/Drot .

    I(q,t)/I(q,0) based on the Rayleigh expansion for **scalar** translational and
    rotational diffusion as described in [2]_ and used in [1]_ .

    Parameters
    ----------
    objekt : universe
        Atomgroup universe
    tlist : array, default = 10 values between 100ps to 100ns
        Time points in ps units.
        If None it is taken from objekt.universe.tlist.
        qlist : array, list of float
        Scattering vectors in units 1/nm.
    Dtrans : float, default = 0
        Translational diffusion coefficient in nm^2/ps = 1e5 A^2/ns.
        If 0 calculated from Rhydro.
    Drot : float , default = 0
        Rotational diffusion coefficient in 1/ps
        If 0 calculated from Rhydro
    Rhydro : float, default = 0
        Hydrodynamic radius in nm.
        If negative, Rhydro is calculated from the SESVolume as equivalent sphere with
        :math:`R_h=(\frac{3V_{SES}}{4\pi})^{1/3} + 0.3` as a rough estimate.

        In general the shape anisotropy needs to be accounted using :py:func:`~.libs.HullRad.hullRad`.
    lmax : int; default=15
        Maximum order spherical harmonics.For karger Q this needs to be increased.
    kwargs :
        Additional keyword arguments are passed to diffusionTRUnivYlm
    cubesize : float, default None
        Cube length (in units nm) for coarse graining, None means no coarse graining.
        For larger proteins the computation takes some time.
        Cubesize defines the size of a cubic grid in which atomic data as positions, formfactor and normal modes
        are averaged to realize a coarse graining and speedup the computation.
        The size should be adjusted to the protein size. This works for residue and atomic modes.

    Returns
    -------
    dataList with a dataArray for each q in qlist
        to get only I(q,t) as Y values use
        cohIntScaIntUnivYlm(....)[0].Y

    Notes
    -----
    We use equ 24 in [2]_ to calculate the field autocorrelation function of a single particle :math:`I_1(Q,t)`

    .. math:: I_1(Q,t) = e^{-D_{trans}Q^2t}\sum_l S_l(Q)e^{-l(l+1)D_{rot}t}

    where NSE measures :math:`I_1(Q,t)/I_1(Q,t=0)` as described in [1]_.

    The partial scattering amplitudes :math:`S_l(Q)` are defined as

    .. math:: S_l(Q) = \sum_m \bigg| \sum_j b_j(Q)j_l(Qr_j) Y_{lm}(\Omega_j)  \bigg|^2

    where :math:`j_l` are the spherical Bessel functions, :math:`Y_{lm}` are spherical harmonics and :math:`\Omega_{j}`
    denotes the orientation of the position vector of the atom at position :math:`r_j` with scattering amplitude
    :math:`b_j`.

    For larger Q a larger lmax is needed as it defines the resolution of the calculation.

    Examples
    --------
    ::

     import jscatter as js
     import numpy as np
     uni = js.bio.scatteringUniverse('3pgk')
     uni.qlist = np.r_[0.01,0.1:2:0.2]
     uni.tlist = np.r_[1,10:1e4:50]
     # Without arguments Dtrans/Drot correspond to sphere volume of SESVolume
     Iqt = js.bio.intScatFuncYlm(uni.residues)
     p = js.grace()
     p.plot(Iqt)
     p.yaxis(label=r'I(Q,t)/I(Q,0)')
     p.xaxis(label=r'\xt\f{} / ps')
     p.title('ISF for translational/rotational diffusion')
     #p.save(js.examples.imagepath+'/iqttranrot.jpg')

    .. image:: ../../examples/images/iqttranrot.jpg
     :align: center
     :width: 50 %
     :alt: hydrationlayerdensity


    References
    ----------
    .. [1] Exploring internal protein dynamics by neutron spin echo spectroscopy
           R. Biehl, M. Monkenbusch and D. Richter
           Soft Matter, 2011, 7, 1299–1307, DOI:10.1039/c0sm00683a
    .. [2] Effect of rotational diffusion on quasielastic light scattering from fractal colloid aggregates
           Lindsay H Klein R Weitz D Lin M Meakin P  Physical Review A  1988 vol: 38 (5) pp: 2614-2626


    """
    # no preparation here as it is done if necessary in later Dylm=diffusionTRUnivYlm
    u = objekt.universe
    if isinstance(objekt, mda.scatteringUniverse):
        objekt = u.atoms

    u.qlist = kwargs.pop('qlist', u.qlist)
    u.error = kwargs.pop('error', u.error)
    u.tlist = kwargs.pop('tlist', u.tlist)

    Dylm = diffusionTRUnivYlm(objekt, Dtrans=Dtrans, Drot=Drot, Rhydro=Rhydro, output='par', **kwargs)

    palm = Dylm.partialAmplitude_lm
    palm_q = Dylm.partialAmplitude_lm_q

    cohIntScaFunc = dL()
    for q in u.qlist:
        Sqt = 0
        Sqq = 0
        # interpolate Scattering amplitudes  works on arrays
        palmi = [np.interp(q, palm_q, palm_l) for palm_l in palm.T]
        for l1 in range(len(palmi)):
            Sqt += palmi[l1] * np.exp(-l1 * (l1 + 1) * Dylm.Drot * u.tlist)
            Sqq += palmi[l1]
        Sqt = np.c_[u.tlist, Sqt / Sqq * np.exp(-q ** 2 * Dylm.Dtrans * u.tlist)].T
        cohIntScaFunc.append(Sqt)
        mda.copyUnivProp(u, cohIntScaFunc[-1])
        cohIntScaFunc[-1].q = q
        cohIntScaFunc[-1].Sq = Sqq
        cohIntScaFunc[-1].lmax = Dylm.lmax
        cohIntScaFunc[-1].Drot = Dylm.Drot
        cohIntScaFunc[-1].Dtrans = Dylm.Dtrans
        cohIntScaFunc[-1].Deff = Dylm.interp(q)[0]
        cohIntScaFunc[-1].Rh = Dylm.Rh
        cohIntScaFunc[-1].viscosity = Dylm.viscosity
        cohIntScaFunc[-1].columnname = 'time; Sqt; Sqt0'
        cohIntScaFunc[-1].setColumnIndex(iey=None)
    return cohIntScaFunc


def intScatFuncPMode(modes, n, **kwargs):
    r"""
    Dynamic mode form factor P_n(q) to calculate ISF of normal mode displacements
    in small displacement approximation.

    Mode *n* contribution to ISF :math:`I(Q,t)/I(Q,0) = e^{-\lambda t}\hat{P}(Q)` or
    additional contribution to the diffusion coefficient in initial slope :math:`\Delta D_{eff}(Q)` .

    Parameters
    ----------
    modes  : normal mode objekt
        Normal modes.
    n    : int
        Index of normal mode.
    cubesize : float, default None
        Cube length (in units nm) for coarse graining, None means no coarse graining.
        For larger proteins the computation takes some time.
        Cubesize defines the size of a cubic grid in which atomic data as positions, formfactor and normal modes
        are averaged to realize a coarse graining and speedup the computation.
        The size should be adjusted to the protein size.
        This works for residue and atomic modes but needs enough atoms in a cube.

    used from modes or universe:
        - modes.u.qlist :  scattering vector q from mode universe in units 1/nm
        - modes.u.temperature : temperature of the mode universe
        - scattering mode as 'n' or 'x' is allowed. For neutron scattering the result corresponds to NSE
          while for 'x' the results corresponds to X-ray photon correlation spectroscopy (XPCS).
        -  displacements from kTdisplacements are used. See the corresponding mode type.

    Returns
    -------
    dataArray [q, Pn, Fq, Pninc]
        - q scattering vector, units 1/nm
        - Pn coherent dynamic formfactor of mode :math:`\alpha`, unit nm²
        - Pninc incoherent dynamic formfactor of mode :math:`\alpha`, unit nm²
        - Fq coherent formfactor, unit nm²
        - Pn and Pninc relate to *mode(i).kTdisplacement* =
          :math:`\vec{d}_{\alpha}=\sqrt{\frac{kT}{k_{\alpha}}}\hat{v}`
          in thermal equilibrium. A scalar scaling factor scales accordingly the force constants used
          for normal mode calculation.

    Notes
    -----
    The formfactor is

    .. math:: F(Q) = \Big \langle \sum_{k,l} b_kb_l e^{iQ(r_k-r_l)} \Big \rangle

    for atoms *k,l* with respective scattering length *b*.
    For small displacements, P(Q) may be obtained in analogy to a 1-phonon approximation of the cross section
    (or elastic normal modes) for displacements along normal mode *α* as [1]_ (for incoherent only k=l):

    .. math:: P_{\alpha}(Q) =& \Big \langle \sum_{k,l} b_kb_l e^{iQ(r_k-r_l)}
                              (\vec{Q}*\vec{d}_{\alpha,k}) (\vec{Q}*\vec{d}_{\alpha,l}) \Big \rangle

    with normal mode displacements :math:`\vec{d}_{\alpha,l} = a_{l,\alpha} \hat{v}_{\alpha,l}` of
    weighted orthogonal eigenvectors :math:`\hat{v}_{\alpha,l}`.

    For elastic modes in thermal equilibrium the mode amplitude :math:`a` is related to the
    (effective) elastic mode force constant :math:`k_{\alpha}=m\omega^2_{\alpha}` (and eigenfrequency)
    by :math:`a_{l,\alpha} =\sqrt{\frac{kT}{k_{\alpha}}} = \sqrt{\frac{kT}{m_l\omega^2_{\alpha}}}`

    Assuming that the modes are overdamped instead of oscillating the mode amplitudes should approximately not change
    but the oscillation needs to be replaced by a relaxation.

    For a common exponential decreasing relaxation along modes we yield for the ISF of multiple modes [2]_:

    .. math:: I(Q,t)/I(Q,0) = e^{-\lambda t}\hat{P}(Q) \text{ with }
              \hat{P}(Q) = \frac{\sum_{\alpha} P_{\alpha}(Q)}{[F(Q) + \sum_{\alpha} P_{\alpha}(Q)]}

    We also may weight the relaxation times according to the eigenvalues of the modes
    or use independent relaxation times. It should be mentioned that the eigenvalues are dependent on geometry and
    the used force atomic constants and therefore to some extent vague.

    The additional contribution to the effective diffusion coefficient of a single mode in initial slope is [1]_:

    .. math:: \Delta D_{eff}(Q) =
                    \frac{\lambda_{\alpha} a_{\alpha}^2 P_{\alpha}(Q)}{Q^2[F(Q)+a_{\alpha}^2 P_{\alpha}(Q)]}

    with the inverse relaxation time :math:`\lambda_{\alpha}` and a mode
    amplitude scaling factor :math:`a_{\alpha}`. The amplitude scaling factor can be used for fitting

    dummy surface atoms are ignored.

    Examples
    --------
    Alcohol dehydrogenase is a tetramer with 4 clefts where the active center is located.

    The PDB structure presents a structure with 2 clefts in a closed configuration with bound cofactor NADH
    and in 2 clefts an open configuration without cofactor.

    The following normal mode analysis identifies modes with large domain movements similar to [1]_.
    In [1]_ a configuration of 4 open clefts and 4 closed clefts is compared.
    ::

     import jscatter as js
     import numpy as np
     import matplotlib.image as mpimg

     adh = js.bio.fetch_pdb('4w6z.pdb1')
     # the 2 dimers in are in model 1 and 2 and need to be merged into one.
     adhmerged = js.bio.mergePDBModel(adh)
     uni=js.bio.scatteringUniverse(adhmerged)
     uni.qlist=np.r_[0.01,0.1:2:0.1]

     # do normal mode analysis without cofactors but 2 clefts still closed
     nm = js.bio.vibNM(uni.select_atoms('protein').residues)

     p = js.mplot()
     a=30
     for NN in [7,8,9,10,11,12]:
        Ph = js.bio.intScatFuncPMode(nm, NN)
        p.Plot(Ph.X, a**2 * Ph._Pn/(Ph._Fq+Ph._Pn)/Ph.X**2, le=f'mode {NN}  rmsd={Ph.kTrmsd*a**2:.2f} A')

     p.Yaxis(label=r'$\Delta D(Q)/\lambda \;/\; nm^2 $',min=0,max=0.013)
     p[0].Xaxis(label=r'$Q / nm^{-1}$')
     p[0].Legend()
     p.Text(string='domain motion modes',x=1,y=0.01)
     p.Text(string='more local modes',x=1,y=0.001)
     p.Title('ADH domain motions')
     p[0].set_title('kT displacements of modes')

     # add image
     adhimg = mpimg.imread(js.examples.imagepath+'/adh.png')
     axin = p[0].inset_axes([0.,0.05,0.5,0.6])
     axin.imshow(adhimg)
     axin.axis('off')
     # p.Save(js.examples.imagepath+'/biodeltaDeff.jpg')

    .. image:: ../../examples/images/biodeltaDeff.jpg
     :align: center
     :width: 50 %
     :alt: biodeltaDeff



    References
    ----------
    .. [1] Direct Observation of Correlated Interdomain Motion in Alcohol Dehydrogenase
            Biehl R et al.Phys. Rev. Lett. 101, 138102 (2008)
    .. [2] Large Domain Fluctuations on 50-ns Timescale Enable Catalytic Activity in Phosphoglycerate Kinase
           R. Inoue, R. Biehl, T. Rosenkranz, J. Fitter, M. Monkenbusch, A. Radulescu, B. Farago, and D. Richter
           Biophysical Journal 99, 2309–2317 (2010), doi: 10.1016/j.bpj.2010.08.017


    """
    u = modes.u
    objekt = modes.ag

    mode = kwargs.pop('mode', 'n')
    ncpu = kwargs.pop('ncpu', 0 if mp.current_process().name == 'MainProcess' else 1)
    output = kwargs.pop('output', True)
    surfdensity = kwargs.pop('surfdensity', None)
    refreshVolume = kwargs.pop('refreshVolume', True)
    u.qlist = kwargs.pop('qlist', u.qlist)
    u.error = kwargs.pop('error', u.error)
    u.tlist = kwargs.pop('tlist', u.tlist)
    cubesize = kwargs.pop('cubesize', None)

    positions, formfactors, I0, ffinc2, sld, sldExclSolvent = \
        prepScatGroups(objekt, mode=mode,
                       surfdensity=surfdensity,
                       refreshVolume=refreshVolume,
                       output=output,
                       suppressSurface=True,
                       **kwargs)

    columnname = 'q; Pn; Fq; Pninc'
    if output:
        print("start integrating ")
        print(columnname)

    # get mode in nm units
    moden = modes.kTdisplacementNM(n)

    if cubesize is not None:
        # do a coarse graining to reduce computing time
        # average positions and formfactors according to cube grid
        positions, formfactors, ffinc2, moden = \
            coarseGraining(u, positions, formfactors, ffinc2, nm=moden, cubesize=cubesize)

    result = formel.doForList(intScatFuncPMode_qlist, [(q, i) for i, q in enumerate(u.qlist)],
                              formfactors=formfactors,
                              ffinc2=ffinc2,
                              positions=positions,
                              moden=moden,
                              error=u.error, loopover=['q', 'iq'], ncpu=ncpu)

    result = dA(np.array(result).T, dtype=float)
    result.isort()
    mda.copyUnivProp(u, result)
    result.modeNumber = n
    result.modeEigenvalue = modes[n].eigenvalue
    result.kTrmsd = modes[n].kTrmsd
    result.kTrmsdNM = modes[n].kTrmsdNM
    result.columnname = columnname
    result.setColumnIndex(iey=4)
    return result


def intScatFuncPMode_qlist(q, formfactors, ffinc2, error, positions, moden, iq):
    # TODO add mode displacement for dummy surface in positions
    b = formfactors[:, iq]
    binc2 = ffinc2[:, iq]
    res = formel.sphereAverage(intScatFuncPMode_q, error, positions, moden, b, binc2, q=q)
    print(f'{q:.2f} ' + ''.join([f'{a:7.3g}  ' for a in res[:3]]))
    return np.r_[q, res[:3]]


def intScatFuncPMode_q(point, r, mode, bcminusv, b2inc, q):
    """
    coherent dynamic form factor of normal mode Mode

    may be obtained in analogy to a 1 phonon approximation of the
    cross section, which in fact is an expansion of the cross
    section with respect to small displacements.

    Parameters
    ----------
    point : array 3 x 1
        point on sphere as direction of q
    q : float
        scattering vector length
    r : array N x 3
        vector of atom positions
    mode : array N x 3
        atomic displacements along normal mode
    bcminusv : array N x x1
        contrast or scattering length for q
    b2inc : array N x 1
        incoherent scattering length squared

    Notes
    -----
    see  P_alpha(Q) of Equation 3 in
    Exploring internal protein dynamics by neutron spin echo spectroscopy
    R. Biehl, M. Monkenbusch and D. Richter
    Soft Matter, 2011, 7 (4), 1299 - 1307
    """

    # TODO -> use Fortran
    qx = q * point
    eiqr = np.exp(np.sum((qx * r) * 1j, axis=1))  # 1.15 ms
    qxMode = np.einsum('j,ij', qx, mode)  # 32.4 µs
    beiqr = eiqr * bcminusv
    # square of sum includes all mixed terms in sum of squared
    Sq = np.abs(np.einsum('i->', beiqr)) ** 2  # 18 µs

    beiqrNM = eiqr * qxMode * bcminusv  # 23   µs
    SqNM = np.abs(np.einsum('i->', beiqrNM)) ** 2  # 17.9 µs

    beiqrNMinc = eiqr * qxMode * b2inc
    SqNMinc = np.einsum('i,i', beiqrNMinc, beiqrNMinc.conj())  # 16µs

    return SqNM.real, Sq.real, SqNMinc.real


def intScatFuncOU(brownianmodes, nm, **kwargs):
    r"""
    ISF I(q,t) for Ornstein-Uhlenbeck process of normal mode domain motions in a harmonic potential with friction.

    Displacements along normal modes in harmonic potential with additional internal friction
    leading to overdamped motions along Brownian Modes. The theory is described in [1]_ and [2]_ and
    applied to an immunoglobulin in [3]_.

    The model relates internal friction and force constants to amplitudes and relaxation times

    Parameters
    ----------
    brownianmodes : brownianMode object
        Brownian normal modes =>  the force constant matrix normalized to friction

        Friction and forceconstants are defined in mode object.
    nm : list of int
        Indices of the modes starting with 6 for first nontrivial mode.
    cubesize : float, default None
        Cube length (in units nm) for coarse graining, None means no coarse graining.
        For larger proteins the computation takes some time.
        Cubesize defines the size of a cubic grid in which atomic data as positions, formfactor and normal modes
        are averaged to realize a coarse graining and speedup the computation.
        The size should be adjusted to the protein size. This works for residue and atomic modes.
    used from modes or universe:
        - relaxationtime in units ps
        - u.tlist : time points from universe in ps
        - u.qlist :  scattering vector q from universe
        - u.temperature : u.temperature from universe
        - scattering mode as 'n' or 'x' is allowed. For neutron scattering the result corresponds to NSE
          while for 'x' the results corresponds to X-ray photon correlation spectroscopy (XPCS).

    Returns
    -------
    dataList : list of dataArray
      - .X : time points
      - .Y : Fqt(t)/Fqt(t=0)             coherent, equ 11+41+49+79 with 81 in [1]_
      - .q                               scattering vector unit 1/nm
      - .relaxationtimes
      - .frictionPerMode                 effectiveFriction of modes see NMmode
      - .forceconstantFromFriction       effectiveForceConstant of modes
      - .Sqt0                            amplitude for t=0     equ 11+41+79 with 81 in [1]_ with error
      - .Sqtinf_DW                       amplitude t=inf , equ 11+41+49 in [1]_ Debye-Waller factor with error in [1]
      - .Sqt00                           amplitude t=0 ,  equ 11+41+50 in [1]_  with error in [1]
      - .Sq_amp0                         sum_i_j[bi*bj] = no displacements = normal formfactor without DW
      - .elasticplateau                  Sqtinf_DW[0]/Sqt0 ; (1-elasticplateau) is the NSE amplitude
      - .frictionPerMode                 friction  mode weighted by mode vectors = b*frict*b
      - .brownianModeRMSD                mode RMSD

    Notes
    -----
    The dynamics of a protein can be described under the assumption of dynamic decoupling [3]_ by a combination

    .. math:: F(Q,t) = F_{trans}(Q,t) \cdot F_{rot}(Q,t) \cdot F_{int}(Q,t)

    The intermediate scattering function :math:`F_{int}(Q,t)` of atoms or subunits *k* with scattering length
    :math:`b_k` at positions :math:`R_k` describing our internal dynamics can be written as

    .. math:: F(Q,t) = \Big \langle \sum_{k,l} b_kb_l e^{iQR_k(t)}e^{iQR_l(0)} \Big \rangle

    With displacements :math:`u_k` from equilibrium position :math:`R_k^{eq}` we can use
    :math:`R_k=R_k^{eq} + u_k(t)` resulting in

    .. math:: F(Q,t) = \Big \langle \sum_{k,l} b_kb_l e^{iqR_k^{eq}}e^{iqR_l^{eq}}
                       f_{kl}(Q,\infty)  f_{kl}^{\prime}(Q,t) \Big \rangle

    The constant term is related to the 3N vibrational modes *j* and only dependent on the harmonic potential as

    .. math:: f_{kl}(Q,\infty) = exp \Big(-\sum_{j=1..3N} \frac{1}{2} ((d_{jk}\cdot Q)^2 + (d_{jl} \cdot Q)^2)  \Big)

    with vibrational displacements  :math:`d_{jk} = \sqrt{kT/(m_k\omega_j^2)}\hat{v}_{jk}` for elastic normal mode
    :math:`\hat{v}_j` that correspond to the width in a Gaussian distribution around the equilibrium configuration
    in a potential with mean force constant :math:`k_j=m_j^{eff}\omega_j^2`
    (effective mass :math:`m_j^{eff}`).
    See :py:func:`~jscatter.bio.nma.vibNM` for elastic modes.
    With increasing :math:`\omega` the mode amplitudes become smaller.

    In the high friction limit the time dependent part within Smoluchowski dynamics (friction dominated)
    is described by

    .. math:: f_{kl}^{\prime}(Q,0) = exp \Big(\sum_{j=1..3N} (e_{jk}Q)(e_{jl}Q)e^{-\lambda_jt} \Big)

    with displacements :math:`e_{jk} = \sqrt{kT/(\lambda_j\Gamma_j)}\hat{b}_{jk}` for
    Brownian mode :math:`\hat{b}_j`, mode friction :math:`\Gamma_j = \hat{b}^T\gamma\hat{b}`
    and inverse mode relaxation time :math:`\lambda_j`.
    The displacement  :math:`e_{jk}` corresponds to the displacement within relaxation time :math:`1/\lambda_j`.
    See :py:func:`~jscatter.bio.nma.brownianNMdiag` for Brownian modes and the definition of the friction matrix
    :math:`\gamma` that defines the mode with the force constant matrix.

    Taylor expansion of the Smoluchowsky dynamics leads to a description for small displacements (or low Q) [1]_
    that results in a description as found in :py:func:`intScatFuncPMode`


    - Friction related to translational diffusion can be estimated from :math:`f=kT/D`.
    - Equipartition determine force constant from msd :math:`f<x^2>/2 = 0.5kT  ==> f= kT/<x^2>`
    - dummy surface atoms are ignored.


    Examples
    --------
    The small protein calmodulin as example.
    Domain motions might be quite fast as here for demonstration the internal friction is choosen low.
    This is a synthetic example without experimental proof just as demonstration.
    See [3]_ for experimental result using antibodies.

    ::

     import jscatter as js
     import numpy as np
     uni=js.bio.scatteringUniverse('3CLN')
     uni.qlist=np.r_[0.01,0.1:2:0.3]
     uni.tlist = np.r_[1:2000:20j,2000:10000:20j]

     # rigid protein trans/rot diffusion
     hR = js.bio.hullRad(uni.atoms)
     Dtrans = hR['Dt'] * 1e2  # in nm²/ps
     Drot = hR['Dr'] * 1e-12  # in 1/ps
     Iqt = js.bio.intScatFuncYlm(uni.residues, Dtrans=Dtrans, Drot=Drot)

     # internal domain motions
     bnm = js.bio.brownianNMdiag(uni.residues,k_b=70, f_d=5)
     OU = js.bio.intScatFuncOU(bnm, [6,7,8])

     # combine diffusion and internal dynamics
     IqtOU = Iqt.copy()
     for i, iqtou in enumerate(IqtOU):
        ou = OU.filter(q=iqtou.q)[0]
        # combining in this case its just multiplication in time domain
        iqtou.Y = iqtou.Y * ou.Y

     # show the result comparing the contributions
     p=js.grace(2,0.8)
     p.multi(1, 3, hgap=0)
     p[0].plot(Iqt,li=-1)
     p[1].plot(OU,li=-1)
     p[2].plot(IqtOU,sy=[1,0.3,-1],li=-1)
     for i in [0,1,2]:
        p[i].xaxis(label=r'\xt\f{} / ps',min=0,max=4999,charsize=1.5)
        p[i].yaxis(scale='log',min=0.4,max=1)
     p[0].yaxis(label='I(Q,t)/I(Q,0)',charsize=1.5)
     p[0].subtitle('trans/rot diffusion',size=1.5)
     p[1].subtitle('internal dynamics',size=1.5)
     p[2].subtitle('trans/rot diffusion + internal dynamics',size=1.5)
     p[1].title('friction dominated internal dynamics in harmonic potential',size=2)
     #p.save(js.examples.imagepath+'/iqtOrnsteinUhlenbeck.jpg',size=(1000,400))

    .. image:: ../../examples/images/iqtOrnsteinUhlenbeck.jpg
     :align: center
     :width: 90 %
     :alt: iqtOrnsteinUhlenbeck


    References
    ----------
    .. [1] Inelastic neutron scattering from damped collective vibrations of macromolecules
           Gerald R. Kneller    Chemical Physics 261, 1-24, (2000)

    .. [2] Harmonicity in slow protein dynamics
           Hinsen K. et al.  Chemical Physics 261, 25, (2000)

    .. [3] Fast antibody fragment motion: flexible linkers act as entropic spring
           Laura R. Stingaciu, Oxana Ivanova, Michael Ohl, Ralf Biehl & Dieter Richter
           Scientific Reports 6, 22148 (2016)  doi:10.1038/srep22148

    """
    u = brownianmodes.u

    mode = kwargs.pop('mode', 'n')
    ncpu = kwargs.pop('ncpu', 0 if mp.current_process().name == 'MainProcess' else 1)
    output = kwargs.pop('output', True)
    surfdensity = kwargs.pop('surfdensity', None)
    refreshVolume = kwargs.pop('refreshVolume', True)
    u.qlist = kwargs.pop('qlist', u.qlist)
    u.error = kwargs.pop('error', u.error)
    u.tlist = kwargs.pop('tlist', u.tlist)
    cubesize = kwargs.pop('cubesize', None)

    positions, formfactors, I0, ffinc2, sld, sldExclSolvent = \
        prepScatGroups(brownianmodes.ag,
                       mode=mode,
                       refreshVolume=refreshVolume,
                       surfdensity=surfdensity,
                       output=output,
                       suppressSurface=True,
                       **kwargs)

    # get relaxation times from normal mode
    bm = brownianmodes[nm]
    irt = [m.invRelaxTime for m in bm]

    # Mode has same shape as r for all modes in one object
    bDisplacements = np.empty((len(irt), brownianmodes.ag.n_atoms, 3))
    for i, j in enumerate(nm):
        # displacement as nm*sqrt(kT/(irt[i]*bm.eF(i)) in units nm
        bDisplacements[i, :, :] = brownianmodes.kTdisplacementNM(j)

    # same for vibrational modes
    # In case no vibrational mode is provided we use the brownian mode with appropriate relaxation time
    # for real displacement NM vectors the masses are not in these equations if all is diagonal
    # currently no vib modes as for diagonal friction both are th same
    # maybe in a future version we have a non diagonal friction matrix

    columnname = 't; Sqt'
    if output:
        print("start integrating")
        print('q     = Sqt(tmin) ... Sqt(tmax)')

    if cubesize is not None:
        # do a coarse graining to reduce computing time
        # average positions and formfactors according to cube grid
        positions, formfactors, ffinc2, bDisplacements = \
            coarseGraining(u, positions, formfactors, ffinc2, nm=bDisplacements, cubesize=cubesize)

    if 1:
        resu = fscatter.cloud.mda_parallel_cohinterscat_ou(qlist=u.qlist,
                                                           r=positions,
                                                           bdisplace=bDisplacements,
                                                           vdisplace=bDisplacements,
                                                           formfactors=formfactors,
                                                           b2inc=ffinc2,
                                                           tlist=u.tlist,
                                                           irt=irt,
                                                           nfib=u.error,
                                                           ncpu=ncpu)
        Slist = np.c_[u.qlist, resu]
    else:
        # for documentation of a pure python version
        resu = formel.doForList(formel.sphereAverage, u.qlist,
                                intScatFuncOU_q,
                                r=positions,
                                bdisplace=bDisplacements,
                                vdisplace=bDisplacements,
                                formfactors=formfactors,
                                b2inc=ffinc2,
                                tlist=u.tlist,
                                qlist=u.qlist,
                                irt=irt,
                                relError=u.error, loopover='q', ncpu=ncpu)
        # add q and remove errors at end of resu
        Slist = np.c_[u.qlist, resu][:, :u.tlist.shape[0] + 3 + 1]

    for q, res in zip(Slist[:, 0], Slist[:, 1:]):
        if output:
            print(f'{q:.3f}  =  {res[0]:.4g} ... {res[-1]:.4g}')
        try:
            result.append(dA(np.c_[u.tlist, res[2:-1].T].T))
        except NameError:
            result = dL(np.c_[u.tlist, res[2:-1].T].T)
        result[-1].columnname = columnname
        result[-1].setColumnIndex(iey=None)
        result[-1].Sqt0 = res[0]
        result[-1].Sqt00 = res[1]
        result[-1][1] = result[-1][1] / result[-1].Sqt0
        result[-1].Sqtinf_DW = res[-1]
        result[-1].temperature = u.temperature
        result[-1].relaxationtimes = [1 / rt for rt in irt]
        result[-1].frictionPerMode = [m.effectiveFriction for m in bm]
        result[-1].forceconstanFromFriction = [m.effectiveForceConstant for m in bm]
        result[-1].brownianModeRMSDNM = np.mean([m.kTrmsdNM ** 2 for m in bm]) ** 0.5
        result[-1].elasticplateau = result[-1].Sqtinf_DW / result[-1].Sqt0
        mda.copyUnivProp(u, result[-1])
        result[-1].q = q

        result[-1].Sq_amp0 = I0

    return result


def intScatFuncOU_q(point, r, bdisplace, vdisplace, formfactors, b2inc, q, tlist, qlist, irt):
    """
    Calculates the coherent intermediate scattering function I(q,t) for Ornstein-Uhlenbeck process

    The Fortran function mda_parallel_cohinterscat_ou is much faster.

    based on displacements along normal modes in harmonic potential
    as eigenvectors of friction-weighted force constant matrix
    relaxation by Brownian normal modes as overdamped relaxation

    Parameters
    ----------
    point : array 1 x 3
        Point on sphere as direction of q
    r: array N x 3
        Positions for N atoms
    bdisplace : array  m x N x 3
        Brownian modes displacements
        m mode vectors in unweighted coordinates as full displacement
        NOT normalized to 1
    vdisplace : array  m x N x 3
        Vibrational mode displacements
        m mode vectors in unweighted coordinates as full displacement
    q : float
        Scattering vector length
    tlist : array
        Timepoints in ns
    qlist : array
        Wavevectors in 1/nm
    b2inc : array N x 1
        incoherent scattering length squared
    irt : array ndim N
        inverse relaxation time for modes
        is the eigenvalue of the modes


    Returns
    -------
    Sqt=0, Sqt[...], Sqt=inf

    References
    ----------
    .. [1] Inelastic neutron scattering from damped collective vibrations of macromolecules
           Gerald R. Kneller    Chemical Physics 261, 1-24, (2000)

    """
    iq = np.searchsorted(qlist, q)
    qx = q * point  # point on sphere
    iqr = np.einsum('i,ji', qx, r) * 1j
    beiqr = formfactors[:, iq] * np.exp(iqr)  # reciprocal density
    qbmodes = np.einsum('i,jli->jl', qx, bdisplace)  # displacement projection for brownian modes
    qvmodes = np.einsum('i,jli->jl', qx, vdisplace)  # same for vibrational modes
    qvmodes2 = qvmodes ** 2  # square of above
    elambdat = np.exp(-1. * (irt * tlist[:, np.newaxis]))  # tlist is ft[:,i]   relaxation of mode i
    qmqmexplabdat = np.einsum('ij,il,mi->jlm', qbmodes, qbmodes, elambdat)  # brownian amplitude relaxation
    qmqmexplabdat0 = np.einsum('ij,il->jl', qbmodes, qbmodes)  # amplitude t=0
    #
    abdQinf = np.zeros((len(qvmodes2[0]), len(qvmodes2[0])), float)
    abdQ0 = np.zeros((len(qvmodes2[0]), len(qvmodes2[0])), float)
    for i in range(len(qvmodes2[:, 0])):
        abdQinf += (qvmodes2[i] + qvmodes2[i][:, None])  # t=inf
        abdQ0 += (qvmodes[i] - qvmodes[i][:, None]) ** 2  # t=0
    fab_q_inf = np.exp(-0.5 * abdQinf)
    fab_q_00 = np.exp(-0.5 * abdQ0)
    fab_q_t = np.exp(qmqmexplabdat)
    fab_q_0 = np.exp(qmqmexplabdat0)

    # sum over particles
    # full relaxation for all t, equ 79 with 81 in [1]_
    Sqt = np.einsum('i,j,ij,ijm->m', beiqr, beiqr.conj(), fab_q_inf, fab_q_t)
    # amplitude at t=0, equ 79 with 81 in [1]_
    Sqt0 = np.einsum('i,j,ij,ij->', beiqr, beiqr.conj(), fab_q_inf, fab_q_0)
    # amplitude at t=0 , equ 50 in [1]_
    Sqt00 = np.einsum('i,j,ij->', beiqr, beiqr.conj(), fab_q_00)
    # amplitude at t=infinity , equ 49 in [1]_
    Sqtinf = np.einsum('i,j,ij->', beiqr, beiqr.conj(), fab_q_inf)

    # we need to return a single array of float
    return np.r_[Sqt0.real, Sqt00.real, Sqt.real, Sqtinf.real]
