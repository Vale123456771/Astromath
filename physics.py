import math
from typing import Any

G = 6.67430e-11
AU = 1.495978707e11
DAY = 86400.0


def simulate_orbit(central_mass: float, x0: float, y0: float, vx0: float, vy0: float, total_time: float, dt: float) -> dict[str, Any]:
    vals = (central_mass, x0, y0, vx0, vy0, total_time, dt)
    if not all(math.isfinite(v) for v in vals):
        raise ValueError('Todos los parámetros deben ser finitos.')
    if central_mass <= 0 or total_time <= 0 or dt <= 0:
        raise ValueError('Masa, tiempo total y paso temporal deben ser positivos.')
    if math.hypot(x0, y0) <= 0:
        raise ValueError('La posición inicial no puede coincidir con el centro.')
    n = math.ceil(total_time / dt)
    if n > 20000:
        raise ValueError('Demasiados pasos (máximo 20000). Aumenta dt o reduce el tiempo.')
    if n < 2:
        raise ValueError('Se requieren al menos dos pasos.')
    mu = G * central_mass
    def derivative(s):
        x, y, vx, vy = s
        r2 = x*x + y*y
        if r2 < 1.0:
            raise ValueError('El cuerpo se acercó demasiado al centro; detén la integración.')
        factor = -mu / (r2 ** 1.5)
        return (vx, vy, factor*x, factor*y)
    def add(s, k, factor):
        return tuple(a + factor*b for a, b in zip(s, k))
    def point(s, t):
        x, y, vx, vy = s
        r = math.hypot(x, y)
        v = math.hypot(vx, vy)
        return {'t': t, 'x': x, 'y': y, 'vx': vx, 'vy': vy, 'r': r, 'v': v,
                'specific_energy': 0.5*v*v - mu/r}
    s = (x0, y0, vx0, vy0)
    energy0 = point(s, 0)['specific_energy']
    trajectory = [point(s, 0.0)]
    max_energy_delta = 0.0
    for i in range(n):
        h = min(dt, total_time - i*dt)
        k1 = derivative(s)
        k2 = derivative(add(s, k1, h/2))
        k3 = derivative(add(s, k2, h/2))
        k4 = derivative(add(s, k3, h))
        s = tuple(s[j] + h*(k1[j]+2*k2[j]+2*k3[j]+k4[j])/6 for j in range(4))
        if not all(math.isfinite(v) for v in s):
            raise ValueError('Integración inestable. Reduce el paso temporal.')
        p = point(s, min((i+1)*dt, total_time))
        trajectory.append(p)
        max_energy_delta = max(max_energy_delta, abs(p['specific_energy']-energy0))
    angular_momentum = x0*vy0-y0*vx0
    eccentricity = math.sqrt(max(0.0, 1 + 2*energy0*angular_momentum**2/mu**2))
    period = 2*math.pi*mu/(-2*energy0)**1.5 if energy0 < 0 else None
    return {'trajectory': trajectory, 'eccentricity': eccentricity, 'period_estimate': period,
            'conservation_error': max_energy_delta/max(abs(energy0), 1.0),
            'orbit_type': 'elliptic' if eccentricity < 1-1e-7 else ('hyperbolic' if eccentricity > 1+1e-7 else 'parabolic'),
            'model': 'Keplerian two-body approximation: central body fixed; test particle mass negligible',
            'method': 'RK4 fixed step'}
