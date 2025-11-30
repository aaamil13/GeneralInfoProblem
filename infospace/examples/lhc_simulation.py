"""
Example: LHC Energy Anomaly Simulation

Simulates particle collision at LHC energies and detects missing energy
that could indicate transition to I_X space.
"""

import numpy as np
import sys
sys.path.append('..')

from infospace import EMSpace, HypotheticalSpace, Energy
from infospace.interactions import ContactPoint


def simulate_lhc_collision(collision_energy_gev: float, 
                           threshold_energy_gev: float = 15.0,
                           vmax_x_factor: float = 10.0):
    """
    Simulate LHC collision with potential I_X transition.
    
    Args:
        collision_energy_gev: Collision energy in GeV
        threshold_energy_gev: Energy threshold for I_X transition
        vmax_x_factor: Vmax_X / c ratio
        
    Returns:
        Dictionary with simulation results
    """
    # Constants
    c = 299792458.0  # m/s
    gev_to_joules = 1.602e-10  # 1 GeV in Joules
    
    # Create spaces
    em_space = EMSpace()
    x_space = HypotheticalSpace(
        Vmax=vmax_x_factor * c,
        lambda_scale=1e-18,  # Sub-nuclear scale
        rho_density=1e35,
        name=f'I_X(Vmax={vmax_x_factor}c)'
    )
    
    # Create contact point (very weak at low energies)
    base_coupling = 1e-40
    energy_enhancement = (collision_energy_gev / threshold_energy_gev) ** 2
    effective_coupling = min(base_coupling * energy_enhancement, 1e-10)
    
    contact = ContactPoint(x_space, em_space, effective_coupling, name='LHC_Threshold')
    
    # Initial energy (all in I_EM)
    initial_energy_j = collision_energy_gev * gev_to_joules
    energy_em = Energy(em_space, initial_energy_j)
    
    # Check if above threshold
    if collision_energy_gev > threshold_energy_gev:
        # Some energy transitions to I_X
        transition_prob = 1.0 - np.exp(-(collision_energy_gev - threshold_energy_gev) / threshold_energy_gev)
        
        # Energy that transitions
        energy_to_x = initial_energy_j * transition_prob
        energy_x = Energy(x_space, energy_to_x)
        
        # Try to measure it (project back to I_EM)
        measured_energy_em = contact.energy_transition(energy_x)
        
        # Missing energy
        missing_energy = energy_to_x - measured_energy_em.carrier_energy
        missing_fraction = missing_energy / initial_energy_j
    else:
        transition_prob = 0.0
        missing_energy = 0.0
        missing_fraction = 0.0
    
    return {
        'collision_energy_gev': collision_energy_gev,
        'threshold_gev': threshold_energy_gev,
        'transition_probability': transition_prob,
        'missing_energy_gev': missing_energy / gev_to_joules,
        'missing_fraction': missing_fraction,
        'contact_efficiency': contact.transition_efficiency(),
        'effective_coupling': effective_coupling,
    }


if __name__ == '__main__':
    print("=" * 70)
    print("LHC Energy Anomaly Simulation")
    print("=" * 70)
    print()
    
    # Simulate range of energies
    energies = [5, 10, 13, 15, 17, 20, 25, 30]  # TeV
    
    print(f"{'E (TeV)':<10} {'P(transition)':<15} {'Missing E (GeV)':<18} {'Missing %':<12} {'η':<12}")
    print("-" * 70)
    
    for E_tev in energies:
        result = simulate_lhc_collision(
            collision_energy_gev=E_tev * 1000,
            threshold_energy_gev=15000,  # 15 TeV threshold
            vmax_x_factor=10.0
        )
        
        print(f"{E_tev:<10.1f} {result['transition_probability']:<15.4f} "
              f"{result['missing_energy_gev']:<18.2f} "
              f"{result['missing_fraction']*100:<12.2f} "
              f"{result['contact_efficiency']:<12.2e}")
    
    print()
    print("=" * 70)
    print("Interpretation:")
    print("- Below 15 TeV: No transition, no missing energy")
    print("- Above 15 TeV: Increasing transition probability")
    print("- Missing energy grows with collision energy")
    print("- Contact efficiency determines how much we can recover")
    print("=" * 70)
