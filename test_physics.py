import math
import pytest
from backend.physics import simulate_orbit, G, AU

def test_earth_like_orbit():
    mass = 1.98847e30
    velocity = math.sqrt(G*mass/AU)
    result = simulate_orbit(mass, AU, 0, 0, velocity, 365.256*86400, 3600)
    assert abs(result['eccentricity']) < 2e-8
    assert result['conservation_error'] < 1e-7
    assert abs(result['trajectory'][-1]['r']/AU - 1) < 1e-4

def test_invalid_steps():
    with pytest.raises(ValueError):
        simulate_orbit(1e30, AU, 0, 0, 30000, 365*86400, 1)
