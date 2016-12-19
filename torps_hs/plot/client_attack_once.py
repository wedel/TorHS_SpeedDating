import os
import cPickle as pickle
import sys
import numpy as np
from numpy import ma
# from ggplot import *
# import pandas as pd
import matplotlib
matplotlib.use('PDF') # alerts matplotlib that display not required
import matplotlib.pyplot
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
from matplotlib.ticker import FixedFormatter, FixedLocator
import matplotlib.cm as cm
import math
from scipy.interpolate import spline
from itertools import cycle
import pylab
import collections
from collections import Counter
import scipy as sp
import scipy.stats
from datetime import datetime, timedelta, time, date
import pylab as pl

##### Plotting functions #####
## helper - cumulative fraction for y axis
def cf(d): return np.arange(1.0,float(len(d))+1.0)/float(len(d))

## helper - return step-based CDF x and y values
## only show to the 99th percentile by default
def getcdf(data, shownpercentile=0.99):
    data.sort()
    frac = cf(data)
    print("len(data)", len(data), "len(cf(data)):", len(frac))
    x, y, lasty = [0], [0], 0.0
    for i in xrange(int(round(len(data)*shownpercentile))):
        x.append(data[i])
        # y.append(lasty)
        # x.append(data[i])
        y.append(frac[i])
        # lasty = frac[i]
    return (x, y)

def find_nearest(array, values):
    indices = np.abs(np.subtract.outer(array, values)).argmin(0)
    return array[indices], indices


def plot_cdf(stats, out_pathname, legend_x):

    # color=iter(matplotlib.cm.Set1(np.linspace(0,0.5,len(stats.keys()))))
    colors=iter(['red','black','red','black'])
    print("len(stats)=%d"%(len(stats)))
    x_max = 0
    matplotlib.rcParams['xtick.labelsize'] = 20
    matplotlib.rcParams['ytick.labelsize'] = 20

    if len(stats)==2:
        folge = ['Vanilla', 'Gekuerzt'] #['Einfach', 'Botnetz']
        linecycler = cycle(["-","--"])
    elif len(stats)==4:
        folge = ['Vanilla_Einfach', 'Vanilla_Botnetz', 'Gekuerzt_Einfach', 'Gekuerzt_Botnetz']
        linecycler = cycle(["-","-","--","--"])
    else:
        print("error. len(stats)=%d"%(len(stats)))
        sys.exit(1)

    for line in folge:
        # print(line)
        try:
            data=stats[line]
        except:
            line_n = [s for s in stats.keys() if line in s][0]
            print("%s was found in stats as %s."%(line,line_n))
            data = stats[line_n]

        # sorted_data=np.sort(data)
        # yvals=np.arange(1.0,float(len(sorted_data))+1.0)/float(len(sorted_data))

        # print(data)
        #yvals=np.arange(len(sorted_data))/float(len(sorted_data))
        # # new x values
        # xn_ax = np.linspace(sorted_data.min(), sorted_data.max(), 200)
        # print(len(xn_ax))
        # # new y values
        # yn_ax = spline(sorted_data, yvals, xn_ax)
        # print(len(yn_ax))

        data_max = max(data)
        data_shown = filter(lambda x: x < data_max, data)
        shown_percentile = float(len(data_shown)) / len(data)
        print("shown_percentile:",shown_percentile)
        x, y = getcdf(data, shown_percentile)

        # print(find_nearest(y, 0.50))
        if shown_percentile > 0:
            q, i = find_nearest(y, 0.80)
            # print(out_pathname, legend_x)
            print("%s: data[%d]=%f equals %f."\
                %(line,i,y[i],x[i]))

            q, i = find_nearest(y, 0.70)
            # print(out_pathname, legend_x)
            print("%s: data[%d]=%f equals %f."\
                %(line,i,y[i],x[i]))

            q, i = find_nearest(y, 0.50)
            # print(out_pathname, legend_x)
            print("%s: data[%d]=%f equals %f."\
                %(line,i,y[i],x[i]))

            q, i = find_nearest(y, 0.30)
            # print(out_pathname, legend_x)
            print("%s: data[%d]=%f equals %f."\
                %(line,i,y[i],x[i]))

            q, i = find_nearest(y, 0.20)
            # print(out_pathname, legend_x)
            print("%s: data[%d]=%f equals %f."\
                %(line,i,y[i],x[i]))
            # print(line)
            # print(y[i],i)
            # print(x[i])
        # print(x)
        if len(x) != 0 and x_max < max(x):
            x_max = max(x)
        matplotlib.pyplot.plot(x, y,
                color=next(colors),
                label = line,
                linewidth = 2,
                linestyle=next(linecycler))

    # matplotlib.pyplot.style.use('ggplot')
    # matplotlib.pyplot.figure(figsize=(8,6), dpi=72, facecolor="white")
    matplotlib.pyplot.legend(loc='best', fontsize=20) #, fontsize = 'small')

    # if legend_x == 'Days from first stream':
    #     matplotlib.pyplot.xlim(xmin=0.0, xmax=x_max)
    # else:
    #     matplotlib.pyplot.xlim(xmin=0.0)
    # matplotlib.pyplot.xscale('symlog')
    matplotlib.pyplot.xlim(xmin=0.0, xmax=x_max) # x_max) #0.2)
    matplotlib.pyplot.ylim(ymin=0.0)

    # matplotlib.pyplot.yscale('log')
    # matplotlib.pyplot.yscale('close_to_one')
    matplotlib.pyplot.yticks(np.arange(0, 1.2, 0.2))

    # matplotlib.pyplot.xticks(np.arange(0, x_max, 0.1))

    matplotlib.pyplot.xlabel(legend_x, fontsize=20)
    matplotlib.pyplot.ylabel('eCDF', fontsize=20)
