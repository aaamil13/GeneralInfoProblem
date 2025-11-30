"""
Lorentz transformations for information spaces.

Generalized Lorentz transformations with Vmax as parameter.
"""

import numpy as np
from typing import Tuple


class LorentzTransform:
    """
    Lorentz transformation in an information space.
    
    Transforms coordinates between frames moving with velocity v:
    x' = γ(x - vt)
    t' = γ(t - vx/Vmax²)
    
    where γ = 1/√(1 - v²/Vmax²)
    """
    
    def __init__(self, space: 'InformationSpace', velocity: float):
        """
        Initialize Lorentz transformation.
        
        Args:
            space: Information space
            velocity: Relative velocity between frames (m/s)
        """
        from ..core.space import InformationSpace
        
        if not isinstance(space, InformationSpace):
            raise TypeError("space must be an InformationSpace instance")
        
        if abs(velocity) >= space.Vmax:
            raise ValueError(f"Velocity {velocity} must be < Vmax {space.Vmax}")
            
        self.space = space
        self.v = velocity
        self.gamma = space.gamma_factor(velocity)
        self.beta = velocity / space.Vmax
    
    def transform_position(self, x: float, t: float) -> Tuple[float, float]:
        """
        Transform position coordinates.
        
        Args:
            x: Position in original frame (m)
            t: Time in original frame (s)
            
        Returns:
            (x', t') in transformed frame
        """
        x_prime = self.gamma * (x - self.v * t)
        t_prime = self.gamma * (t - self.v * x / self.space.Vmax**2)
        return x_prime, t_prime
    
    def transform_velocity(self, u: float) -> float:
        """
        Transform velocity using velocity addition formula.
        
        u' = (u - v) / (1 - uv/Vmax²)
        
        Args:
            u: Velocity in original frame (m/s)
            
        Returns:
            Velocity in transformed frame (m/s)
        """
        numerator = u - self.v
        denominator = 1 - (u * self.v) / self.space.Vmax**2
        return numerator / denominator
    
    def transform_momentum(self, p: float, E: float) -> Tuple[float, float]:
        """
        Transform momentum and energy.
        
        p' = γ(p - vE/Vmax²)
        E' = γ(E - vp)
        
        Args:
            p: Momentum in original frame (kg·m/s)
            E: Energy in original frame (J)
            
        Returns:
            (p', E') in transformed frame
        """
        p_prime = self.gamma * (p - self.v * E / self.space.Vmax**2)
        E_prime = self.gamma * (E - self.v * p)
        return p_prime, E_prime
    
    def inverse(self) -> 'LorentzTransform':
        """
        Get inverse transformation.
        
        Returns:
            Lorentz transform with -v
        """
        return LorentzTransform(self.space, -self.v)
    
    def __repr__(self) -> str:
        return f"LorentzTransform(space={self.space.name}, v={self.v:.2e}, γ={self.gamma:.4f})"


def compose_transforms(transform1: LorentzTransform, 
                       transform2: LorentzTransform) -> LorentzTransform:
    """
    Compose two Lorentz transformations.
    
    Args:
        transform1: First transformation
        transform2: Second transformation
        
    Returns:
        Composed transformation
    """
    if transform1.space != transform2.space:
        raise ValueError("Transforms must be in the same space")
    
    # Velocity addition formula
    v1 = transform1.v
    v2 = transform2.v
    Vmax = transform1.space.Vmax
    
    v_total = (v1 + v2) / (1 + v1 * v2 / Vmax**2)
    
    return LorentzTransform(transform1.space, v_total)
