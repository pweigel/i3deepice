import numpy as np
import scipy.stats as st
from icecube import dataclasses

def get_t0(pulses):
    time = []
    charge = []
    for i in pulses:
        # print(i)
        for j in i[1]:
            charge.append(j.charge)
            time.append(j.time) # + np.random.randn()*1e-6) # what a fudge factor...
            
    # Now we check for pulses at the same time
    unique_times = set(time)
    new_time = []
    new_charge = []
    for t in unique_times:
        new_time.append(t)
        _charge = 0
        for idx, _t in enumerate(time):
            if t == _t:
                _charge += charge[idx] 
        new_charge.append(_charge)
    # print(np.sum(new_charge), np.sum(charge))
    return median(new_time, weights=new_charge)


def median(arr, weights=None):
    if weights is not None:
        weights = 1. * np.array(weights)
    else:
        weights = np.ones(len(arr))
    # print(len(set(arr)), len(arr))
    rv = st.rv_discrete(values=(arr, weights / weights.sum()))
    return rv.median()

def charge_after_time(charges, times, t=100):
    mask = (times - np.min(times)) < t
    return np.sum(charges[mask])


def time_of_percentage(charges, times, percentage):
    charges = charges.tolist()
    cut = np.sum(charges) / (100. / percentage)
    sum = 0
    for i in charges:
        sum = sum + i
        if sum > cut:
            tim = times[charges.index(i)]
            break
    return tim

#based on the pulses
def pulses_quantiles(charges, times, quantile):
    tot_charge = np.sum(charges)
    cut = tot_charge*quantile
    progress = 0
    for i, charge in enumerate(charges):
        progress += charge
        if progress >= cut:
            return times[i]
