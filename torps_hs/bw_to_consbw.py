from network_analysis import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def consbw_calc(bw, a, b):
    return max(0, int(round(float((bw-b)/a))))

def get_regression_coeff(in_dir, num_processes):

    (guard_a, guard_b, guard_r_squared, guard_cons_bws, guard_obs_bws) =\
        get_guard_regression(in_dir, num_processes)
    # guard_a = 297.655588881
    # guard_b = 1717416.85555
    # guard_r_squared = 0.698512970655

    print("### coefficients from guard relays:\n\
    # guard_a = {0}\n\
    # guard_b = {1}\n\
    # guard_r_squared = {2}"\
    .format(guard_a, guard_b, guard_r_squared))

    (middle_a, middle_b, middle_r_squared, middle_cons_bws, middle_obs_bws) =\
        get_middle_regression(in_dir, num_processes)
    print("### coefficients from middle relays:\n\
    # middles_a = {0}\n\
    # middles_b = {1}\n\
    # middles_r_squared = {2}"\
    .format(middle_a, middle_b, middle_r_squared))

    # out_name = 'guard_regression.png'
    # out_pathname = os.path.join('./', out_name)
    # plot(guard_a, guard_b, guard_obs_bws, guard_cons_bws, out_pathname)

    # out_name = 'middle_regression.png'
    # out_pathname = os.path.join('./', out_name)
    # plot(middle_a, middle_b, middle_obs_bws, middle_cons_bws, out_pathname)

    # return (guard_a, guard_b, None, None, middle_a, middle_b, None, None)
    return (guard_a, guard_b, guard_cons_bws, guard_obs_bws, middle_a, middle_b, middle_cons_bws, middle_obs_bws)



def plot(a,b,x,y,out_pathname):
    x = np.asarray(x)
    y = np.asarray(y)
    plt.plot(x, y, 'o', label='Original data', markersize=1)
    # plt.plot(x, (a*x + b), 'r', label='Fitted line Cons')
    plt.plot(x, ((y-b)/a), 'b', label='Fitted line')
    plt.legend()
    plt.ylabel('Consensus Bandwidth', fontsize='small')
    plt.xlabel('Observed Bandwidth', fontsize='small')
    plt.grid()
    plt.tight_layout()
    plt.savefig(out_pathname)
    plt.close()

def print_bw_to_cons(full_bw, div_in_routers, guard_a, guard_b, middle_a, middle_b):
    ratios = ['1:3','1:2','1:1','3:2','2:1','7:3','3:1','4:1','9:1','50:1','1:0']
    divs = [0.25, 0.333333333333, 0.5, 0.6, 0.66666666666666, 0.7, 0.75, 0.8, 0.9, 0.98, 1]

    print('\n### {0} Byte FullBW divided through {1} adv Guard(s) and {1} adv Middle(s).'\
    .format(full_bw, div_in_routers))
    print('#{:>12}  {:>12}  {:>12}  {:>12}  {:>12}'\
    .format('Ratio', 'guard_bw','middle_bw', 'guard_cons', 'middle_cons'))
    for ratio, div in zip(ratios, divs):
        guard_bw = int(round((full_bw*div)/div_in_routers))
        middle_bw = int(round((full_bw*(1-div))/div_in_routers))
        print('#{:>12}  {:>12}  {:>12}  {:>12}  {:>12}'\
        .format(ratio,
                guard_bw,
                middle_bw,
                consbw_calc(guard_bw, guard_a, guard_b),
                consbw_calc(middle_bw, middle_a, middle_b)))


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print('Wrong usage. Usage: bw_to_consbw.py [in_dir]: in_dir is the directory containing network state files.')
        sys.exit(-1)
    else:
        in_dir = sys.argv[1]
        num_processes = 20
        # sys.exit(1)


    (guard_a,
    guard_b,
    guard_cons_bws,
    guard_obs_bws,
    middle_a,
    middle_b,
    middle_cons_bws,
    middle_obs_bws) = get_regression_coeff(in_dir, num_processes)







    # # from ns-2014-03:
    # # guard_r_squared = 0.797948722029
    # guard_a = 306.708195266
    # guard_b = 1318438.06549
    # # middles_r_squared = 0.809001003306
    # middle_a = 319.636788605
    # middle_b = 741615.803375

    print("100MiB Guard BW = 104857600 Byte ergibt ~ {0} Cons BW"\
        .format(consbw_calc(104857600, guard_a, guard_b)))

    print("100MiB Middle BW = 104857600 Byte ergibt ~ {0} Cons BW\n"\
            .format(consbw_calc(104857600, middle_a, middle_b)))


    full_bw = 104857600 # 100MiB
    print_bw_to_cons(full_bw, 1, guard_a, guard_b, middle_a, middle_b)
    print_bw_to_cons(full_bw/2, 1, guard_a, guard_b, middle_a, middle_b)
    print_bw_to_cons(full_bw*2, 1, guard_a, guard_b, middle_a, middle_b)

    # out_name = 'guard_regression.png'
    # out_pathname = os.path.join('./', out_name)
    # plot(guard_a, guard_b, guard_obs_bws, guard_cons_bws, out_pathname)

    # out_name = 'middle_regression.png'
    # out_pathname = os.path.join('./', out_name)
    # plot(middle_a, middle_b, middle_obs_bws, middle_cons_bws, out_pathname)
