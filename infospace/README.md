# InfoSpace - Python Library for Information Speed Theory

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library for simulating and computing with information spaces based on the **Information Speed Theory**.

## Overview

InfoSpace implements the seven fundamental insights of Information Speed Theory:

1. **Multiple Information Spaces** - Different I_k spaces with different Vmax_k
2. **Measurement as Projection** - v_measured = min(v_real, c)
3. **Vacuum Phase Transitions** - Energy thresholds for space transitions
4. **Universality of Formulas** - c → Vmax_k in all relativistic formulas
5. **EM Confinement** - All measurements are EM-based
6. **Contact Points** - Energy transition mechanisms with coupling g
7. **Scale Incompatibility** - λ, ρ, T determine accessibility

## Installation

```bash
# Clone the repository
cd infospace

# Install dependencies
pip install numpy scipy matplotlib

# Install in development mode
pip install -e .
```

## Quick Start

```python
from infospace import EMSpace, HypotheticalSpace, Energy
from infospace.interactions import ContactPoint
from infospace.transforms import ProjectionOperator

# Create information spaces
em_space = EMSpace()  # Standard EM space with Vmax = c
x_space = HypotheticalSpace(Vmax=10*c, lambda_scale=1e-15)

# Create contact point
contact = ContactPoint(x_space, em_space, coupling_strength=1e-38)
print(f"Transition efficiency: {contact.transition_efficiency():.2e}")

# Energy calculations
mass = 1e-27  # kg (proton mass)
energy_em = Energy(em_space)
E_em = energy_em.total_energy(mass)
print(f"Energy in I_EM: {E_em:.2e} J")

energy_x = Energy(x_space)
E_x = energy_x.total_energy(mass)
print(f"Energy in I_X: {E_x:.2e} J (factor {E_x/E_em:.1f})")

# Projection
projection = ProjectionOperator(x_space, em_space)
v_real = 5 * c  # Faster than light in I_X
v_measured = projection.project_velocity(v_real)
print(f"Real velocity: {v_real/c:.1f}c")
print(f"Measured velocity: {v_measured/c:.1f}c")
```

## Features

### Core Classes

- **InformationSpace**: Base class for all information spaces

  - `EMSpace`: Electromagnetic space (Vmax = c)
  - `GravitationalSpace`: Gravitational wave space
  - `HypotheticalSpace`: Custom I_X spaces with Vmax > c
  - `SourceSpace`: Pre-spatial I_0 space

- **Energy**: Energy calculations per carrier
  - Total energy: E = m·Vmax²
  - Relativistic energy: E² = (p·Vmax)² + (m·Vmax²)²
  - Photon energy, wavelength conversions

### Transformations

- **LorentzTransform**: Generalized Lorentz transformations

  - Coordinate transformations
  - Velocity addition
  - Momentum and energy transformations

- **ProjectionOperator**: Space-to-space projections
  - Velocity projection: v_measured = min(v_real, Vmax_target)
  - Energy projection with contact points
  - Information loss calculation

### Interactions

- **ContactPoint**: Energy transition between spaces
  - Coupling strength g
  - Scale, density, topology compatibility
  - Transition efficiency: η = g² × f*λ × f*ρ × f_T

## Examples

### LHC Energy Anomaly Simulation

```bash
python examples/lhc_simulation.py
```

Simulates particle collisions at LHC energies and detects missing energy that could indicate transition to I_X space above energy threshold.

### More Examples

- `examples/cmb_analysis.py` - CMB correlation analysis
- `examples/dark_matter.py` - Dark matter clustering simulation

## Project Structure

```
infospace/
├── __init__.py
├── core/
│   ├── space.py          # Information space classes
│   ├── energy.py         # Energy calculations
│   └── constants.py      # Physical constants
├── transforms/
│   ├── lorentz.py        # Lorentz transformations
│   └── projection.py     # Projection operators
├── interactions/
│   └── contact_point.py  # Contact point mechanics
├── examples/
│   ├── lhc_simulation.py
│   ├── cmb_analysis.py
│   └── dark_matter.py
└── tests/
    ├── test_spaces.py
    ├── test_transforms.py
    └── test_contact_points.py
```

## Theory Background

This library implements the **Information Speed Theory**, which proposes that:

- The speed of light c is not a universal limit, but specific to electromagnetic space
- Multiple information spaces exist with different maximum speeds
- All our measurements are filtered through the EM channel
- Contact points with coupling strength g enable energy transitions between spaces

For full theory documentation, see:

- [English Documentation](../en/)
- [Bulgarian Documentation](../bg/)
- [Main README](../README.md)

## Testing

```bash
pytest tests/
```

## Dependencies

- Python 3.8+
- numpy
- scipy
- matplotlib (for visualization)
- pytest (for testing)

## Contributing

This is a research project. Contributions are welcome!

## License

MIT License

## Citation

If you use this library in your research, please cite:

```
Information Speed Theory (2025)
Python Implementation: InfoSpace Library
```

## Contact

For questions or discussions, please open an issue in the repository.

---

**Made with 🧠 and ❤️ for advancing theoretical physics**
