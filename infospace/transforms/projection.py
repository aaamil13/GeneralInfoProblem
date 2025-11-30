"""
Projection operators between information spaces.

Projects phenomena from one space to another, implementing the measurement filter.
"""

import numpy as np
from typing import Optional


class ProjectionOperator:
    """
    Projection operator from source space to target space.
    
    Implements the fundamental measurement filter:
    v_measured = min(v_real, Vmax_target)
    """
    
    def __init__(self, source_space: 'InformationSpace', 
                 target_space: 'InformationSpace'):
        """
        Initialize projection operator.
        
        Args:
            source_space: Source information space
            target_space: Target information space (usually I_EM)
        """
        from ..core.space import InformationSpace
        
        if not isinstance(source_space, InformationSpace):
            raise TypeError("source_space must be an InformationSpace instance")
        if not isinstance(target_space, InformationSpace):
            raise TypeError("target_space must be an InformationSpace instance")
            
        self.source = source_space
        self.target = target_space
    
    def project_velocity(self, v_real: float) -> float:
        """
        Project velocity from source to target space.
        
        v_measured = min(v_real, Vmax_target)
        
        Args:
            v_real: Real velocity in source space (m/s)
            
        Returns:
            Measured velocity in target space (m/s)
        """
        return min(abs(v_real), self.target.Vmax) * np.sign(v_real)
    
    def information_loss(self, v_real: float) -> float:
        """
        Calculate information loss in projection.
        
        If v_real > Vmax_target, information is lost.
        
        Args:
            v_real: Real velocity (m/s)
            
        Returns:
            Information loss factor (0 = no loss, 1 = complete loss)
        """
        if abs(v_real) <= self.target.Vmax:
            return 0.0
        else:
            # Information about true speed is lost
            return 1.0 - self.target.Vmax / abs(v_real)
    
    def project_energy(self, energy_source: 'Energy', 
                      contact_point: Optional['ContactPoint'] = None) -> 'Energy':
        """
        Project energy from source to target space.
        
        Requires a contact point for energy conversion.
        
        Args:
            energy_source: Energy in source space
            contact_point: Contact point for transition (optional)
            
        Returns:
            Energy in target space
        """
        from ..core.energy import Energy
        
        if energy_source.space != self.source:
            raise ValueError("Energy must be in source space")
        
        if contact_point is None:
            # No contact point - assume perfect projection
            efficiency = 1.0
        else:
            # Use contact point efficiency
            efficiency = contact_point.transition_efficiency()
        
        # Convert energy
        if energy_source.carrier_energy is None:
            return Energy(self.target, None)
        
        converted_energy = energy_source.carrier_energy * efficiency
        return Energy(self.target, converted_energy)
    
    def is_observable(self, phenomenon_scale: float) -> bool:
        """
        Check if phenomenon at given scale is observable in target space.
        
        Args:
            phenomenon_scale: Characteristic scale of phenomenon (m)
            
        Returns:
            True if observable
        """
        # Phenomenon must be compatible with target space scale
        scale_ratio = abs(np.log10(phenomenon_scale / self.target.lambda_scale))
        
        # Observable if within ~5 orders of magnitude
        return scale_ratio < 5.0
    
    def projection_matrix(self, dimensions: int = 4) -> np.ndarray:
        """
        Get projection matrix for spacetime coordinates.
        
        Args:
            dimensions: Number of spacetime dimensions (default 4)
            
        Returns:
            Projection matrix
        """
        # For now, simple identity with velocity limit
        matrix = np.eye(dimensions)
        
        # Scale time dimension by Vmax ratio
        if self.source.Vmax != self.target.Vmax:
            matrix[0, 0] = self.target.Vmax / self.source.Vmax
        
        return matrix
    
    def __repr__(self) -> str:
        return f"ProjectionOperator({self.source.name} → {self.target.name})"
