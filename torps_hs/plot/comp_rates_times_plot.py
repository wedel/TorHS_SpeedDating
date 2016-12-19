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
    np.savetxt(out_pathname+".dat", np.transpose(a), header=h, fmt="%10s")
    #########################################################################

def first_comp_times(start_time, end_time, stats_list):
    """Turns compromise stats into first times of guard/exit/guard&exit compromise."""

    time_len = float(end_time - start_time)/float(24*60*60) # Time_len in Days
    guard_comp_times = []
    middel_comp_times = []
    exit_comp_times = []

    gm_comp_times = []
    ge_comp_times = []
    em_comp_times = []
    gme_comp_times = []

    gm_ge_comp_times = []
    # print(stats_list)
    for stats in stats_list:
        guard_comp_time = time_len
        middel_comp_time = time_len
        exit_comp_time = time_len
        ge_time = time_len
        gm_time = time_len
        em_time = time_len
        gme_time = time_len
        gm_ge_comp_time = time_len

        if (stats['guard_only_time'] != None):
            guard_comp_time = float(stats['guard_only_time'] -\
                start_time)/float(24*60*60)

        if (stats['exit_only_time'] != None):
            exit_comp_time = float(stats['exit_only_time'] -\
                start_time)/float(24*60*60)

        if (stats['middle_only_time'] != None):
            middel_comp_time = float(stats['middle_only_time'] -\
                start_time)/float(24*60*60)

        if  (stats['guard_and_exit_time'] != None):
            ge_time = float(stats['guard_and_exit_time'] -\
                start_time)/float(24*60*60)
            guard_comp_time = min(ge_time, gme_time, gm_time, guard_comp_time)
            exit_comp_time = min(exit_comp_time, ge_time, em_time, gme_time)

            gm_ge_comp_time = min(gm_time, ge_time, gme_time, gm_ge_comp_time)

        if  (stats['guard_and_middle_time'] != None):
            gm_time = float(stats['guard_and_middle_time'] -\
                start_time)/float(24*60*60)
            guard_comp_time = min(ge_time, gme_time, gm_time, guard_comp_time)
            middel_comp_time = min(middel_comp_time, em_time, gme_time, gm_time)

            gm_ge_comp_time = min(gm_time, ge_time, gme_time, gm_ge_comp_time)

        if (stats['exit_and_middle_time'] != None):
            em_time = float(stats['exit_and_middle_time'] -\
                start_time)/float(24*60*60)
            middel_comp_time = min(middel_comp_time, em_time, gme_time, gm_time)
            exit_comp_time = min(exit_comp_time, ge_time, em_time, gme_time)

        if  (stats['guard_and_middle_and_exit_time'] != None):
            gme_time = float(stats['guard_and_middle_and_exit_time'] -\
                start_time)/float(24*60*60)
            guard_comp_time = min(ge_time, gme_time, gm_time, guard_comp_time)
            exit_comp_time = min(exit_comp_time, ge_time, em_time, gme_time)
            middel_comp_time = min(middel_comp_time, em_time, gme_time, gm_time)

            gm_ge_comp_time = min(gm_time, ge_time, gme_time, gm_ge_comp_time)

        guard_comp_times.append(guard_comp_time)
        middel_comp_times.append(middel_comp_time)
        exit_comp_times.append(exit_comp_time)

        gm_comp_times.append(gm_time)
        ge_comp_times.append(ge_time)
        em_comp_times.append(em_time)
        gme_comp_times.append(gme_time)
        gm_ge_comp_times.append(gm_ge_comp_time)

    return (guard_comp_times,
            middel_comp_times,
            exit_comp_times,
            gm_comp_times,
            ge_comp_times,
            em_comp_times,
            gme_comp_times,
            gm_ge_comp_times)

