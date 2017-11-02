from pandas import read_csv
from sputtertarget import SputterTarget
import seaborn as sns
import pandas as pd
import pylab as pl

Ge = SputterTarget('example.dat')
Mn = SputterTarget('Mn_2017oct28.txt')

frames = [ Mn.get_dataframe(), 
           Ge.get_dataframe()
]
df = pd.concat(frames)

print(Ge.get_experimenter)
print(df)

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
