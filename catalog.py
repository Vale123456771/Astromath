SOLAR_MASS = 1.98847e30
SOLAR_LUMINOSITY = 3.828e26
SOURCE = 'NASA Planetary Fact Sheet (valores aproximados; verificar antes de uso científico)'
# Parámetros aproximados para actividades didácticas; no son efemérides en tiempo real.
rows = [
 ('Mercurio',3.3011e23,2439.7,5.43,.387,87.97,3.7),
 ('Venus',4.8675e24,6051.8,5.24,.723,224.70,8.87),
 ('Tierra',5.97237e24,6371.0,5.51,1.0,365.256,9.81),
 ('Marte',6.4171e23,3389.5,3.93,1.524,686.98,3.71),
 ('Júpiter',1.8982e27,69911,1.33,5.204,4332.59,24.79),
 ('Saturno',5.6834e26,58232,.69,9.583,10759.22,10.44),
 ('Urano',8.6810e25,25362,1.27,19.191,30688.5,8.69),
 ('Neptuno',1.02413e26,24622,1.64,30.07,60182,11.15),
]
PLANETS = {name.lower(): dict(name=name,mass_kg=mass,mean_radius_km=radius,density_g_cm3=density,semi_major_axis_au=axis,orbital_period_days=period,surface_gravity_m_s2=gravity,source=SOURCE) for name,mass,radius,density,axis,period,gravity in rows}
STARS = {
 'sun': dict(name='Sol',luminosity_watts=SOLAR_LUMINOSITY,mass_kg=SOLAR_MASS,effective_temp_k=5772,radius_km=695700,spectral_type='G2V',source='IAU nominal solar constants (aproximaciones)'),
 'vega': dict(name='Vega',luminosity_watts=40.12*SOLAR_LUMINOSITY,mass_kg=2.135*SOLAR_MASS,effective_temp_k=9600,radius_km=2.362*695700,spectral_type='A0V',source='Valores aproximados de literatura; Vega rota rápidamente y los parámetros dependen del modelo')
}
