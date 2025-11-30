"""
Contact points between information spaces.

Implements energy transition mechanisms with coupling strength.
"""

import numpy as np


class ContactPoint:
    """
    Contact point between two information spaces.
    
    A physical system that "lives" in both spaces and facilitates
    energy transition: E_X → [Contact Point] → E_EM
    """
    
    def __init__(self, 
                 space_x: 'InformationSpace',
                 space_em: 'InformationSpace',
                 coupling_strength: float,
                 name: str = 'contact'):
        """
        Initialize contact point.
        
        Args:
            space_x: Source information space
            space_em: Target information space (usually I_EM)
            coupling_strength: Coupling constant g
            name: Contact point identifier
        """
        from ..core.space import InformationSpace
        
        if not isinstance(space_x, InformationSpace):
            raise TypeError("space_x must be an InformationSpace instance")
        if not isinstance(space_em, InformationSpace):
            raise TypeError("space_em must be an InformationSpace instance")
        
        if not (0 <= coupling_strength <= 1):
            raise ValueError("Coupling strength must be in [0, 1]")
            
        self.space_x = space_x
        self.space_em = space_em
        self.g = coupling_strength
        self.name = name
    
    def scale_compatibility(self) -> float:
        """
        Calculate scale compatibility factor.
        
        f_λ = exp(-Δλ / λ_ref)
        
        Returns:
            Scale compatibility (0 to 1)
        """
        delta_lambda = abs(self.space_x.lambda_scale - self.space_em.lambda_scale)
        lambda_ref = min(self.space_x.lambda_scale, self.space_em.lambda_scale)
        
        if lambda_ref == 0:
            return 0.0
        
        return np.exp(-delta_lambda / lambda_ref)
    
    def density_compatibility(self) -> float:
        """
        Calculate density compatibility factor.
        
        f_ρ = exp(-|log(ρ_X/ρ_EM)|)
        
        Returns:
            Density compatibility (0 to 1)
        """
        if self.space_em.rho_density == 0 or not np.isfinite(self.space_x.rho_density):
            return 0.0
        
        ratio = self.space_x.rho_density / self.space_em.rho_density
        
        if ratio <= 0 or not np.isfinite(ratio):
            return 0.0
        
        return np.exp(-abs(np.log(ratio)))
    
    def topology_compatibility(self) -> float:
        """
        Calculate topology compatibility factor.
        
        Returns:
            Topology compatibility (0 to 1)
        """
        # Simple model: same topology = 1, different = 0.1
        if self.space_x.topology == self.space_em.topology:
            return 1.0
        else:
            return 0.1
    
    def transition_efficiency(self) -> float:
        """
        Calculate total transition efficiency.
        
        η = g² × f_λ × f_ρ × f_T
        
        Returns:
            Efficiency (0 to 1)
        """
        scale_compat = self.scale_compatibility()
        density_compat = self.density_compatibility()
        topology_compat = self.topology_compatibility()
        
        return (self.g ** 2) * scale_compat * density_compat * topology_compat
    
    def energy_transition(self, energy_x: 'Energy') -> 'Energy':
        """
        Transition energy from I_X to I_EM.
        
        E_EM = η × E_X
        
        Args:
            energy_x: Energy in source space
            
        Returns:
            Energy in target space
        """
        from ..core.energy import Energy
        
        if energy_x.space != self.space_x:
            raise ValueError("Energy must be in source space")
        
        if energy_x.carrier_energy is None:
            raise ValueError("Energy must have carrier_energy set")
        
        eta = self.transition_efficiency()
        converted_energy = energy_x.carrier_energy * eta
        
        return Energy(self.space_em, converted_energy)
    
    def effective_coupling(self, energy: float) -> float:
        """
        Calculate effective coupling at given energy.
        
        Some contact points may have energy-dependent coupling.
        
        Args:
            energy: Energy scale (J)
            
        Returns:
            Effective coupling strength
        """
        # For now, constant coupling
        # Could add energy dependence: g_eff(E) = g_0 × (E/Λ)^n
        return self.g
    
    def __repr__(self) -> str:
        eta = self.transition_efficiency()
        return (f"ContactPoint('{self.name}': {self.space_x.name} → {self.space_em.name}, "
                f"g={self.g:.2e}, η={eta:.2e})")


# Predefined contact points
def create_ligo_contact_point(space_gw: 'InformationSpace', 
                              space_em: 'InformationSpace') -> ContactPoint:
    """
    Create LIGO-like contact point for gravitational waves.
    
    Args:
        space_gw: Gravitational wave space
        space_em: EM space
        
    Returns:
        Contact point with g ~ 10^-20
    """
    return ContactPoint(space_gw, space_em, 
                       coupling_strength=1e-20,
                       name='LIGO')


def create_neutrino_contact_point(space_weak: 'InformationSpace',
                                  space_em: 'InformationSpace') -> ContactPoint:
    """
    Create neutrino detector contact point.
    
    Args:
        space_weak: Weak interaction space
        space_em: EM space
        
    Returns:
        Contact point with g ~ 10^-5
    """
    return ContactPoint(space_weak, space_em,
                       coupling_strength=1e-5,
                       name='Neutrino_Detector')


def create_dark_matter_contact_point(space_dark: 'InformationSpace',
                                     space_em: 'InformationSpace') -> ContactPoint:
    """
    Create hypothetical dark matter contact point.
    
    Args:
        space_dark: Dark matter space
        space_em: EM space
        
    Returns:
        Contact point with g ~ 10^-45
    """
    return ContactPoint(space_dark, space_em,
                       coupling_strength=1e-45,
                       name='Dark_Matter')
