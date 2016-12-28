# Speed Dating: A Performance-Enhanced Rendezvous Circuit for Tor
This is derived from my diploma theses on Tor Rendezvous Circuits and fragmented in the following directories:
 - TorPS_HS/ contains Python Code as an expansion to the original *[The Tor Path Simulator (TorPS)](https://torps.github.io/)* for Hidden Services.
 - TorPerf/ contains R Code to anlyse modified rendezvous Circuits regarding their performance.
 - TorPerf/data/ contains aggregated data for a) a rough compairison between various circuitlength in [TorPerf/data/circuitlength](https://github.com/wedel/TorHS_SpeedDating/tree/master/torperf/data/circuitlength) and b) by a more realistic comparison of vanilla rendezvous circuits and a one-hop shorted circuit in [TorPerf/data/5Hops_rendezvous](https://github.com/wedel/TorHS_SpeedDating/tree/master/torperf/data/5Hops_rendezvous).
 

## TorPS with Rendezvous Ciruits
TorPS is required to get the code running. For all geneal instructions please refer to their [readme](https://github.com/torps/torps/blob/master/README.md)

0. [Stem](https://stem.torproject.org/) is required fot TorPS simulations. 
1. Get a local copy of TorPS `git clone https://github.com/torps/torps.git`
2. Copy all files from [TorPS_HS/](https://github.com/wedel/TorHS_SpeedDating/tree/master/torps_hs) dir of this repo to your local copy of TorPS.

### Path Simulation HOWTO
After you processed your local copys of the Tor consensuses and descriptors into a more compact format you are ready for simulation of Tor (rendezvous) circuits. Running simulations over a given periode works just as before and described in the [TorPS readme](https://github.com/torps/torps/blob/master/README.md) by calling
<pre><code>python pathsim.py simulate [args] </pre></code>
with the following *additional* args:

**Path Algorithm**:
* `hs_tor`
* `hs_short_tor`
* `hs_tor_honeypot`
* `hs_short_tor_honeypot`

**User model**:
* `hs_only_simple` connetcts to a hidden service every minute.
* `hs_simple` connects to a hidden service and google.com alternately every minute. 

**Adversery Relays**:
* The number of adversary guard, middle and exit relays are set in `num_adv_guards`,`num_adv_middles`and `num_adv_exits`
* The ammount of consensus bandwidth of adversary guard, middle and exit relays are set in`adv_guard_cons_bw`, `adv_exit_cons_bw` and `adv_middle_cons_bw`. The consensus bandwidth will be splitted by the number of the adversary relay for each circuit position.

### Example
<pre><code> python pathsim.py simulate --nsf_dir out/network-state/ns-2014-02--2014-12--num_samples 2000 --user_model hs_only_simple=1800 --format relay-adv --adv_guard_cons_bw 679462  --adv_exit_cons_bw 0 --adv_time 0 --num_adv_guards 1 --num_adv_exits 0 --num_adv_middles 1 --adv_middle_cons_bw 0  --loglevel INFO hs_short_tor</pre></code>
     
### Version
We based our implementation on Tor version 0.2.6.9. Please notice, that the original TorPS was moddeled from Tor stable release 0.2.4.23.

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE, see [LICENSE](LICENSE) file for details.
