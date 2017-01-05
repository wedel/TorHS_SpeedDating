# Speed Dating: A Performance-Enhanced Rendezvous Circuit for Tor
As part of my diploma thesis on Tor rendezvous circuits, I developed a number of simulation and evaluation scripts and conducted live experiments.
Here, I make the code and the data sets publicly available:

 - `torps_hs/` contains Python code that extends the *[Tor Path Simulator (TorPS)](https://torps.github.io/)* to simulate rendezvous circuits.
 - `torperf/` contains R code to analyze modified rendezvous circuits regarding their performance.
 - `torperf/data/circuitlength` contains aggregated data briefly comparing various circuit lengths
 - `torperf/data/5Hops_rendezvous` contains aggregated data comparing vanilla rendezvous circuits with five-hop rendezvous circuits.


## Simulating Rendezvous Circuits with TorPS

For detailed instructions on TorPS, please refer to their [readme](https://github.com/torps/torps/blob/master/README.md).

###Setup
0. [Stem](https://stem.torproject.org/) is required for TorPS simulations.
1. Get a local copy of TorPS `git clone https://github.com/torps/torps.git`
2. Copy all files from the `torps_hs/` directory to your local copy of TorPS.

### Path Simulation
After preparing Tor consensus and descriptor files for TorPS, you are ready to simulate Tor rendezvous circuits. Running simulations works in the same way as described in the [TorPS readme](https://github.com/torps/torps/blob/master/README.md). That is, by calling
<pre><code>python pathsim.py simulate [args] </pre></code>

Here, we introduce the following *additional* arguments for rendezvous circuit simulation.

**Path selection**:

* `hs_tor` uses vanilla Tor path selection, if connecting to an hidden services.
* `hs_short_tor` uses the performance-enhanced path selection, if connecting to an hidden service.

**User model**:

* `hs_only_simple` connects to a hidden service every minute.
* `hs_simple` connects alternating to a hidden service and google.com every minute.

**Adversary resources**:

* The number of adversary guard, middle and exit relays are set in `num_adv_guards`, `num_adv_middles`, and `num_adv_exits`.
* The amount of consensus bandwidth of adversary guard, middle and exit relays are set in `adv_guard_cons_bw`, `adv_exit_cons_bw`, and `adv_middle_cons_bw`. The bandwidth will be distributed evenly on the number of the adversary relays.

#### Example
<pre><code> python pathsim.py simulate --nsf_dir out/network-state/ns-2014-02--2014-12--num_samples 2000 --user_model hs_only_simple=1800 --format relay-adv --adv_guard_cons_bw 679462  --adv_exit_cons_bw 0 --adv_time 0 --num_adv_guards 1 --num_adv_exits 0 --num_adv_middles 1 --adv_middle_cons_bw 0  --loglevel INFO hs_short_tor</pre></code>

The file `vanilla_vs_short_sim.sh` contains additional examples, including an example for parallelized simulations with a high amount of samples.

### Adversary Resource Distribution
In order to get an optimized adversary resource distribution, we tested various scenarios. In particular, we simulated adversaries with various bandwidth distributions between guard and middle relays. Please note that exit relays are typically not used for rendezvous circuits and therefore do not need to be considered. For more details we refer to the file `bw_allocation_analyze.sh`.

### Version
We based our implementation on Tor version 0.2.6.9. Please notice that the original TorPS was modeled after Tor 0.2.4.23, though.

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE, see [LICENSE](LICENSE) file for details.
