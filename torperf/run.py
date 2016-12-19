#!/usr/bin/python

### Copyright 2007 Steven J. Murdoch
### See LICENSE for licensing information

### Modded by Moritz Wedel

import os
import time

## Configuration
#

#Socks_Port for every other version of TOR:
# SocksPort_short1Guard_HS1Guard = 9020
SocksPort_short3Guard_HS1Guard = 9021
# SocksPort_vanilla1Guard_HS1Guard = 9022
SocksPort_vanilla3Guard_HS1Guard = 9023

# SocksPort_short1Guard_HS3Guard = 9024
SocksPort_short3Guard_HS3Guard = 9025
# SocksPort_vanilla1Guard_HS3Guard = 9026
SocksPort_vanilla3Guard_HS3Guard = 9027

#Controle_Port for every other version of TOR:
# ControlePort_short1Guard_HS1Guard= 10020
ControlePort_short3Guard_HS1Guard = 10021
# ControlePort_vanilla1Guard_HS1Guard = 10022
ControlePort_vanilla3Guard_HS1Guard = 10023

# ControlePort_short1Guard_HS3Guard= 10024
ControlePort_short3Guard_HS3Guard = 10025
# ControlePort_vanilla1Guard_HS3Guard = 10026
ControlePort_vanilla3Guard_HS3Guard = 10027

# Server to download from
server_1Guard = "utqbkxcywf6um6so.onion"
server_3Guard= "ll4wxm53bswwkjxl.onion"

## Files to download
bigfile = "/.5mbfile" ## location of big file on server

#How much bytes are expected?
expectedBytes = 5*(10**6) #   5 * (10**6) # 5MB
print expectedBytes

## Duration of a experiment
test_duration = 10 * 60 ## Should be > 10min to ensure circuits are not re-used

#Duration for a sub-experiment
delay = test_duration / 4

vanillaTor_basedir = "$HOME/tor_vanilla"
shortTor_basedir = "$HOME/tor_short"


## Main program
print("Start Tor's...")
#Start Tor's
# os.system("cd %s/Client1Guard/HS1Guard/torperfdata/ && %s/Client1Guard/HS1Guard/src/or/tor -f %s/Client1Guard/HS1Guard/tordata/torrc &"%(vanillaTor_basedir, vanillaTor_basedir, vanillaTor_basedir))
# os.system("cd %s/Client1Guard/HS3Guard/torperfdata/ && %s/Client1Guard/HS3Guard/src/or/tor -f %s/Client1Guard/HS3Guard/tordata/torrc &"%(vanillaTor_basedir, vanillaTor_basedir, vanillaTor_basedir))
os.system("cd %s/Client3Guard/HS1Guard/torperfdata/ && %s/Client3Guard/HS1Guard/src/or/tor -f %s/Client3Guard/HS1Guard/tordata/torrc &"%(vanillaTor_basedir, vanillaTor_basedir, vanillaTor_basedir))
os.system("cd %s/Client3Guard/HS3Guard/torperfdata/ && %s/Client3Guard/HS3Guard/src/or/tor -f %s/Client3Guard/HS3Guard/tordata/torrc &"%(vanillaTor_basedir, vanillaTor_basedir, vanillaTor_basedir))

# os.system("cd %s/Client1Guard/HS1Guard/torperfdata/ && %s/Client1Guard/HS1Guard/src/or/tor -f %s/Client1Guard/HS1Guard/tordata/torrc &"%(shortTor_basedir, shortTor_basedir, shortTor_basedir))
# os.system("cd %s/Client1Guard/HS3Guard/torperfdata/ && %s/Client1Guard/HS3Guard/src/or/tor -f %s/Client1Guard/HS3Guard/tordata/torrc &"%(shortTor_basedir, shortTor_basedir, shortTor_basedir))
os.system("cd %s/Client3Guard/HS1Guard/torperfdata/ && %s/Client3Guard/HS1Guard/src/or/tor -f %s/Client3Guard/HS1Guard/tordata/torrc &"%(shortTor_basedir, shortTor_basedir, shortTor_basedir))
os.system("cd %s/Client3Guard/HS3Guard/torperfdata/ && %s/Client3Guard/HS3Guard/src/or/tor -f %s/Client3Guard/HS3Guard/tordata/torrc &"%(shortTor_basedir, shortTor_basedir, shortTor_basedir))

time.sleep(10)

print("Start extra_stat's...")
# os.system("cd %s/Client1Guard/HS1Guard/torperfdata/ && python $HOME/torperf/extra_stats.py --truncate %i short1Guard_HS1Guard.extradata &"%(shortTor_basedir, ControlePort_short1Guard_HS1Guard))
# os.system("cd %s/Client1Guard/HS3Guard/torperfdata/ && python $HOME/torperf/extra_stats.py --truncate %i short1Guard_HS3Guard.extradata &"%(shortTor_basedir, ControlePort_short1Guard_HS3Guard))

os.system("cd %s/Client3Guard/HS1Guard/torperfdata/ && python $HOME/torperf/extra_stats.py %i short3Guard_HS1Guard.extradata &"%(shortTor_basedir, ControlePort_short3Guard_HS1Guard))
os.system("cd %s/Client3Guard/HS3Guard/torperfdata/ && python $HOME/torperf/extra_stats.py %i short3Guard_HS3Guard.extradata &"%(shortTor_basedir, ControlePort_short3Guard_HS3Guard))

# os.system("cd %s/Client1Guard/HS1Guard/torperfdata/ && python $HOME/torperf/extra_stats.py --truncate %i vanilla1Guard_HS1Guard.extradata &"%(vanillaTor_basedir, ControlePort_vanilla1Guard_HS1Guard))
# os.system("cd %s/Client1Guard/HS3Guard/torperfdata/ && python $HOME/torperf/extra_stats.py --truncate %i vanilla1Guard_HS3Guard.extradata &"%(vanillaTor_basedir, ControlePort_vanilla1Guard_HS3Guard))

