"""
Physical constants used throughout the library.
All values in SI units.
"""

import numpy as np

# Speed of light in vacuum (m/s)
SPEED_OF_LIGHT = 299792458.0  # Exact value

# Planck constant (J·s)
PLANCK_CONSTANT = 6.62607015e-34  # Exact value

# Reduced Planck constant (J·s)
HBAR = PLANCK_CONSTANT / (2 * np.pi)

# Planck length (m)
PLANCK_LENGTH = 1.616255e-35

# Planck energy (J)
PLANCK_ENERGY = 1.956e9  # GeV in Joules: 1.956e9 * 1.602e-10

# Planck time (s)
PLANCK_TIME = 5.391e-44

# Gravitational constant (m³/kg·s²)
GRAVITATIONAL_CONSTANT = 6.67430e-11

# Elementary charge (C)
ELEMENTARY_CHARGE = 1.602176634e-19  # Exact value

# Fine structure constant (dimensionless)
FINE_STRUCTURE_CONSTANT = 7.2973525693e-3  # ≈ 1/137

# Electron mass (kg)
ELECTRON_MASS = 9.1093837015e-31

# Proton mass (kg)
PROTON_MASS = 1.67262192369e-27

# Conversion factors
EV_TO_JOULES = ELEMENTARY_CHARGE
GEV_TO_JOULES = 1e9 * EV_TO_JOULES
JOULES_TO_EV = 1.0 / EV_TO_JOULES
JOULES_TO_GEV = 1.0 / GEV_TO_JOULES
