"""
InfoSpace - Python Library for Information Speed Theory

A library for simulating and computing with information spaces based on 
the Information Speed Theory.

Core concepts:
- Multiple information spaces I_k with different maximum speeds Vmax_k
- Energy calculations based on carriers
- Transformations between spaces
- Contact points for energy transitions
- Structure analysis and clustering
"""

__version__ = "0.1.0"
__author__ = "Information Speed Theory Research"

from .core.space import InformationSpace, EMSpace, GravitationalSpace, HypotheticalSpace
from .core.energy import Energy
from .core.constants import SPEED_OF_LIGHT, PLANCK_CONSTANT, PLANCK_LENGTH

__all__ = [
    'InformationSpace',
    'EMSpace',
    'GravitationalSpace',
    'HypotheticalSpace',
    'Energy',
    'SPEED_OF_LIGHT',
    'PLANCK_CONSTANT',
    'PLANCK_LENGTH',
]