def comp_set_plot_times(start_times, end_times, compromise_stats,
    out_dir, out_name, figsize = None, fontsize = 'small',
    legend_locs = {'guard':'lower right', 'exit':'lower right', 'both':'lower right'}):
    """
    Plots cdfs of times to compromise for compromised-set statistics.
    Input:
        start_times: timestamps of simulation starts for each dataset
        end_times: timestamps of simulation ends for each dataset
        compromise_stats: (list) each element is a list of statistics
            calculated for compromised set
        out_dir: output directory
        out_name: string to comprise part of output filenames
    """

    stats_guard_comp_times = {}
    stats_middel_comp_times = {}
    stats_exit_comp_times = {}

    stats_gm_comp_times = {}
    stats_ge_comp_times = {}
    stats_em_comp_times = {}
    stats_gme_comp_times = {}
    stats_gm_ge_comp_times = {}

    stats_client_gm_loc_times = {}
    stats_client_g_loc_times = {}
    stats_client_guard_dec_times = {}

    print(compromise_stats.keys())
    print(start_times)
    print(end_times)
    for key in sorted(compromise_stats.keys()):
        start_time = start_times[key]
        end_time = end_times[key]

        (guard_comp_times,
        middel_comp_times,
        exit_comp_times,
        gm_comp_times,
        ge_comp_times,
        em_comp_times,
        gme_comp_times,
        gm_ge_comp_times) = first_comp_times(start_time, end_time,
            compromise_stats[key])

        stats_guard_comp_times[key] = guard_comp_times
        stats_middel_comp_times[key] = middel_comp_times
        stats_exit_comp_times[key] = exit_comp_times
        stats_gm_comp_times[key] = gm_comp_times
        stats_ge_comp_times[key] = ge_comp_times
        stats_em_comp_times[key] = em_comp_times
        stats_gme_comp_times[key] = gme_comp_times
        stats_gm_ge_comp_times[key] = gm_ge_comp_times

        # GuardMiddleAttac equals stats_client_gm_loc_times
        # GuardAttac equals stats_client_g_loc_times
        if key.startswith('Vanilla'):
            print('%s stats with Vanilla'%(key))
            stats_client_gm_loc_times[key] = gm_ge_comp_times
            stats_client_g_loc_times[key] = guard_comp_times
            stats_client_guard_dec_times[key] = middel_comp_times
        elif key.startswith('Gekuerzt'):
            print('%s stats with Gekuerzt'%(key))
            stats_client_gm_loc_times[key] = guard_comp_times
            stats_client_g_loc_times[key] = guard_comp_times
            stats_client_guard_dec_times[key] = exit_comp_times
        else:
            print('Error: %s isnt fomated as expected'%(key))

    # cdf of all bad
    print('Will plot guard_comp_times')
    # print(stats_frac_rp_located.keys())
    out_filename = out_name + 'guard_comp_times.pdf'
    out_pathname = os.path.join(out_dir, out_filename)
    plot_cdf(stats_guard_comp_times, out_pathname, 'Tage ab dem ersten Rendezvous Circuit')

    print('Will plot client_guard_dec_times')
    # print(stats_frac_client_located.keys())
    out_filename = out_name + 'client_guard_dec_times.pdf'
    out_pathname = os.path.join(out_dir, out_filename)
    plot_cdf(stats_client_guard_dec_times, out_pathname, 'Tage ab dem ersten Rendezvous Circuit')

    # print('Will plot middel_comp_times')
    # # print(stats_frac_hs_located.keys())
    # out_filename = out_name + 'middel_comp_times.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_middel_comp_times, out_pathname, 'Tage ab dem ersten Rendezvous Circuit')
    #
    # print('Will plot exit_comp_times')
    # # print(stats_frac_client_located.keys())
    # out_filename = out_name + 'exit_comp_times.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_exit_comp_times, out_pathname, 'Tage ab dem ersten Rendezvous Circuit')
    #
    # print('Will plot gm_comp_times')
    # # print(stats_frac_client_located.keys())
    # out_filename = out_name + 'gm_comp_times.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_gm_comp_times, out_pathname, 'Tage ab dem ersten Rendezvous Circuit')
    #
    # print('Will plot ge_comp_times')
    # # print(stats_frac_client_located.keys())
    # out_filename = out_name + 'ge_comp_times.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_ge_comp_times, out_pathname, 'Tage ab dem ersten Rendezvous Circuit')
    #
    # print('Will plot em_comp_times')
    # # print(stats_frac_client_located.keys())
    # out_filename = out_name + 'em_comp_times.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_em_comp_times, out_pathname, 'Tage ab dem ersten Rendezvous Circuit')
    #
    # print('Will plot gme_comp_times')
    # # print(stats_frac_client_located.keys())
    # out_filename = out_name + 'gme_comp_times.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_gme_comp_times, out_pathname, 'Tage ab dem ersten Rendezvous Circuit')
    #
    # print('Will plot gm_ge_comp_times')
    # # print(stats_frac_client_located.keys())
    # out_filename = out_name + 'gm_ge_comp_times.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_gm_ge_comp_times, out_pathname, 'Tage ab dem ersten Rendezvous Circuit')
    #
    # print('Will plot client_gm_loc_times')
    # # print(stats_frac_client_located.keys())
    # out_filename = out_name + 'client_loc_gm_times.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_client_gm_loc_times, out_pathname, 'Tage ab dem ersten Rendezvous Circuit')
    #
    # print('Will plot client_g_loc_times')
    # # print(stats_frac_client_located.keys())
    # out_filename = out_name + 'client_loc_g_times.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_client_g_loc_times, out_pathname, 'Tage ab dem ersten Rendezvous Circuit')

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

