"""
================
sputtertarget.py
================

Code to calibrate sputter targets used in a Corona Vacuum Coders B3R. The 
main idea is to sputter using known powers for given times over weigh discs.
These discs are pre-weighed using a Satorious Microbalance, the atomic mass, 
and density is used to help estimate the relative sputter rates amongst
other sputter targets.
"""
# ISC License
#
# Copyright 2017 David Kalliecharan <dave@dal.ca>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
# OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from pylab import pi
from pandas import read_csv
import string
import yaml

__author__  = 'David Kalliecharan'
__license__ = 'ISC License'
__version__ = '0.1.0'
__status__  = 'Development'

# Constants
MG_TO_G = 1E-3
CM_TO_NM = 1E7
MIN_TO_SEC = 60
WEIGH_DISC_RADIUS_DFLT = 0.0063 # m

# Add option headers at bottom of list, and updadate OPTIONAL_HEADERS_INDEX
DATA_FILE_COLS = [ 'mass_i (mg)',
                   'mass_f (mg)',
                   'power (W)',
                   'time (min)',
                   'area (cm^2)',
]
OPTIONAL_HEADERS_INDEX = 2
OPTIONAL_HEADER_KEYS = DATA_FILE_COLS[OPTIONAL_HEADERS_INDEX:]

EXCEPTION_FORMAT = """File format incorrect!  Check header format to ensure column headers have no spaces between commas (,), and is as follows:
---
element      : Ge
atomic_mass  : 72.630 # g/mol
density      : 5.323  # g/cm^3
table_motion : stationary
date         : 2017-Oct-31
experimenter : David Kalliecharan
...
mass_i (mg), mass_f (mg), power (W), time (min), area (cm^2)
11.534, 12.432, 50, 500, 1
11.638, 12.589, 40, 400, 1
11.456, 12.359, 30, 300, 1
"""

WARNING_TABLE_MOTION = """Calbiration not specified in header!
---
table_motion : stationary|rotating
...
"""

class SputterTarget():
    def __init__(self, ifile):
        skiprows = self.__extract_header(ifile)
        self.__df = read_csv(ifile, skiprows=skiprows)
        # Strip out spaces on begining and end of columns
        self.__df.columns = self.__df.columns.str.strip()
        # Add element column
        self.__df['element'] = [self.__hdr['element']]*self.__df.shape[0]
        for key in OPTIONAL_HEADER_KEYS:
            if key not in list(self.__df.keys()):
                # Add column of repeating values for calculations
                self.__df[key] = [self.__hdr[key]]*self.__df.shape[0]
        for key in DATA_FILE_COLS:
            if key not in list(self.__df.keys()):
                raise Exception(EXCEPTION_FORMAT)
        self.__calibrate()
        return

    def __extract_header(self, ifile, begin='---', end='...'):
        begin += '\n'
        end += '\n'
        with open(ifile, 'r') as f:
            header = str()
            skiprows=0
            grab = False
            for line in f.readlines():
                if line == begin:
                    grab = not grab
                elif grab == False:
                    continue
                header += line
                skiprows += 1
                if line == end:
                    break
        if header == "":
            raise Exception(EXCEPTION_FORMAT)
        header = header.replace('\t', ' ')
        header = yaml.load(header)
        self.__hdr = header
        return skiprows

    def __calibrate(self, *args, **kws):
        """Analyzes calibration data to acquire depositon, and rates."""
        mass_diff = self.__df['mass_f (mg)'] - self.__df['mass_i (mg)']
        sputter_time = self.__df['time (min)']*MIN_TO_SEC
        mols = (mass_diff/self.__hdr['atomic_mass'])*MG_TO_G
        mols_per_sec = mols/sputter_time
        nm = (mass_diff*MG_TO_G/self.__hdr['density']/self.__df['area (cm^2)'])*CM_TO_NM
        nm_per_sec = nm/sputter_time
        self.__df['mass_diff (mg)'] = mass_diff
        self.__df['time (s)'] = sputter_time
        self.__df['mols'] = mols
        self.__df['mols/cm^2'] = self.__df['mols']/self.__df['area (cm^2)']
        self.__df['rate (mols/s)'] = mols_per_sec
        self.__df['rate (mols/s/cm^2)'] = self.__df['rate (mols/s)']/self.__df['area (cm^2)']
        self.__df['nm'] = nm
        self.__df['rate (nm/s)'] = nm_per_sec
        return

    def estimate_rotating_mask(self):
        """Only required for table_motion = 'stationary', not valid for rotating."""
        if 'table_motion' not in list(self.__hdr.keys()):
            raise Warning(WARNING_TABLE_MOTION)
        if self.__hdr['table_motion'].lower() != 'stationary':
            print('Only valid for stationary measurements')
        headers = ['rate (mols/s)', 'rate (mols/s/cm^2)', 'rate (nm/s)']
        return self.__df[headers].apply(lambda x: x/30)

    def get_dataframe(self):
        return self.__df

    def get_header(self):
        return self.__hdr['experimenter']
if __name__ == '__main__':
    pass