#    matplotlib.pyplot.title(title, fontsize=fontsize)
    # matplotlib.pyplot.grid()
    matplotlib.pyplot.tight_layout()
    matplotlib.pyplot.savefig(out_pathname)
    matplotlib.pyplot.close()

    #########################################################################
    # Export Data
    #########################################################################
    a = []
    h = []
    for line in folge:
        h.append(line)
        data=stats[line]
        y, x = getcdf(data, 1)
        a.append(x)
        a.append(y)

    h = ", ".join(h)
    np.savetxt(out_pathname+".dat", np.transpose(a), header=h, fmt="%10.5f")
    #########################################################################

def sliding_mean(data_array, window=5):
    data_array = data_array
    new_list = []
    for i in range(len(data_array)):
        indices = range(max(i - window + 1, 0),
                        min(i + window + 1, len(data_array)))
        avg = 0
        for j in indices:
            avg += data_array[j]
        avg /= float(len(indices))
        new_list.append(avg)

    return new_list

def mean_confidence_interval(amount_datapoint, ammount_all, confidence=0.95):
    a = np.append(1.0*np.array(np.ones(amount_datapoint)),1.0*np.array(np.zeros(ammount_all-amount_datapoint)))
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h

def loc_at_t_plot(compromise_stats, ammount_sims, out_dir, out_name):
    # stats_client_loc_on_times = {}
    # for key in sorted(compromise_stats.keys()):
    #     # key = dirname
    #     # compromise_stats[key] = Array of all simulated Clients
    #     # for stats in compromise_stats[key]:
    #     #     # stats = {time:Compromised(Bool), time:Compromised(Bool), ...}
    #     #     pass
    #     #  {k: sum(d[k] for d in dict1) for k in dict1[0]}
    #
    #     #Absolut:
    #     # stats_client_loc_on_times[key] = {t:sum(d[t] for d in compromise_stats[key]) for t in compromise_stats[key][0]}
    #     #Mean:
    #     stats_client_loc_on_times[key] =\
    #         {(float(t)/float(24*60*60)):(float(sum(d[t])/len(compromise_stats[key])) \
    #         for d in compromise_stats[key]) for t in compromise_stats[key][0]}
    print("loc_at_t_plot(): Will divide values by %d."%ammount_sims)
    stats_client_loc_on_times = compromise_stats
    print('Will plot client_anteil')
    out_filename = out_name + 'client_anteil.pdf'
    out_pathname = os.path.join(out_dir, out_filename)
    tmp_dir = {}
    for key in stats_client_loc_on_times:
        print("Anzahl Values for %s: %d"%(key, len(stats_client_loc_on_times[key].values())))
        if len(stats_client_loc_on_times[key].values()) > 0:
            tmp_dir[key] = [(float(v)/ammount_sims) for v in stats_client_loc_on_times[key].values()]
    # dire = {k:v.values() for k,v in stats_client_loc_on_times}
    plot_cdf(tmp_dir, out_pathname, 'Anteil der Clients')

    print('Will plot client_loc_at_dates')
    out_filename = out_name + 'client_loc_at_dates.pdf'
    out_pathname = os.path.join(out_dir, out_filename)

    # print(len(stats_client_loc_on_times['Gekuerzt_Botnetz']))
    # print(stats_client_loc_on_times['Gekuerzt_Botnetz'][0:5])
    # for i in range(10):
    #     print(stats_client_loc_on_times['Gekuerzt_Botnetz'][i]/float(24*60*60))
    # print(stats_client_loc_on_times['Gekuerzt_Botnetz'][0:5])

    max_time = float(max(stats_client_loc_on_times['Vanilla_Einfach'].keys()))/float(24*60*60)
    min_time = float(min(stats_client_loc_on_times['Vanilla_Einfach'].keys()))/float(24*60*60)
    print(min_time, max_time)
    print(stats_client_loc_on_times['Vanilla_Einfach'].keys()[0:5])
    # color=iter(matplotlib.cm.Set1(np.linspace(0,0.5,len(stats_client_loc_on_times.keys()))))
    colors=iter(['red','black','red','black'])

    start = date(2014,2,1)
    start = datetime.combine(start, datetime.min.time())
    date_legend = [start+timedelta(minutes=(t/60)) for t in stats_client_loc_on_times['Vanilla_Einfach'].keys()]
    print(date_legend[0:5])

    matplotlib.rcParams['xtick.labelsize'] = 15 # Dates
    matplotlib.rcParams['ytick.labelsize'] = 20 # WK
    fig, ax = matplotlib.pyplot.subplots()
    matplotlib.rcParams['xtick.labelsize'] = 15 # Dates
    matplotlib.rcParams['ytick.labelsize'] = 20 # WK
    # ax.rcParams['xtick.labelsize'] = 13 # Dates
    # ax.rcParams['ytick.labelsize'] = 20 # WK

    if len(stats_client_loc_on_times)==2:
        folge = ['Vanilla', 'Gekuerzt']
        linecycler = cycle(["-","--"])
    elif len(stats_client_loc_on_times)==4:
        folge = ['Vanilla_Einfach', 'Vanilla_Botnetz', 'Gekuerzt_Einfach', 'Gekuerzt_Botnetz']
        linecycler = cycle(["-","-","--","--"])
    else:
        print("error. len(stats)=%d"%(len(stats)))
        sys.exit(1)

    #########################################################################
    # Export Data
    #########################################################################
    a = []
    h = []
    #########################################################################

    for key in folge:
        try:
            data=stats_client_loc_on_times[key]
        except:
            line_n = [s for s in stats_client_loc_on_times.keys() if key in s][0]
            print("%s was found in stats as %s."%(key,line_n))
            data = stats_client_loc_on_times[line_n]
        if len((data.items())) == 0:
            continue
        print(key)
        print(len(data.items()))

        data = {(float(t)/float(24*60*60)):float(mean_confidence_interval(v,ammount_sims)[0]) for t,v in data.items()}
        data = collections.OrderedDict(sorted(data.items()))

        dates = data.keys()
        y = len(dates[0:dates.index(float(1))])
        # print("y=%d. dates[0:y]=%s. dates[y+1:y*2]=%s."%(y, dates[0:y], dates[y+1:y*2]))
        data_y = sliding_mean(data.values(),y)
        col=next(colors)

        max_anteil = float(max(data.values()))*100.0
        min_anteil = float(min(data.values()))*100.0
        mean_anteil = float(np.mean(data.values()))*100.0
        print("%s: Max=%f, Min=%f, Mean=%f"%(key,max_anteil, min_anteil, mean_anteil))

        ax.plot(date_legend, data_y,
                color=col,
                label = key,
                linewidth = 2,
                linestyle=next(linecycler))

    #########################################################################
    # Export Data
    #########################################################################
        h.append(key)
        date_strings = [dt.isoformat() for dt in date_legend]
        a.append(date_strings)
        a.append(data_y)

    h = ", ".join(h)
    np.savetxt(out_pathname+".dat", np.transpose(a), header=h, fmt="%20s")

    #########################################################################

    matplotlib.pyplot.gcf().autofmt_xdate()
    matplotlib.pyplot.ylim(ymin=0.0) #,ymax=0.6)
    matplotlib.pyplot.legend(loc='best', fontsize=20)
    #matplotlib.pyplot.xlabel('Tage seit die Relays des Angreifers im Netzwerk sind', fontsize=20)
    # matplotlib.pyplot.ylabel('Mean Anteil Kompromittierter Clients', fontsize=20)
    matplotlib.pyplot.ylabel('Anteil deanonymisierter Clients', fontsize=20)