# def sliding_mean(data_array, dates, day=1):
#
#     y = len(dates[0:dates.index(float(day))])
#     print("y=%d. dates[0:y]=%s. dates[y+1:y*2]=%s."%(y, dates[0:y], dates[y+1:y*2]))
#     new_list = [data_array[x:x+y] for x in range(0, len(data_array),y)]
#     print("len(Data_array)=%d, len(new_list)=%d."%\
#             (len(data_array), len(new_list)))

    #         indices = range(max(i - window + 1, 0),
    #                     min(i + window + 1, len(data_array)))
    #     avg = 0
    #     for j in indices:
    #         avg += data_array[j]
    #     avg /= float(len(indices))
    #     new_list.append(avg)
    #
    # return new_list


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

    # print('Will plot client_anteil')
    # out_filename = out_name + 'client_anteil.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # tmp_dir = {}
    # for key in stats_client_loc_on_times:
    #     print("Anzahl Values for %s: %d"%(key, len(stats_client_loc_on_times[key].values())))
    #     if len(stats_client_loc_on_times[key].values()) > 0:
    #         tmp_dir[key] = [(float(v)/ammount_sims) for v in stats_client_loc_on_times[key].values()]
    # # dire = {k:v.values() for k,v in stats_client_loc_on_times}
    # plot_cdf(tmp_dir, out_pathname, 'Anteil der Clients')

    print('Will plot client_loc_at_times')
    out_filename = out_name + 'client_loc_at_times.pdf'
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
    # lines = ["-","-","--","--"]
    # linecycler = cycle(lines)

    if len(stats_client_loc_on_times)==2:
        folge = ['Vanilla', 'Gekuerzt']
        linecycler = cycle(["-","--"])
    elif len(stats_client_loc_on_times)==4:
        folge = ['Vanilla_Einfach', 'Vanilla_Botnetz', 'Gekuerzt_Einfach', 'Gekuerzt_Botnetz']
        linecycler = cycle(["-","-","--","--"])
    else:
        print("error. len(stats)=%d"%(len(stats)))
        sys.exit(1)

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
        # print(type(data))
        # print(data.items()[0])
        #mean
        # data = {(float(t)/float(24*60*60)):(float(v)/ammount_sims) for t,v in data.items()}
        # data = collections.OrderedDict(sorted(data.items()))
        print(mean_confidence_interval(data.values()[0], ammount_sims,0.75))


        data = {(float(t)/float(24*60*60)):float(mean_confidence_interval(v,ammount_sims)[0]) for t,v in data.items()}
        data = collections.OrderedDict(sorted(data.items()))

        # data_y = sliding_mean(data.values(), data.keys())
        dates = data.keys()
        y = len(dates[0:dates.index(float(1))])
        # print("y=%d. dates[0:y]=%s. dates[y+1:y*2]=%s."%(y, dates[0:y], dates[y+1:y*2]))
        data_y = sliding_mean(data.values(),y)
        if key == 'Gekuerzt_Botnetz':
            data_bot = data_y
        elif key == 'Gekuerzt_Einfach':
            data_easy = data_y

        # data_sem_max = {(float(t)/float(24*60*60)):float(mean_confidence_interval(v,ammount_sims,0.75)[2]) for t,v in data.items()}
        # data_sem_max = collections.OrderedDict(sorted(data.items()))
        # # data_sem_max_y = sliding_mean(data_sem_max.values(),y)
        # data_sem_min = {(float(t)/float(24*60*60)):float(mean_confidence_interval(v,ammount_sims,0.75)[1]) for t,v in data.items()}
        # data_sem_min = collections.OrderedDict(sorted(data.items()))
        # data_sem_min_y = sliding_mean(data_sem_min.values(),y)

        # data_sem = {float(t):((float(v)/float(math.sqrt(ammount_sims)))) for t,v in data.items()}
        # data_sem = collections.OrderedDict(sorted(data.items()))
        # data_y_sem = sliding_mean(data_sem.values())
        # data_y_sem_min = [min(y-s,0) for y,s in zip(data_y, data_y_sem)]
        # data_y_sem_max = [y+s for y,s in zip(data_y, data_y_sem)]
        #Absolut
        #data= (stats_client_loc_on_times[key]
        col=next(colors)

        # matplotlib.pyplot.fill_between(data_sem_min.keys(), data_sem_min.values(),
        #          data_sem_max.values(), color=col, alpha=0.5)


        matplotlib.pyplot.plot(data.keys(), data_y,
                color=col,
                label = key,
                linewidth = 2,
                linestyle=next(linecycler))
        # matplotlib.pyplot.line(data.keys(), data.values(),
        #         color=next(color),
        #         label = key,
        #         linewidth = 1,
        #         linestyle=next(linecycler))
        # matplotlib.pyplot.scatter(data.keys(), data.values(),
        #         color=next(color),
        #         label = key,
        #         s=1,
        #         alpha=0.1)
                # linewidth = 1,
                # linestyle=next(linecycler))
        # matplotlib.pyplot.hist(data.values(), bins=len(data.keys())),
        #                 histtype='step',
        #                 stacked=True,
        #                 fill=True)
        # matplotlib.pyplot.xcorr(data.keys(), data.values(),
        #         # s=area,
        #         # c=next(color),
        #         label=key)
        #         # alpha=0.5)

    # print("len data_bot: %d"%(len(data_bot)))
    # diff_array = np.array([float(a)-float(b) for a,b in zip(data_bot,data_easy)])
    # # print(diff_array)
    # max_diff = float(max(diff_array.max(),0.0))
    # min_diff = float(max(diff_array.min(),0.0))
    #
    # print("Max-Diff: %f. Min-Diff: %f."%(max_diff, min_diff))

    matplotlib.rcParams['xtick.labelsize'] = 18
    matplotlib.rcParams['ytick.labelsize'] = 18
    matplotlib.pyplot.legend(loc='best', fontsize=20) #, fontsize = 'small')
    matplotlib.pyplot.xlim(xmin=min_time, xmax=max_time)
    matplotlib.pyplot.ylim(ymin=0.0)#,ymax=0.6)

    # matplotlib.pyplot.yticks(np.arange(0, 1.1, 0.1))

    # matplotlib.pyplot.yticks(np.arange(0, 0.61, 0.1))
    matplotlib.pyplot.xlabel('Tage seit die Relays des Angreifers im Netzwerk sind', fontsize=20)
    # matplotlib.pyplot.ylabel('Mean Anteil Kompromittierter Clients', fontsize=20)
    matplotlib.pyplot.ylabel('Wahrscheinlichkeit', fontsize=20)