os.system("cd %s/Client3Guard/HS1Guard/torperfdata/ && python $HOME/torperf/extra_stats.py %i vanilla3Guard_HS1Guard.extradata &"%(vanillaTor_basedir, ControlePort_vanilla3Guard_HS1Guard))
os.system("cd %s/Client3Guard/HS3Guard/torperfdata/ && python $HOME/torperf/extra_stats.py %i vanilla3Guard_HS3Guard.extradata &"%(vanillaTor_basedir, ControlePort_vanilla3Guard_HS3Guard))
time.sleep(10)

print("Will start Testing with Vanilla and ShortTor...")

#Start Downloading with Socks-Client
wait = 0

# Wie viele widerholungen?
for i in range(3024*4): #3 Woche laufzeit
    if wait > 0:
        print("...")
        time.sleep(wait)
    choose_case = (i % 4)
    if choose_case == 0:
        test_type = "Short 3 Guards & HS 1 Guard"
        logfile = shortTor_basedir + "/Client3Guard/HS1Guard/torperfdata/short3Guard_HS1Guard.data"
        server = server_1Guard
    if choose_case == 1:
        test_type = "Short 3 Guards & HS 3 Guard"
        logfile = shortTor_basedir + "/Client3Guard/HS3Guard/torperfdata/short3Guard_HS3Guard.data"
        server = server_3Guard
    if choose_case == 2:
        test_type = "Vanilla 3 Guard & HS 1 Guard"
        logfile = vanillaTor_basedir + "/Client3Guard/HS1Guard/torperfdata/vanilla3Guard_HS1Guard.data"
        server = server_1Guard
    if choose_case == 3:
        test_type = "Vanilla 3 Guard & HS 3 Guard"
        logfile = vanillaTor_basedir + "/Client3Guard/HS3Guard/torperfdata/vanilla3Guard_HS3Guard.data"
        server = server_3Guard

    print "Starting run %s"%test_type, i, "at", time.asctime()
    start = time.time()
    if test_type == "Short 3 Guards & HS 1 Guard":
        os.system("torperf/trivsocks-client %s 127.0.0.1:%i %s %i >> %s 2>/dev/null"%(server, SocksPort_short3Guard_HS1Guard, bigfile, expectedBytes, logfile))
    if test_type == "Short 3 Guards & HS 3 Guard":
        os.system("torperf/trivsocks-client %s 127.0.0.1:%i %s %i >> %s 2>/dev/null"%(server, SocksPort_short3Guard_HS3Guard, bigfile, expectedBytes, logfile))
    if test_type == "Vanilla 3 Guard & HS 1 Guard":
        os.system("torperf/trivsocks-client %s 127.0.0.1:%i %s %i >> %s 2>/dev/null"%(server, SocksPort_vanilla3Guard_HS1Guard, bigfile, expectedBytes, logfile))
    if test_type == "Vanilla 3 Guard & HS 3 Guard":
        os.system("torperf/trivsocks-client %s 127.0.0.1:%i %s %i >> %s 2>/dev/null"%(server, SocksPort_vanilla3Guard_HS3Guard, bigfile, expectedBytes, logfile))
    wait = start + delay - time.time()
    print "Finished run %s"%test_type, i, "at", time.asctime(), "waiting for %5f s"%wait

# #Finished Tests
print("Finished Test's.")


    # if choose_case== 0:
    #     test_type = "Short 1 Guard & HS 1 Guard"
    #     logfile = shortTor_basedir + "/Client1Guard/HS1Guard/torperfdata/short1Guard_HS1Guard.data"
    #     server = server_1Guard
    # if choose_case== 1:
    #     test_type = "Short 1 Guard & HS 3 Guard"
    #     logfile = shortTor_basedir + "/Client1Guard/HS3Guard/torperfdata/short1Guard_HS3Guard.data"
    #     server = server_3Guard
    # if choose_case == 4:
    #     test_type = "Vanilla 1 Guard & HS 1 Guard"
    #     logfile = vanillaTor_basedir + "/Client1Guard/HS1Guard/torperfdata/vanilla1Guard_HS1Guard.data"
    #     server = server_1Guard
    # if choose_case == 5:
    #     test_type = "Vanilla 1 Guard & HS 3 Guard"
    #     logfile = vanillaTor_basedir + "/Client1Guard/HS3Guard/torperfdata/vanilla1Guard_HS3Guard.data"
    #     server = server_3Guard


    # if test_type == "Short 1 Guard & HS 1 Guard":
    #     os.system("torperf/trivsocks-client %s 127.0.0.1:%i %s %i >> %s 2>/dev/null"%(server, SocksPort_short1Guard_HS1Guard, bigfile, expectedBytes, logfile))
    # if test_type == "Short 1 Guard & HS 3 Guard":
        # os.system("torperf/trivsocks-client %s 127.0.0.1:%i %s %i >> %s 2>/dev/null"%(server, SocksPort_short1Guard_HS3Guard, bigfile, expectedBytes, logfile))
    # if test_type == "Vanilla 1 Guard & HS 1 Guard":
    #     os.system("torperf/trivsocks-client %s 127.0.0.1:%i %s %i >> %s 2>/dev/null"%(server, SocksPort_vanilla1Guard_HS1Guard, bigfile, expectedBytes, logfile))
    # if test_type == "Vanilla 1 Guard & HS 3 Guard":
    #     os.system("torperf/trivsocks-client %s 127.0.0.1:%i %s %i >> %s 2>/dev/null"%(server, SocksPort_vanilla1Guard_HS3Guard, bigfile, expectedBytes, logfile))
