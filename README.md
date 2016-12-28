# Speed Dating: A Performance-Enhanced Rendezvous Circuit for Tor
This is derived from my diploma theses on Tor Rendezvous Circuits and fragmented in the following directories:
 - TorPS/ contains Python Code as an expansion to the original *[The Tor Path Simulator (TorPS)](https://torps.github.io/)* for Hidden Services.
 - TorPerf/ contains R Code to anlyse modified rendezvous Circuits regarding their performance.
 - TorPerf/data/ contains aggregated data for a) a rough compairison between various circuitlength in [TorPerf/data/circuitlength](https://github.com/wedel/TorHS_SpeedDating/tree/master/torperf/data/circuitlength) and b) by a more realistic comparison of vanilla rendezvous circuits and a one-hop shorted circuit in [TorPerf/data/5Hops_rendezvous](https://github.com/wedel/TorHS_SpeedDating/tree/master/torperf/data/5Hops_rendezvous).
 

## TorPS with Rendezvous Ciruits
TorPS is required to get the code running. For all geneal instructions please reffer to their [Readme](https://github.com/torps/torps/blob/master/README.md)

0. [Stem](https://stem.torproject.org/) is required fot TorPS simulations. 
1. Get a local copy of TorPS `git clone https://github.com/torps/torps.git`
2. Copy all files from [TorPS/](https://github.com/wedel/TorHS_SpeedDating/tree/master/torps) dir of this repo to your local copy of TorPS.

### Path Simulation HOWTO
After you processed your local copys of the Tor consensuses and descriptors into a more compact format you are ready for simulation of Tor (rendezvous) circuits. Running simulations over a given periode works just as before and described in the [TorPS Readme](https://github.com/torps/torps/blob/master/README.md) by callin 
<pre><code>python pathsim.py simulate [args] </pre></code>

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE, see [LICENSE](LICENSE) file for details.
