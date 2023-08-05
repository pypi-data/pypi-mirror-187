import sys
import typing


def convert_from_particle_system():
    ''' Add a new curves object based on the current state of the particle system

    '''

    pass


def convert_to_particle_system():
    ''' Add a new or update an existing hair particle system on the surface object

    '''

    pass


def sculptmode_toggle():
    ''' Enter/Exit sculpt mode for curves

    '''

    pass


def select_all(action: typing.Union[str, int] = 'TOGGLE'):
    ''' (De)select all control points

    :param action: Action, Selection action to execute * TOGGLE Toggle -- Toggle selection for all elements. * SELECT Select -- Select all elements. * DESELECT Deselect -- Deselect all elements. * INVERT Invert -- Invert selection of all elements.
    :type action: typing.Union[str, int]
    '''

    pass


def set_selection_domain(domain: typing.Union[str, int] = 'POINT'):
    ''' Change the mode used for selection masking in curves sculpt mode

    :param domain: Domain
    :type domain: typing.Union[str, int]
    '''

    pass


def snap_curves_to_surface(attach_mode: typing.Union[str, int] = 'NEAREST'):
    ''' Move curves so that the first point is exactly on the surface mesh

    :param attach_mode: Attach Mode, How to find the point on the surface to attach to * NEAREST Nearest -- Find the closest point on the surface for the root point of every curve and move the root there. * DEFORM Deform -- Re-attach curves to a deformed surface using the existing attachment information. This only works when the topology of the surface mesh has not changed.
    :type attach_mode: typing.Union[str, int]
    '''

    pass


def surface_set():
    ''' Use the active object as surface for selected curves objects and set it as the parent

    '''

    pass