#    matplotlib.pyplot.title(title, fontsize=fontsize)
    # matplotlib.pyplot.grid()
    matplotlib.pyplot.tight_layout()
    matplotlib.pyplot.savefig(out_pathname)
    matplotlib.pyplot.close()

def read_analysis_files(pathnames):
    """Reads in simulation analysis files (as produced by pathsim_analysis.py).
    Returns list of start times, end times, and statistics."""

    client_compromise_stats = []
    hs_compromise_stats = []
    location_stats = []
    loc_at_t_stats = {}
    guardloc_at_t_stats = {}
    start_time = None
    end_time = None
    for pathname in pathnames:
        with open(str(pathname), 'rb') as f:
            new_start_time = pickle.load(f)
            new_end_time = pickle.load(f)
            new_client_compromise_stats = pickle.load(f)
            new_hs_compromise_stats = pickle.load(f)
            new_location_stats = pickle.load(f)
            try:
                new_loc_at_t_stats = pickle.load(f)
                new_loc_at_t_stats = collections.OrderedDict(sorted(new_loc_at_t_stats.items()))
            except:
                new_loc_at_t_stats = None
            try:
                new_guardloc_at_t_stats = pickle.load(f)
                new_guardloc_at_t_stats = collections.OrderedDict(sorted(new_guardloc_at_t_stats.items()))
            except:
                new_guardloc_at_t_stats = None



            # print(new_loc_at_t_stats.keys()[0:5])
            # for i in range(5):
            #     print(new_loc_at_t_stats.keys()[i]/float(24*60*60))
            # print("new_client_compromise_stats:", new_client_compromise_stats[0],'\n')
            # print("new_hs_compromise_stats:", new_hs_compromise_stats[0], '\n')
            if (new_client_compromise_stats == new_hs_compromise_stats):
                raise ValueError('Alert: new_client_compromise_stats equals new_hs_compromise_stats')
            # if (new_start_time == new_end_time):
            #     raise ValueError('Alert: new_client_compromise_stats equals new_hs_compromise_stats')
            print(new_start_time)
            if (start_time == None):
                start_time = new_start_time
            else:
                start_time = min(start_time, new_start_time)
            if (end_time == None):
                end_time = new_end_time
            else:
                end_time = max(end_time, new_end_time)
            client_compromise_stats.extend(new_client_compromise_stats)
            hs_compromise_stats.extend(new_hs_compromise_stats)
            location_stats.extend(new_location_stats)
            if new_loc_at_t_stats is not None:
                loc_at_t_stats = Counter(loc_at_t_stats) + Counter(new_loc_at_t_stats)
                loc_at_t_stats = collections.OrderedDict(sorted(loc_at_t_stats.items()))
            if new_guardloc_at_t_stats is not None:
                guardloc_at_t_stats = Counter(guardloc_at_t_stats) + Counter(new_guardloc_at_t_stats)
                guardloc_at_t_stats = collections.OrderedDict(sorted(guardloc_at_t_stats.items()))
    if (client_compromise_stats == hs_compromise_stats):
        raise ValueError('Alert: client_compromise_stats equals hs_compromise_stats')
    return (start_time, end_time, client_compromise_stats, hs_compromise_stats, location_stats, loc_at_t_stats, guardloc_at_t_stats)

