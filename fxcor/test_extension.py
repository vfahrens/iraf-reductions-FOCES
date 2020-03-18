from astroquery.simbad import Simbad
from astropy import io

result_table = Simbad.query_object('ups And')
print(result_table)
print(result_table['DEC'][0])
# RA =