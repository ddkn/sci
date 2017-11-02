from pandas import read_csv
from sputtertarget import SputterTarget
import seaborn as sns
import pandas as pd
import pylab as pl

Ge = SputterTarget('../misc/sputtertarget_example.dat')
Mn = SputterTarget('../../calibrate/Mn_2017oct28.txt')

frames = [ Mn.get_dataframe(), 
           Ge.get_dataframe()
]
df = pd.concat(frames)

for k, v in Ge.get_header().items():
    print('{key}: {val}'.format(key=k, val=v))
print('='*72)
print(df)

# How to estimate rotating table, see the new columns
Mn_df = pd.concat([Mn.get_dataframe(), Mn.get_rotating_table_estimate(),], 
                  axis=1)

print('='*72)
print(Mn_df)

pl.style.use('physrev')

pl.figure()
sns.regplot('power (W)', 'rate (mols/s/cm^2)', data=Ge.get_dataframe(),	
            ci=None,
            label='Ge',)
            
sns.regplot('power (W)', 'rate (mols/s/cm^2)', data=Mn.get_dataframe(), 
            label='Mn', 
            ci=None,)
pl.legend(loc='best')
pl.grid(True)

pl.show()