def compromised_set_plot(pathnames_list, line_labels, out_dir, out_name,
    figsize = None, fontsize = 'small',
    time_legend_locs = {'guard':'lower right', 'exit':'lower right', 'both':'lower right'},
    rate_legend_locs = {'guard':'lower right', 'exit':'lower right', 'both':'lower right'}):
    """Plots cdfs for compromised-set statistics."""
    if (line_labels == None): # assume pathnames given as flat list
        pathnames_list = [pathnames_list]
    # aggregate the stats
    client_compromise_stats = {}
    hs_compromise_stats = {}
    location_stats = {}
    loc_at_t_stats = {}
    guardloc_at_t_stats = {}

    start_times = {}
    end_times = {}
    ammount_sims = 0
    for pathnames in pathnames_list:
        print(pathnames)
        dirnames = os.path.dirname(pathnames[0]).split('/')[-1]
        print(dirnames)
        (start_times[dirnames],
        end_times[dirnames],
        client_compromise_stats[dirnames],
        hs_compromise_stats[dirnames],
        location_stats[dirnames],
        loc_at_t_stats[dirnames],
        guardloc_at_t_stats[dirnames]) = read_analysis_files(pathnames)
        ammount_sims = max(ammount_sims, len(client_compromise_stats[dirnames]))

    if any(loc_at_t_stats.values()):
        loc_at_t_plot(loc_at_t_stats, ammount_sims, out_dir, (out_name+'_Location_'))
    if any(guardloc_at_t_stats.values()):
        loc_at_t_plot(guardloc_at_t_stats, ammount_sims, out_dir, (out_name+'Guard_Location_'))

