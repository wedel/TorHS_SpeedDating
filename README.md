# Speed Dating: A Performance-Enhanced Rendezvous Circuit for Tor
This is derived from my diploma theses on Tor Rendezvous Circuits. 

The Project is fragmented in the following directories:
 - TorPS/ contains Python Code as an expansion to the original *[The Tor Path Simulator (TorPS)](https://torps.github.io/)* for Hidden Services.
 - TorPerf/ contains R Code to anlyse modified rendezvous Circuits regarding their performance.
 - TorPerf/data/ contains aggregated data for a) a rough compairison between various circuitlength in [TorPerf/data/circuitlength](https://github.com/wedel/TorHS_SpeedDating/tree/master/torperf/data/circuitlength) and b) by a more realistic comparison of vanilla rendezvous circuits and a one-hop shorted circuit in [TorPerf/data/5Hops_rendezvous](https://github.com/wedel/TorHS_SpeedDating/tree/master/torperf/data/5Hops_rendezvous).
 

## TorPS with Rendezvous Ciruits
TorPS is required to get the code running. 

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

0. [Stem](https://stem.torproject.org/) is required fot TorPS simulations. 
1. `git clone https://github.com/torps/torps.git`
2. Copy all files from [TorPS/](https://github.com/wedel/TorHS_SpeedDating/tree/master/torps) dir of this repo to your local copy of TorPS.


### Path Simulation HOWTO

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

bAnd repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo


## Built With



## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE, see [LICENSE](LICENSE) file for details.