#    matplotlib.pyplot.title(title, fontsize=fontsize)
    # matplotlib.pyplot.grid()
    matplotlib.pyplot.tight_layout()
    matplotlib.pyplot.savefig(out_pathname)
    matplotlib.pyplot.close()


def relay_comp_plot_cdf(compromise_stats, out_dir, out_name, figsize = None, fontsize = 'small',
    legend_locs = {'guard':'lower right', 'exit':'lower right', 'both':'lower right'}):
    """
    Plots cdfs of compromise fractions for compromised-set statistics.
    Input:
        compromise_stats: (list) each element is a list of statistics
            calculated for the compromised set
        line_labels: (list) each element is a line label or None if only
            one line to be plotted
        out_dir: directory for output files
        out_name: identifying string to be incorporated in filenames

    """
    stats_frac_guard_comp = {}
    stats_frac_middle_comp = {}
    stats_frac_exit_comp = {}

    stats_gm_comp = {}
    stats_ge_comp = {}
    stats_em_comp = {}
    stats_gme_comp = {}

    stats_gm_ge_comp = {}
    stats_client_g_loc = {}
    stats_client_gm_loc = {}
    stats_client_guard_desc = {}
    # print(compromise_stats.keys())
    # print(len(compromise_stats.keys()))
    for key in sorted(compromise_stats.keys()):
        frac_guard_comp = []
        frac_middle_comp = []
        frac_exit_comp =[]

        frac_gm_comp = []
        frac_ge_comp = []
        frac_em_comp = []
        frac_gme_comp = []

        frac_gm_ge_comp = []

        print(len(compromise_stats[key]))

        # print(len(compromise_stats[key]))
        for stats in compromise_stats[key]:
            # print "len(stats)=",len(stats)
            # print(stats)
            tot_ct = float(stats['guard_only_bad'] +
                    stats['middle_only_bad'] +
                    stats['exit_only_bad'] +
                    stats['guard_and_exit_bad'] +
                    stats['guard_and_middle_bad'] +
                    stats['exit_and_middle_bad'] +
                    stats['guard_and_middle_and_exit_bad'] +
                    stats['good'])
            # print(tot_ct)
            frac_guard_comp.append(\
               float(stats['guard_only_bad'] +
                stats['guard_and_exit_bad'] +
                stats['guard_and_middle_bad'] +
                stats['guard_and_middle_and_exit_bad']) / float(tot_ct))
            frac_middle_comp.append(\
               float(stats['middle_only_bad'] +
                stats['guard_and_middle_bad'] +
                stats['exit_and_middle_bad'] +
                stats['guard_and_middle_and_exit_bad'])  / float(tot_ct))
            frac_exit_comp.append(\
               float(stats['exit_only_bad'] +
                stats['guard_and_exit_bad'] +
                stats['exit_and_middle_bad'] +
                stats['guard_and_middle_and_exit_bad']) / float(tot_ct))

            frac_gm_comp.append(\
               float(stats['guard_and_middle_bad'] +
                stats['guard_and_middle_and_exit_bad']) / float(tot_ct))

            frac_ge_comp.append(\
               float(stats['guard_and_exit_bad'] +
                stats['guard_and_middle_and_exit_bad']) / float(tot_ct))

            frac_em_comp.append(\
               float(stats['exit_and_middle_bad'] +
                stats['guard_and_middle_and_exit_bad']) / float(tot_ct))

            frac_gme_comp.append(\
               float(stats['guard_and_middle_and_exit_bad']) / float(tot_ct))

            frac_gm_ge_comp.append(\
               float(stats['guard_and_exit_bad'] +
               stats['guard_and_middle_bad'] +
               stats['guard_and_middle_and_exit_bad']) / float(tot_ct))


            # client_anteil_loc = [frac_guard_comp.sort()]



        stats_frac_guard_comp[key] = frac_guard_comp
        stats_frac_middle_comp[key] = frac_middle_comp
        stats_frac_exit_comp[key] = frac_exit_comp
        stats_gm_comp[key] = frac_gm_comp
        stats_ge_comp[key] = frac_ge_comp
        stats_em_comp[key] = frac_em_comp
        stats_gme_comp[key] = frac_gme_comp
        stats_gm_ge_comp[key] = frac_gm_ge_comp

        # GuardMiddleAttac equals stats_client_gm_loc_times
        # GuardAttac equals stats_client_g_loc_times
        if key.startswith('Vanilla'):
            print('%s stats with Vanilla'%(key))
            stats_client_gm_loc[key] = frac_gm_ge_comp
            stats_client_g_loc[key] = frac_guard_comp
            stats_client_guard_desc[key] = frac_middle_comp
        elif key.startswith('Gekuerzt'):
            print('%s stats with Gekuerzt'%(key))
            stats_client_gm_loc[key] = frac_guard_comp
            stats_client_g_loc[key] = frac_guard_comp
            stats_client_guard_desc[key] = frac_exit_comp
        else:
            print('Error: %s isnt fomated as expected'%(key))


        # if key.startswith('Vanilla'):
        #     print('%s stats with vanilla'%(key))
        #     if key.endswith('MiddleAdv'):
        #         print('%s ends with MiddleAdv'%(key))
        #         stats_client_loc[key] = frac_gm_ge_comp
        #         stats_client_guard_desc[key] =
        #     elif key.endswith('GuardAdv'):
        #         print('%s ends with GuardAdv'%(key))
        #         stats_client_loc[key] = frac_guard_comp
        # elif key.startswith('Gekuerzt'):
        #     print('%s stats with short'%(key))
        #     stats_client_loc[key] = frac_guard_comp
        # else:
        #     print('Error: %s isnt as expected'%(key))

    print('Will plot guard_comp')
    print(stats_frac_guard_comp.keys())
    out_filename = out_name + 'guard_comp.pdf'
    out_pathname = os.path.join(out_dir, out_filename)
    plot_cdf(stats_frac_guard_comp, out_pathname, 'Anteil der Rendezvous Circuits')

    print('Will plot client_guard_desc')
    # print(stats_frac_client_located.keys())
    out_filename = out_name + 'client_guard_desc.pdf'
    out_pathname = os.path.join(out_dir, out_filename)
    plot_cdf(stats_client_guard_desc, out_pathname, 'Anteil der Rendezvous Circuits')

    # print('Will plot middle_comp')
    # print(stats_frac_middle_comp.keys())
    # out_filename = out_name + 'middle_comp.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_frac_middle_comp, out_pathname, 'Anteil der Rendezvous Circuits')
    #
    # print('Will plot exit_comp')
    # print(stats_frac_exit_comp.keys())
    # out_filename = out_name + 'exit_comp.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_frac_exit_comp, out_pathname, 'Anteil der Rendezvous Circuits')
    #
    # print('Will plot gm_comp')
    # # print(stats_frac_client_located.keys())
    # out_filename = out_name + 'gm_comp.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_gm_comp, out_pathname, 'Anteil der Rendezvous Circuits')
    #
    # print('Will plot ge_comp')
    # # print(stats_frac_client_located.keys())
    # out_filename = out_name + 'ge_comp.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_ge_comp, out_pathname, 'Anteil der Rendezvous Circuits')
    #
    # print('Will plot em_comp')
    # # print(stats_frac_client_located.
    # stats_frac_guard_comp[key] = frac_guard_comp
    # stats_frac_middle_comp[key] = frac_middle_comp
    # stats_frac_exit_comp[key] = frac_exit_comp
    # stats_gm_comp[key] = frac_gm_comp
    # stats_ge_comp[key] = frac_ge_comp
    # stats_em_comp[key] = frac_em_comp
    # stats_gme_comp[key] = frac_gme_comp
    # stats_gm_ge_comp[key] = frac_gm_ge_comp
    #
    #     # GuardMiddleAttac equals stats_client_gm_loc_timeskeys())
    # out_filename = out_name + 'em_comp.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_em_comp, out_pathname, 'Anteil der Rendezvous Circuits')
    #
    # print('Will plot gme_comp')
    # # print(stats_frac_client_located.keys())
    # out_filename = out_name + 'gme_comp.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_gme_comp, out_pathname, 'Anteil der Rendezvous Circuits')
    #
    # print('Will plot gm_ge_comp')
    # # print(stats_frac_client_located.keys())
    # out_filename = out_name + 'gm_ge_comp.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_gm_ge_comp, out_pathname, 'Anteil der Rendezvous Circuits')
    #
    # print('Will plot client_gm_loc')
    # # print(stats_frac_client_located.keys())
    # out_filename = out_name + 'client_gm_loc.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_client_gm_loc, out_pathname, 'Anteil der Rendezvous Circuits')
    #
    # print('Will plot client_g_loc')
    # # print(stats_frac_client_located.keys())
    # out_filename = out_name + 'client_g_loc.pdf'
    # out_pathname = os.path.join(out_dir, out_filename)
    # plot_cdf(stats_client_g_loc, out_pathname, 'Anteil der Rendezvous Circuits')



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
            # print(new_start_time)
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

    # if any(loc_at_t_stats.values()):
    #     loc_at_t_plot(loc_at_t_stats, ammount_sims, out_dir, (out_name+'_Location_'))
    # if any(guardloc_at_t_stats.values()):
    #     loc_at_t_plot(guardloc_at_t_stats, ammount_sims, out_dir, (out_name+'Guard_Location_'))
    comp_set_plot_times(start_times, end_times, client_compromise_stats, out_dir, (out_name+'client_'))
    # comp_set_plot_times(start_times, end_times, hs_compromise_stats, out_dir, (out_name+'hs_'))
    relay_comp_plot_cdf(client_compromise_stats, out_dir, (out_name+'client_'))
    # relay_comp_plot_cdf(hs_compromise_stats, out_dir, (out_name+'hs_'))


if __name__ == '__main__':
    usage = 'Usage: comp_rates_plot.py [in_dir] [out_dir] [out_name]: \nTakes \
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