if __name__ == '__main__':
    usage = 'Usage: client_attack_once.py [in_dir] [out_dir] [out_name]: \nTakes \
all files in in_dir, plots their contents according to type, and outputs the results to \
out_dir. out_name is optional; if omitted, it is \
assumed that input filenames are of form x.y.z, and output files will use x for out_name.'
    if (len(sys.argv) < 3):
        print(usage)
        sys.exit(1)

    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    if (len(sys.argv) > 3):
        out_name = sys.argv[3]
    else:
        out_name = ''

    line_labels = None

    pathnames = []
    for dirpath, dirnames, fnames in os.walk(in_dir):
        tmp_pathnames = []
        if len(dirnames) != 0:
            line_labels = dirnames
            # print(line_labels)
            line_labels = sorted(line_labels)
            # print(line_labels)
        else:
            if len(fnames) != 0:
                for fname in fnames:
                    # print(fname)
                    tmp_pathnames.append(os.path.join(dirpath,fname))
                    tmp_pathnames = sorted(tmp_pathnames)
                    if line_labels == None:
                        line_labels = os.path.dirname(dirpath).split('/')[-1]
                        line_labels = sorted(line_labels)
                pathnames.append(tmp_pathnames)
    pathnames.sort()

    compromised_set_plot(pathnames, line_labels, out_dir, out_name)
