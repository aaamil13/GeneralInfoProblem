"""
Information Space classes.

Defines different types of information spaces with their characteristic properties.
"""

import numpy as np
from typing import Optional, Literal
from .constants import SPEED_OF_LIGHT, PLANCK_LENGTH


class InformationSpace:
    """
    Base class for information spaces.
    
    An information space I_k is characterized by:
    - Vmax: Maximum speed for information propagation
    - lambda_scale: Characteristic length scale
    - rho_density: Information density (bits/m³)
    - topology: Topology type (local/extended/global)
    - carrier: Physical carrier name
    """
    
    def __init__(
        self,
        Vmax: float,
        lambda_scale: float,
        rho_density: float,
        topology: Literal['local', 'extended', 'global'] = 'extended',
        carrier: str = 'unknown',
        name: str = 'I_X'
    ):
        """
        Initialize an information space.
        
        Args:
            Vmax: Maximum speed (m/s)
            lambda_scale: Characteristic length scale (m)
            rho_density: Information density (bits/m³)
            topology: Topology type
            carrier: Physical carrier name
            name: Space identifier
        """
        if Vmax <= 0:
            raise ValueError("Vmax must be positive")
        if lambda_scale <= 0:
            raise ValueError("lambda_scale must be positive")
        if rho_density <= 0:
            raise ValueError("rho_density must be positive")
            
        self.Vmax = Vmax
        self.lambda_scale = lambda_scale
        self.rho_density = rho_density
        self.topology = topology
        self.carrier = carrier
        self.name = name
    
    def metric_signature(self, dt: float, dx: float, dy: float, dz: float) -> float:
        """
        Calculate spacetime interval in this space.
        
        ds² = -Vmax² dt² + dx² + dy² + dz²
        
        Args:
            dt, dx, dy, dz: Coordinate differentials
            
        Returns:
            Spacetime interval ds²
        """
        return -(self.Vmax**2) * dt**2 + dx**2 + dy**2 + dz**2
    
    def is_causal(self, delta_t: float, delta_x: float) -> bool:
        """
        Check if two events are causally connected in this space.
        
        Events are causal if: Δt > Δx/Vmax
        
        Args:
            delta_t: Time separation (s)
            delta_x: Spatial separation (m)
            
        Returns:
            True if causally connected
        """
        return delta_t > delta_x / self.Vmax
    
    def gamma_factor(self, velocity: float) -> float:
        """
        Calculate Lorentz gamma factor for this space.
        
        γ = 1/√(1 - v²/Vmax²)
        
        Args:
            velocity: Velocity (m/s)
            
        Returns:
            Gamma factor
        """
        if abs(velocity) >= self.Vmax:
            raise ValueError(f"Velocity {velocity} exceeds Vmax {self.Vmax}")
        
        beta_squared = (velocity / self.Vmax) ** 2
        return 1.0 / np.sqrt(1.0 - beta_squared)
    
    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(name='{self.name}', "
                f"Vmax={self.Vmax:.2e}, λ={self.lambda_scale:.2e}, "
                f"ρ={self.rho_density:.2e})")
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, InformationSpace):
            return False
        return (np.isclose(self.Vmax, other.Vmax) and
                np.isclose(self.lambda_scale, other.lambda_scale) and
                np.isclose(self.rho_density, other.rho_density))


class EMSpace(InformationSpace):
    """
    Electromagnetic information space.
    
    The standard space we inhabit with Vmax = c.
    """
    
    def __init__(self):
        """Initialize EM space with standard parameters."""
        super().__init__(
            Vmax=SPEED_OF_LIGHT,
            lambda_scale=1e-10,  # Atomic scale (Angstrom)
            rho_density=1e29,    # ~1 bit per atom
            topology='extended',
            carrier='photon',
            name='I_EM'
        )


class GravitationalSpace(InformationSpace):
    """
    Gravitational information space.
    
    Space for gravitational wave propagation.
    Note: Vmax measured via EM, so appears to be c.
    """
    
    def __init__(self, Vmax: Optional[float] = None):
        """
        Initialize gravitational space.
        
        Args:
            Vmax: Maximum speed (defaults to c, but may be different)
        """
        if Vmax is None:
            Vmax = SPEED_OF_LIGHT  # Measured value
            
        super().__init__(
            Vmax=Vmax,
            lambda_scale=1e6,     # Kilometer scale (LIGO arm length)
            rho_density=1e-20,    # Very dilute
            topology='global',
            carrier='graviton',
            name='I_GW'
        )


class HypotheticalSpace(InformationSpace):
    """
    Hypothetical faster-than-light information space.
    
    Custom I_X space with Vmax > c.
    """
    
    def __init__(
        self,
        Vmax: float,
        lambda_scale: Optional[float] = None,
        rho_density: Optional[float] = None,
        topology: Literal['local', 'extended', 'global'] = 'extended',
        carrier: str = 'unknown',
        name: str = 'I_X'
    ):
        """
        Initialize hypothetical space.
        
        Args:
            Vmax: Maximum speed (must be > c)
            lambda_scale: Characteristic length (defaults to Planck scale)
            rho_density: Information density (defaults to 1e20)
            topology: Topology type
            carrier: Carrier name
            name: Space identifier
        """
        if Vmax <= SPEED_OF_LIGHT:
            raise ValueError(f"Hypothetical space must have Vmax > c, got {Vmax}")
        
        if lambda_scale is None:
            lambda_scale = PLANCK_LENGTH  # Default to Planck scale
        
        if rho_density is None:
            rho_density = 1e20  # Default density
            
        super().__init__(
            Vmax=Vmax,
            lambda_scale=lambda_scale,
            rho_density=rho_density,
            topology=topology,
            carrier=carrier,
            name=name
        )


class SourceSpace(InformationSpace):
    """
    Source/Origin space I_0.
    
    Pre-spatial, pre-temporal space. Theoretical construct.
    """
    
    def __init__(self):
        """Initialize source space."""
        super().__init__(
            Vmax=np.inf,  # No speed limit
            lambda_scale=PLANCK_LENGTH,
            rho_density=np.inf,  # Infinite information density
            topology='local',
            carrier='quantum_information',
            name='I_0'
        )
    
    def is_causal(self, delta_t: float, delta_x: float) -> bool:
        """All events are causally connected in I_0."""
        return True
