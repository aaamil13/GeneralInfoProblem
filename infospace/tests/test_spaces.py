"""
Unit tests for information space classes.
"""

import pytest
import numpy as np
import sys
sys.path.append('..')

from infospace.core import EMSpace, GravitationalSpace, HypotheticalSpace, SourceSpace
from infospace.core.constants import SPEED_OF_LIGHT


class TestEMSpace:
    """Tests for electromagnetic space."""
    
    def test_creation(self):
        """Test EM space creation."""
        em = EMSpace()
        assert em.Vmax == SPEED_OF_LIGHT
        assert em.name == 'I_EM'
        assert em.carrier == 'photon'
    
    def test_metric(self):
        """Test spacetime metric."""
        em = EMSpace()
        # Lightlike interval: ds² = 0
        ds2 = em.metric_signature(dt=1.0, dx=SPEED_OF_LIGHT, dy=0, dz=0)
        assert abs(ds2) < 1e-6
    
    def test_causality(self):
        """Test causal connection."""
        em = EMSpace()
        # Timelike separation
        assert em.is_causal(delta_t=2.0, delta_x=SPEED_OF_LIGHT)
        # Spacelike separation
        assert not em.is_causal(delta_t=0.5, delta_x=SPEED_OF_LIGHT)
    
    def test_gamma_factor(self):
        """Test Lorentz gamma factor."""
        em = EMSpace()
        # At rest
        assert abs(em.gamma_factor(0) - 1.0) < 1e-10
        # At 0.6c
        gamma = em.gamma_factor(0.6 * SPEED_OF_LIGHT)
        expected = 1.25  # 1/√(1-0.36)
        assert abs(gamma - expected) < 0.01


class TestHypotheticalSpace:
    """Tests for hypothetical I_X spaces."""
    
    def test_creation(self):
        """Test I_X space creation."""
        x_space = HypotheticalSpace(Vmax=10*SPEED_OF_LIGHT)
        assert x_space.Vmax == 10 * SPEED_OF_LIGHT
        assert x_space.name == 'I_X'
    
    def test_invalid_vmax(self):
        """Test that Vmax must be > c."""
        with pytest.raises(ValueError):
            HypotheticalSpace(Vmax=0.5*SPEED_OF_LIGHT)
    
    def test_gamma_factor(self):
        """Test gamma factor in I_X space."""
        x_space = HypotheticalSpace(Vmax=10*SPEED_OF_LIGHT)
        # At 5c (half of Vmax_X)
        gamma = x_space.gamma_factor(5 * SPEED_OF_LIGHT)
        expected = 1.0 / np.sqrt(1 - 0.25)  # 1/√0.75
        assert abs(gamma - expected) < 0.01


class TestSourceSpace:
    """Tests for source space I_0."""
    
    def test_creation(self):
        """Test I_0 space creation."""
        i0 = SourceSpace()
        assert i0.Vmax == np.inf
        assert i0.name == 'I_0'
    
    def test_causality(self):
        """Test that all events are causal in I_0."""
        i0 = SourceSpace()
        # Any separation is causal
        assert i0.is_causal(delta_t=0.001, delta_x=1e10)


class TestSpaceComparison:
    """Tests for comparing spaces."""
    
    def test_equality(self):
        """Test space equality."""
        em1 = EMSpace()
        em2 = EMSpace()
        assert em1 == em2
    
    def test_inequality(self):
        """Test space inequality."""
        em = EMSpace()
        x = HypotheticalSpace(Vmax=10*SPEED_OF_LIGHT)
        assert em != x


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
