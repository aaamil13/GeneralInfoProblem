"""
Energy calculations for information spaces.

Energy is represented per carrier and depends on the information space.
"""

import numpy as np
from typing import Optional
from .constants import HBAR, SPEED_OF_LIGHT


class Energy:
    """
    Energy in an information space.
    
    Energy is calculated based on the carrier and the space's Vmax:
    - For I_EM: E = ℏω (photon energy)
    - For general I_k: E = m·Vmax_k²
    """
    
    def __init__(self, space: 'InformationSpace', carrier_energy: Optional[float] = None):
        """
        Initialize energy in a given space.
        
        Args:
            space: Information space
            carrier_energy: Energy per carrier (J), optional
        """
        from .space import InformationSpace
        
        if not isinstance(space, InformationSpace):
            raise TypeError("space must be an InformationSpace instance")
            
        self.space = space
        self.carrier_energy = carrier_energy
    
    def total_energy(self, mass: float) -> float:
        """
        Calculate total energy for a given mass.
        
        E = m·Vmax²
        
        Args:
            mass: Mass (kg)
            
        Returns:
            Total energy (J)
        """
        return mass * self.space.Vmax ** 2
    
    def relativistic_energy(self, momentum: float, mass: float) -> float:
        """
        Calculate relativistic energy.
        
        E² = (p·Vmax)² + (m·Vmax²)²
        
        Args:
            momentum: Momentum (kg·m/s)
            mass: Rest mass (kg)
            
        Returns:
            Total relativistic energy (J)
        """
        p_term = (momentum * self.space.Vmax) ** 2
        m_term = (mass * self.space.Vmax ** 2) ** 2
        return np.sqrt(p_term + m_term)
    
    def kinetic_energy(self, velocity: float, mass: float) -> float:
        """
        Calculate kinetic energy.
        
        K = (γ - 1)·m·Vmax²
        
        Args:
            velocity: Velocity (m/s)
            mass: Mass (kg)
            
        Returns:
            Kinetic energy (J)
        """
        gamma = self.space.gamma_factor(velocity)
        return (gamma - 1) * mass * self.space.Vmax ** 2
    
    def photon_energy(self, frequency: float) -> float:
        """
        Calculate photon energy (for EM space).
        
        E = ℏω = h·f
        
        Args:
            frequency: Frequency (Hz)
            
        Returns:
            Photon energy (J)
        """
        return HBAR * 2 * np.pi * frequency
    
    def photon_frequency(self, energy: float) -> float:
        """
        Calculate photon frequency from energy.
        
        f = E/h
        
        Args:
            energy: Energy (J)
            
        Returns:
            Frequency (Hz)
        """
        return energy / (HBAR * 2 * np.pi)
    
    def wavelength_to_energy(self, wavelength: float) -> float:
        """
        Convert wavelength to energy (for EM space).
        
        E = h·c/λ
        
        Args:
            wavelength: Wavelength (m)
            
        Returns:
            Energy (J)
        """
        return HBAR * 2 * np.pi * SPEED_OF_LIGHT / wavelength
    
    def energy_to_wavelength(self, energy: float) -> float:
        """
        Convert energy to wavelength (for EM space).
        
        λ = h·c/E
        
        Args:
            energy: Energy (J)
            
        Returns:
            Wavelength (m)
        """
        return HBAR * 2 * np.pi * SPEED_OF_LIGHT / energy
    
    def binding_energy_ratio(self, other_space: 'InformationSpace') -> float:
        """
        Calculate ratio of binding energies in different spaces.
        
        E_k / E_EM = (Vmax_k / c)²
        
        Args:
            other_space: Other information space
            
        Returns:
            Energy ratio
        """
        return (other_space.Vmax / self.space.Vmax) ** 2
    
    def __repr__(self) -> str:
        if self.carrier_energy is not None:
            return f"Energy(space={self.space.name}, E={self.carrier_energy:.2e} J)"
        else:
            return f"Energy(space={self.space.name})"
    
    def __mul__(self, scalar: float) -> 'Energy':
        """Multiply energy by scalar."""
        if self.carrier_energy is None:
            raise ValueError("Cannot multiply energy without carrier_energy set")
        return Energy(self.space, self.carrier_energy * scalar)
    
    def __rmul__(self, scalar: float) -> 'Energy':
        """Right multiplication."""
        return self.__mul__(scalar)
    
    def __add__(self, other: 'Energy') -> 'Energy':
        """Add energies (must be in same space)."""
        if self.space != other.space:
            raise ValueError("Cannot add energies from different spaces")
        if self.carrier_energy is None or other.carrier_energy is None:
            raise ValueError("Cannot add energies without carrier_energy set")
        return Energy(self.space, self.carrier_energy + other.carrier_energy)
