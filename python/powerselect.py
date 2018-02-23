"""
============
Power Select
============

Plots calibration data for sputter targets, with desired power values
indicated by vlines for a Inverse Heusler Alloy X2YZ, where X, Y, and Z
are elements of the periodic table. It also shows dotted lines for a
linear estimate of values outside of the calibrted range.
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

from sputtertarget import SputterTarget
import pylab as pl
from itertools import cycle

__author__  = 'David Kalliecharan'
__license__ = 'ISC License'
__version__ = '0.1.0'
__status__  = 'Development'

MAX_POWER = 80 # Watts
MARKER_LST = ['o', 's', '^', 'D', 'v', '<', '>', '8', 'p', '*']
COLOR_LST = [str('C{}'.format(x)) for x in range(10)]
LIN_50_100_MSK_SCALE = 1.2

def get_elem(target):
    return target.get_header()['element']

if __name__ == '__main__':

    tgt = [ SputterTarget("../data/calibration/Ge/Ge_Stat_Cal_Si_Square.dat"),
            SputterTarget("../data/calibration/Mn/Mn_Stat_Cal_Cu_Disk_35_65.dat"),
            SputterTarget("../data/calibration/Mn/Mn_Stat_Cal_Si_square_30_70.dat"),
            SputterTarget("../data/calibration/Ni/Ni_Stat_Cal_Si_Square.dat"),
            SputterTarget("../data/calibration/Co/Co_Stat_Cal_Si_Square.dat"),
            SputterTarget("../data/calibration/Co/Co_Stat_Cal_Si_Square_0.070in_thick.dat"),
    ]

    print('Select the target X for the inverse heusler alloy X2YZ')
    for i, t in enumerate(tgt):
        print('{n}) {elem} ({date})'.format(n=i, elem=get_elem(t),
                                            date=t.get_header()['date']))

    x = -1
    while x not in range(len(tgt)):
        x = input('Choose one of the above options [0-{}]: '.format(len(tgt)-1))
        try:
            x = int(x)
        except ValueError:
            x = -1
    # Set the X target to the first element
    #x_tgt = tgt.pop(x)
    #tgt.insert(0, x_tgt)

    print('Select the max operating power for the  {} target'.format(get_elem(tgt[x])))
    p = -1
    while p not in range(MAX_POWER):
        p = input('Choose one of the above options [0-{}]: '.format(MAX_POWER))
        try:
            p = int(p)
        except ValueError:
            p = -1
    print('And select the target Y for the inverse heusler alloy X2YZ')
    for i, t in enumerate(tgt):
        print('{n}) {elem} ({date})'.format(n=i, elem=get_elem(t),
                                            date=t.get_header()['date']))
    y = -1
    while y not in range(len(tgt)):
        y = input('Choose one of the above options [0-{}]: '.format(len(tgt)-1))
        try:
            y = int(y)
        except ValueError:
            y = -1

    print('Finally select the target Z for the inverse heusler alloy X2YZ')
    for i, t in enumerate(tgt):
        print('{n}) {elem} ({date})'.format(n=i, elem=get_elem(t),
                                            date=t.get_header()['date']))
    z = -1
    while z not in range(len(tgt)):
        z = input('Choose one of the above options [0-{}]: '.format(len(tgt)-1))
        try:
            z = int(z)
        except ValueError:
            z = -1

    inv_heusler = [tgt[i] for i in (x, y, z)]
    # Plot the calibration data
    marker = cycle(MARKER_LST[:len(tgt)])
    color = cycle(COLOR_LST[:len(tgt)])
    pl.figure()
    power_vals = []
    for t in inv_heusler:
        col = next(color)
        df = t.get_dataframe()

        power = df['power (W)']
        rate = df['rate (mols/s/cm^2)']
        elem = get_elem(t)
        pl.plot(power, rate, label=elem,
                linestyle='', marker=next(marker), color=col)

        m, yint, _, _, _ = t.get_linregress()
        power_est = pl.linspace(0, MAX_POWER) # Watts
        pl.plot(power_est, power_est*m + yint, linestyle='--', color=col, label='')
        pl.plot(power, power*m + yint, linestyle='-', color=col, label='')

        # Plot rate estimates
        if elem == get_elem(tgt[x]):
            xmin, xmax = pl.xlim()
            ymin, ymax = pl.ylim()
            pl.ylim(ymin, ymax)
            pl.xlim(xmin, xmax)
            x_rate = m*p + yint
            print('\nRates')
            print('='*5)
            print('X   rate: {:0.6e} mols/s/cm^2'.format(x_rate))
            pl.hlines(x_rate, xmin, xmax, color='m', label='X = Linear or Const.')

            yz_rate = x_rate/2
            yz_rate_scaled = yz_rate*LIN_50_100_MSK_SCALE
            print('Y|Z rate: {:0.6e} mols/s/cm^2'.format(yz_rate_scaled))
            pl.hlines(yz_rate, xmin, xmax, color='c', linestyle='-', label='const. (X=const.)')
            pl.hlines(yz_rate_scaled, xmin, xmax, color='c', linestyle=':', label='const (X=Linear)')

        try:
            power_vals.append((yz_rate - yint)/m)
        except:
            pass

    rate_setting = [yz_rate]*len(inv_heusler)
    rate_setting[0] = x_rate
    power_vals[0] = p

    print("\nPowers\n=====")
    for t, pv in zip(inv_heusler, power_vals):
        print(get_elem(t), ':', '{:0.2f}'.format(pv), 'W')

    pl.vlines(power_vals, 0, rate_setting)

    pl.minorticks_on()
    pl.xlabel('Power (W)')
    pl.ylabel('Depostion rate (mols/s/cm$^{{2}}$)')
    pl.legend()
    pl.grid(True)

    ymin, ymax = pl.ylim()
    pl.ylim((0, ymax))

    pl.show()
