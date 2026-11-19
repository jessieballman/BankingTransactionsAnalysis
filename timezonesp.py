import pandas as pd
from sqlalchemy import create_engine
engine = create_engine(
    'postgresql+psycopg://USER:PASSWORD@localhost:5432/bankstrans'
)

query = """
SELECT DISTINCT country,city FROM customers
"""

# timezones.py
time_zone = {
    ('US', 'Austin'): 'America/Chicago',
    ('FR', 'Montpellier'): 'Europe/Paris',
    ('NZ', 'Dunedin'): 'Pacific/Auckland',
    ('US', 'Columbus'): 'America/New_York',
    ('NL', 'Utrecht'): 'Europe/Amsterdam',
    ('SI', 'Ljubljana'): 'Europe/Ljubljana',
    ('AU', 'Perth'): 'Australia/Perth',
    ('FR', 'Nantes'): 'Europe/Paris',
    ('NL', 'Groningen'): 'Europe/Amsterdam',
    ('GB', 'Manchester'): 'Europe/London',
    ('US', 'Tucson'): 'America/Phoenix',
    ('NO', 'Bergen'): 'Europe/Oslo',
    ('IE', 'Galway'): 'Europe/Dublin',
    ('DE', 'Leipzig'): 'Europe/Berlin',
    ('DE', 'Freiburg'): 'Europe/Berlin',
    ('CA', 'Halifax'): 'America/Halifax',
    ('GB', 'Bristol'): 'Europe/London',
    ('AU', 'Hobart'): 'Australia/Hobart',
    ('CA', 'Victoria'): 'America/Vancouver',
    ('US', 'Denver'): 'America/Denver',
    ('GB', 'Sheffield'): 'Europe/London',
    ('US', 'Raleigh'): 'America/New_York',
    ('AU', 'Adelaide'): 'Australia/Adelaide',
    ('GB', 'Norwich'): 'Europe/London',
    ('ES', 'Valencia'): 'Europe/Madrid',
    ('IT', 'Bologna'): 'Europe/Rome',
    ('SE', 'Uppsala'): 'Europe/Stockholm',
    ('IE', 'Cork'): 'Europe/Dublin',
    ('NZ', 'Auckland'): 'Pacific/Auckland',
    ('CA', 'Toronto'): 'America/Toronto',
    ('PT', 'Porto'): 'Europe/Lisbon',
    ('DK', 'Aarhus'): 'Europe/Copenhagen',
    ('US', 'Portland'): 'America/Los_Angeles',
    ('FI', 'Tampere'): 'Europe/Helsinki',
}

country_city = pd.read_sql(query, engine)
country_city['both'] = list(zip(country_city['country'], country_city['city']))
country_city['timezone'] = country_city['both'].map(time_zone)
country_city = country_city[['country','city','timezone']]
country_city.to_sql(
    name='timezones',
    con=engine,
    index=False
)