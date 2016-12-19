from random import random, randint, choice, sample
import collections
import os
from models import *
import hs_event_callbacks
import pathsim
from stem import Flag

NOPORT = 100

class CircuitCreationGiveUP(Exception):
    pass


def client_assign_rendezvous_stream(client_state, stream, cons_rel_stats,
    cons_valid_after, cons_fresh_until, cons_bw_weights, cons_bwweightscale,
    descriptors, hibernating_status, stream_weighted_exits,
    weighted_middles, weighted_guards, congmodel, pdelmodel, callbacks=None):
    """Assigns a stream to a circuit for a given client."""

    guards = client_state['guards']
    stream_assigned = None

    # try to use a dirty circuit
    for circuit in client_state['dirty_exit_circuits']:
        if (circuit['dirty_time'] > \
                stream['time'] - pathsim.TorOptions.max_circuit_dirtiness):
                #  and pathsim.circuit_supports_stream(circuit, stream, descriptors):
            if not circuit['internal']:
                if pathsim._testing:
                    print('client_assign_rendezvous_stream():'\
                    +'Found dirty Circuit, but it\'s not internal.\n')
                continue
            stream_assigned = circuit
            if pathsim._testing:
                print('client_assign_rendezvous_stream():'\
                +'Dirty Circuit uses %s Exit-Relay as last Hop.\n' %\
                (('an' if Flag.EXIT in cons_rel_stats[circuit['path'][-1]].flags else 'no')))
                if (stream['type'] == 'connect'):
                    print('Assigned CONNECT stream to port {0} to'.format(stream['port'])
                    + 'dirty circuit at {0}'.format(stream['time']))
                elif (stream['type'] == 'resolve'):
                    print('Assigned RESOLVE stream to dirty circuit \
                    at {0}'.format(stream['time']))
                else:
                    print('Assigned unrecognized stream to dirty circuit \
                    at {0}'.format(stream['time']))
            break
    # next try and use a clean circuit
    if (stream_assigned == None):
        new_clean_exit_circuits = collections.deque()
        while (len(client_state['clean_exit_circuits']) > 0):
            circuit = client_state['clean_exit_circuits'].popleft()
            if not circuit['internal']:
                if pathsim._testing:
                    print('client_assign_rendezvous_stream():'\
                    +'Found clean Circuit, but it\'s not internal.\n')
                new_clean_exit_circuits.append(circuit)
                continue
            # if (pathsim.circuit_supports_stream(circuit, stream, descriptors)):
            stream_assigned = circuit
            circuit['dirty_time'] = stream['time']
            client_state['dirty_exit_circuits'].appendleft(circuit)
            new_clean_exit_circuits.extend(\
                client_state['clean_exit_circuits'])
            client_state['clean_exit_circuits'].clear()
            if pathsim._testing:
                print('client_assign_rendezvous_stream():'\
                +'Clean Circuit uses %s Exit-Relay as last Hop.\n' %\
                (('an' if Flag.EXIT in cons_rel_stats[circuit['path'][-1]].flags else 'no')))
                if (stream['type'] == 'connect'):
                    print('Assigned CONNECT stream to port {0} to'.format(stream['port'])
                    + 'clean circuit at {0}'.format(stream['time']))
                elif (stream['type'] == 'resolve'):
                    print('Assigned RESOLVE stream to clean circuit \
                    at {0}'.format(stream['time']))
                else:
                    print('Assigned unrecognized stream to clean circuit \
                    at {0}'.format(stream['time']))

            # reduce cover count for covered port needs
            pathsim.uncover_circuit_ports(circuit,\
                client_state['port_needs_covered'])
            # else:
            #     pathsim.new_clean_exit_circuits.append(circuit)
        client_state['clean_exit_circuits'] =\
            new_clean_exit_circuits
    # if stream still unassigned we must make new circuit
    if (stream_assigned == None):
        new_circ = None
        if (stream['type'] == 'connect'):
            stable = (stream['port'] in pathsim.TorOptions.long_lived_ports)
            new_circ = create_circuit(False, cons_rel_stats,
                cons_valid_after, cons_fresh_until,
                cons_bw_weights, cons_bwweightscale,
                descriptors, hibernating_status, guards, stream['time'], True,
                stable, True, stream['ip'], stream['port'],
                congmodel, pdelmodel, stream_weighted_exits, False,
                weighted_middles, weighted_guards, callbacks)
        elif (stream['type'] == 'resolve'):
            new_circ = create_circuit(False, cons_rel_stats,
                cons_valid_after, cons_fresh_until,
                cons_bw_weights, cons_bwweightscale,
                descriptors, hibernating_status, guards, stream['time'], True,
                False, True, None, None, congmodel, pdelmodel,
                stream_weighted_exits, True,
                weighted_middles, weighted_guards, callbacks)
        else:
            raise ValueError('Unrecognized stream in client_assign_stream(): \
            {0}'.format(stream['type']))
        new_circ['dirty_time'] = stream['time']
        stream_assigned = new_circ
        client_state['dirty_exit_circuits'].appendleft(new_circ)
        if pathsim._testing:
            print('client_assign_rendezvous_stream():'\
            +'New Circuit uses %s Exit-Relay as last Hop.\n' %\
            (('an' if Flag.EXIT in cons_rel_stats[new_circ['path'][-1]].flags else 'no')))
            if (stream['type'] == 'connect'):
                print('Created circuit at time {0} to cover CONNECT \
                stream to ip {1} and port {2}.'.format(stream['time'], stream['ip'],\
                stream['port']))
            elif (stream['type'] == 'resolve'):
                print('Created circuit at time {0} to cover RESOLVE \
                stream.'.format(stream['time']))
            else:
                print('Created circuit at time {0} to cover unrecognized \
                stream.'.format(stream['time']))

    # if (callbacks is not None):
    #     callbacks.stream_assignment(stream, stream_assigned)

    return stream_assigned

def can_extend_to(circuit, extend, descriptors):
    path = circuit['path']
    desc2 = descriptors[extend]
    fprint2 = desc2.fingerprint
    nick2 = desc2.nickname
    ip2 = desc2.address

    if pathsim._testing:
        print("can_extend_to(): Will check against RP [{0}]".format(desc2.fingerprint))

    for i in range(len(path)):
        desc1 = descriptors[path[i]]
        fprint1 = desc1.fingerprint
        nick1 = desc1.nickname
        ip1 = desc1.address
        if pathsim._testing:
            print("can_extend_to(): Will check RP against {0}-th Relay [{1}] in Circuit"\
            .format(i, desc1.fingerprint))

        if fprint1 == fprint2:
            if pathsim._testing:
                print("can_extend_to(): Relay in Circuit from HS to RP equals RP.")
            return False
        else:
            if (pathsim.in_same_family(descriptors, fprint1, fprint2) or\
                pathsim.in_same_16_subnet(ip1, ip2)):
                if pathsim._testing:
                    print("can_extend_to(): Relay in Circuit from HS to RP is in same family or same \16-subnet as RP.")
                return False
    if pathsim._testing:
        print("can_extend_to(): Everything okay.")
    return True


def hs_assign_rendezvous_stream(hs_state, stream, rp, cons_rel_stats,
    cons_valid_after, cons_fresh_until, cons_bw_weights, cons_bwweightscale,
    descriptors, hibernating_status, stream_weighted_exits,
    weighted_middles, weighted_guards, congmodel, pdelmodel, callbacks=None):
    """Assigns a stream to a circuit for a given client."""

    guards = hs_state['guards']
    stream_assigned = None

    if pathsim._testing:
        print('{0} [{1}] will be used as the rendezvous point (RP).'\
        .format(rp, stream['ip']))

    # try to use a dirty circuit
    for circuit in hs_state['dirty_exit_circuits']:
        if not circuit['internal']:
            if pathsim._testing:
                print('hs_assign_rendezvous_stream():'\
                +'Found dirty Circuit, but it\'s not internal\n')
            continue
        if not can_extend_to(circuit, rp, descriptors):
            if pathsim._testing:
                print('hs_assign_rendezvous_stream():'\
                +'Found dirty Circuit, but we can\'t extend the rp to it.\n')
            continue
        if (circuit['dirty_time'] > \
                stream['time'] - pathsim.TorOptions.max_circuit_dirtiness):
                # and pathsim.circuit_supports_stream(circuit, stream, descriptors):
            stream_assigned = circuit
            if pathsim._testing:
                print('hs_assign_rendezvous_stream():'\
                +'Dirty Circuit uses %s Exit-Relay as last Hop.\n' %\
                (('an' if Flag.EXIT in cons_rel_stats[circuit['path'][-1]].flags else 'no')))
                if (stream['type'] == 'connect'):
                    print('Assigned CONNECT stream to port {0} to'.format(stream['port'])
                    + 'dirty circuit at {0}'.format(stream['time']))
                elif (stream['type'] == 'resolve'):
                    print('Assigned RESOLVE stream to dirty circuit \
                    at {0}'.format(stream['time']))
                else:
                    print('Assigned unrecognized stream to dirty circuit \
                    at {0}'.format(stream['time']))
            break

    # next try and use a clean circuit
    if (stream_assigned == None):
        new_clean_exit_circuits = collections.deque()
        while (len(hs_state['clean_exit_circuits']) > 0):
            circuit = hs_state['clean_exit_circuits'].popleft()
            if not circuit['internal']:
                if pathsim._testing:
                    print('hs_assign_rendezvous_stream():'\
                    +'Found clean Circuit, but it\'s not internal.\n')
                new_clean_exit_circuits.append(circuit)
                continue
            if not can_extend_to(circuit, rp, descriptors):
                if pathsim._testing:
                    print('hs_assign_rendezvous_stream():'\
                    +'Found clean Circuit, but we can\'t extend the RP to it.\n')
                new_clean_exit_circuits.append(circuit)
                continue
            # if (pathsim.circuit_supports_stream(circuit, stream, descriptors)):
            stream_assigned = circuit
            circuit['dirty_time'] = stream['time']
            hs_state['dirty_exit_circuits'].appendleft(circuit)
            new_clean_exit_circuits.extend(\
                hs_state['clean_exit_circuits'])
            hs_state['clean_exit_circuits'].clear()
            if pathsim._testing:
                print('hs_assign_rendezvous_stream():'\
                +'Clean Circuit uses %s Exit-Relay as last Hop.\n' %\
                (('an' if Flag.EXIT in cons_rel_stats[circuit['path'][-1]].flags else 'no')))
                if (stream['type'] == 'connect'):
                    print('Assigned CONNECT stream to port {0} to'.format(stream['port'])
                    + 'clean circuit at {0}'.format(stream['time']))
                elif (stream['type'] == 'resolve'):
                    print('Assigned RESOLVE stream to clean circuit \
                    at {0}'.format(stream['time']))
                else:
                    print('Assigned unrecognized stream to clean circuit \
                    at {0}'.format(stream['time']))

            # reduce cover count for covered port needs
            pathsim.uncover_circuit_ports(circuit,\
                hs_state['port_needs_covered'])
            # else:
            #    pathsim.new_clean_exit_circuits.append(circuit)
        hs_state['clean_exit_circuits'] =\
            new_clean_exit_circuits
    # if stream still unassigned we must make new circuit
    if (stream_assigned == None):
        if (stream['type'] == 'connect'):
            stable = (stream['port'] in pathsim.TorOptions.long_lived_ports)
            for num_attempts in range((pathsim.TorOptions.max_rend_failures
                * pathsim.TorOptions.max_circuit_failures)):
                new_circ = create_circuit(True, cons_rel_stats,
                    cons_valid_after, cons_fresh_until,
                    cons_bw_weights, cons_bwweightscale,
                    descriptors, hibernating_status, guards, stream['time'], True,
                    stable, True, stream['ip'], stream['port'],
                    congmodel, pdelmodel, stream_weighted_exits, False,
                    weighted_middles, weighted_guards, callbacks)
                if can_extend_to(new_circ, rp, descriptors):
                    break
            else:
                raise CircuitCreationGiveUP('hs_assign_rendezvous_stream(): Could not'\
                + ' create new Circuit in {0} attempts for rend stream.'\
                .format(num_attempts+1))
            if pathsim._testing:
                print('hs_assign_rendezvous_stream(): Chose new Circuit'\
                + ' in {0} attempts for rend stream.'.format(num_attempts+1))
        elif (stream['type'] == 'resolve'):
            for num_attempts in range((pathsim.TorOptions.max_rend_failures
                * pathsim.TorOptions.max_circuit_failures)):
                new_circ = create_circuit(True, cons_rel_stats,
                    cons_valid_after, cons_fresh_until,
                    cons_bw_weights, cons_bwweightscale,
                    descriptors, hibernating_status, guards, stream['time'], True,
                    False, True, None, None, congmodel, pdelmodel,
                    rp, True,
                    weighted_middles, weighted_guards, callbacks)
                if can_extend_to(new_circ, rp, descriptors):
                    break
            else:
                raise CircuitCreationGiveUP('hs_assign_rendezvous_stream(): Could not'\
                + ' create new Circuit in {0} attempts for rend stream.'\
                .format(num_attempts+1))
            if pathsim._testing:
                print('hs_assign_rendezvous_stream(): Chose new Circuit'\
                + ' in {0} attempts for rend stream.'.format(num_attempts+1))
        else:
            raise ValueError('Unrecognized stream in hs_assign_rendezvous_stream(): \
            {0}'.format(stream['type']))
        new_circ['dirty_time'] = stream['time']
        stream_assigned = new_circ
        hs_state['dirty_exit_circuits'].appendleft(new_circ)
        if pathsim._testing:
            print('hs_assign_rendezvous_stream():'\
            +'New Circuit uses %s Exit-Relay as last Hop.\n' %\
            (('an' if Flag.EXIT in cons_rel_stats[new_circ['path'][-1]].flags else 'no')))
            if (stream['type'] == 'connect'):
                print('Created circuit at time {0} to cover CONNECT \
                stream to ip {1} and port {2}.'.format(stream['time'], stream['ip'],\
                stream['port']))
            elif (stream['type'] == 'resolve'):
                print('Created circuit at time {0} to cover RESOLVE \
                stream.'.format(stream['time']))
            else:
                print('Created circuit at time {0} to cover unrecognized \
                stream.'.format(stream['time']))

    # if (callbacks is not None):
    #     callbacks.stream_assignment(stream, stream_assigned)

    return stream_assigned


def stream_update_port_needs(stream, port_needs_global,
    port_need_weighted_exits, client_states,
    descriptors, cons_rel_stats, cons_bw_weights, cons_bwweightscale):
    """Updates port needs based on input stream.
    If new port, returns updated list of exits filtered for port."""
    if (stream['type'] == 'resolve'):
        # as in Tor, treat RESOLVE requests as port 80 for
        #  prediction (see rep_hist_note_used_resolve())
        port = 80
    else:
        port = stream['port']
    if (port in port_needs_global):
        if (port_needs_global[port]['expires'] != None) and\
            (port_needs_global[port]['expires'] <\
                stream['time'] + pathsim.TorOptions.port_need_lifetime):
            port_needs_global[port]['expires'] =\
                stream['time'] + pathsim.TorOptions.port_need_lifetime
        return None
    else:
        if pathsim._testing:
            print('Will add Port {0} for global needed {1} Circuits.'\
            .format(port,
            'internal' if port==NOPORT else 'external'))
        port_needs_global[port] = {
            'expires':(stream['time']+pathsim.TorOptions.port_need_lifetime),
            'fast':True,
            'internal':(True if port==NOPORT else False),
            'stable':(port in pathsim.TorOptions.long_lived_ports),
            'cover_num':pathsim.TorOptions.port_need_cover_num}
        # adjust cover counts for the new port need
        for client_state in client_states:
            client_state['port_needs_covered'][port] = 0
            for circuit in client_state['clean_exit_circuits']:
                if (pathsim.circuit_covers_port_need(circuit,\
                        descriptors, port,\
                        port_needs_global[port])):
                    client_state['port_needs_covered'][port]\
                        += 1
                    circuit['covering'].add(port)
        # precompute exit list and weights for new port need
        port_need_exits = pathsim.filter_exits(cons_rel_stats,\
            descriptors, port_needs_global[port]['fast'],\
            port_needs_global[port]['stable'],
            port_needs_global[port]['internal'],\
            None, port)
        if pathsim._testing:
            print('# exits for new need at port {0}: {1}'.\
                format(port, len(port_need_exits)))
        if port==NOPORT:
            port_need_exit_weights = pathsim.get_position_weights(\
                port_need_exits, cons_rel_stats, 'm',\
                cons_bw_weights, cons_bwweightscale)
        else:
            port_need_exit_weights = pathsim.get_position_weights(\
                port_need_exits, cons_rel_stats, 'e',\
                cons_bw_weights, cons_bwweightscale)
        pn_weighted_exits = \
            pathsim.get_weighted_nodes(port_need_exits, port_need_exit_weights)
        port_need_weighted_exits[port] = pn_weighted_exits


def timed_client_updates(is_hs, cur_time, client_state, port_needs_global,
    cons_rel_stats, cons_valid_after,
    cons_fresh_until, cons_bw_weights, cons_bwweightscale, descriptors,
    hibernating_status, port_need_weighted_exits, weighted_middles,
    weighted_guards, congmodel, pdelmodel, callbacks=None):
    """Performs updates to client state that occur on a time schedule."""

    guards = client_state['guards']

    # kill old dirty circuits
    while (len(client_state['dirty_exit_circuits'])>0) and\
            (client_state['dirty_exit_circuits'][-1]['dirty_time'] <=\
                cur_time - pathsim.TorOptions.max_circuit_dirtiness):
        if pathsim._testing:
            print('Killed dirty exit circuit at time {0} w/ dirty time \
            {1}'.format(cur_time, client_state['dirty_exit_circuits'][-1]['dirty_time']))
        client_state['dirty_exit_circuits'].pop()

    # kill old clean circuits
    while (len(client_state['clean_exit_circuits'])>0) and\
            (client_state['clean_exit_circuits'][-1]['time'] <=\
                cur_time - pathsim.TorOptions.circuit_idle_timeout):
        if pathsim._testing:
            print('Killed clean exit circuit at time {0} w/ time \
            {1}'.format(cur_time, client_state['clean_exit_circuits'][-1]['time']))
        pathsim.uncover_circuit_ports(client_state['clean_exit_circuits'][-1],\
            client_state['port_needs_covered'])
        client_state['clean_exit_circuits'].pop()

    # kill circuits with relays that have gone into hibernation
    pathsim.kill_circuits_by_relay(client_state, \
        lambda r: hibernating_status[r], 'is hibernating')

    # cover uncovered ports while fewer than
    # TorOptions.max_unused_open_circuits clean
    for port, need in port_needs_global.items():
        if (client_state['port_needs_covered'][port] < need['cover_num']):
            # we need to make new circuits
            # note we choose circuits specifically to cover all port needs,
            #  while Tor makes one circuit (per sec) that covers *some* port
            #  (see circuit_predict_and_launch_new() in circuituse.c)
            if pathsim._testing:
                print('Creating {0} {1} circuit(s) at time {2} to cover port \
                {3}.'.format(need['cover_num']-client_state['port_needs_covered'][port],\
                'internal' if need['internal'] else 'external',\
                cur_time, port))
            while (client_state['port_needs_covered'][port] <\
                    need['cover_num']) and\
                (len(client_state['clean_exit_circuits']) < \
                    pathsim.TorOptions.max_unused_open_circuits):
                new_circ = create_circuit(is_hs, cons_rel_stats,
                    cons_valid_after, cons_fresh_until,
                    cons_bw_weights, cons_bwweightscale,
                    descriptors, hibernating_status, guards, cur_time,
                    need['fast'], need['stable'], need['internal'], None, port,
                    congmodel, pdelmodel,
                    port_need_weighted_exits[port],
                    True, weighted_middles, weighted_guards, callbacks)
                client_state['clean_exit_circuits'].appendleft(new_circ)

                # cover this port and any others
                client_state['port_needs_covered'][port] += 1
                new_circ['covering'].add(port)
                for pt, nd in port_needs_global.items():
                    if (pt != NOPORT) and (pt != port) and\
                        (pathsim.circuit_covers_port_need(new_circ,
                            descriptors, pt, nd)):
                        client_state['port_needs_covered'][pt] += 1
                        new_circ['covering'].add(pt)

def get_guards_for_circ(is_hs, bw_weights, bwweightscale, cons_rel_stats,\
    descriptors, fast, stable, guards,\
    exit,\
    circ_time, weighted_guards=None):
    """Obtains needed number of live guards that will work for circuit.
    Chooses new guards if needed, and *modifies* guard list by adding them."""
    # Get live guards then add new ones until TorOptions.num_guards reached,
    # where live is
    #  - bad_since isn't set
    #  - unreachable_since isn't set without retry
    #  - has descriptor, though create_circuits should ensure descriptor exists
    # Note that node need not have Valid flag to be live. As far as I can tell,
    # a Valid flag is needed to be added to the guard list, but isn't needed
    # after that point.
    # Note that hibernating status is not an input here.
    # Rules derived from Tor source: choose_random_entry_impl() in entrynodes.c

    if is_hs:
        num_guards = pathsim.TorOptions.num_hs_guards
        min_num_guards = pathsim.TorOptions.min_num_hs_guards
        guard_expiration_min = pathsim.TorOptions.hs_guard_expiration_min
        guard_expiration_max = pathsim.TorOptions.hs_guard_expiration_max
    elif not is_hs:
        num_guards = pathsim.TorOptions.num_client_guards
        min_num_guards = pathsim.TorOptions.min_num_client_guards
        guard_expiration_min = pathsim.TorOptions.client_guard_expiration_min
        guard_expiration_max = pathsim.TorOptions.client_guard_expiration_max

    # add guards if not enough in list
    if (len(guards) < num_guards):
        # Oddly then only count the number of live ones
        # Slightly depart from Tor code by not considering the circuit's
        # fast or stable flags when finding live guards.
        # Tor uses fixed Stable=False and Fast=True flags when calculating #
        # live but fixed Stable=Fast=False when adding guards here (weirdly).
        # (as in choose_random_entry_impl() and its pick_entry_guards() call)
        live_guards = filter(lambda x: (guards[x]['bad_since']==None) and\
                            (x in descriptors) and\
                            ((guards[x]['unreachable_since'] == None) or\
                             pathsim.guard_is_time_to_retry(guards[x],circ_time)),\
                             guards)
        for i in range(num_guards - len(live_guards)):
            new_guard = pathsim.get_new_guard(bw_weights, bwweightscale,\
                cons_rel_stats, descriptors, guards,\
                weighted_guards)
            if pathsim._testing:
                print('Need {0} more guard(s). Adding {1} [{2}]'.format(\
                    (num_guards-len(guards)),
                    cons_rel_stats[new_guard].nickname, new_guard))
            expiration = randint(guard_expiration_min,\
                guard_expiration_max)
            guards[new_guard] = {'expires':(expiration+\
                circ_time), 'bad_since':None, 'unreachable_since':None,\
                'last_attempted':0, 'made_contact':False}
            if pathsim._testing:
                print("New Guard [{0}] with expiration in {1} days"\
                    .format(new_guard, expiration/(24*60*60)))
        if pathsim._testing:
            print("Guards of {0}: {1}"\
            .format(("client" if not is_hs else "hs"), guards.keys()))

    # check for guards that will work for this circuit
    guards_for_circ = filter(lambda x: pathsim.guard_filter_for_circ(x,\
        cons_rel_stats, descriptors, fast, stable, exit, circ_time, guards),\
        guards)
    # add new guards while there aren't enough for this circuit
    # adding is done without reference to the circuit - how Tor does it
    while (len(guards_for_circ) < min_num_guards):
            if pathsim._testing:
                print("Guards of {0}: {1}"\
                .format(("client" if not is_hs else "hs"), guards.keys()))
            new_guard = pathsim.get_new_guard(bw_weights, bwweightscale,\
                cons_rel_stats, descriptors, guards,\
                weighted_guards)
            if pathsim._testing:
                print('Need guard for circuit. Adding {0} [{1}]'.format(\
                    cons_rel_stats[new_guard].nickname, new_guard))
            expiration = randint(guard_expiration_min,\
                guard_expiration_max)
            guards[new_guard] = {'expires':(expiration+\
                circ_time), 'bad_since':None, 'unreachable_since':None,\
                'last_attempted':0, 'made_contact':False}
            if (pathsim.guard_filter_for_circ(new_guard, cons_rel_stats, descriptors,\
                fast, stable, exit, circ_time, guards)):
                guards_for_circ.append(new_guard)
            if pathsim._testing:
                print("New Guard [{0}] with expiration in {1} days"\
                    .format(new_guard, expiration/(24*60*60)))


    # return first TorOptions.num_guards usable guards
    return guards_for_circ[0:num_guards]


def select_exit_node(bw_weights, bwweightscale, cons_rel_stats, descriptors,\
    fast, stable, internal, ip, port, weighted_exits=None, exits_exact=False):
    """Chooses a valid exit node. To improve performance when simulating many
    streams, we allow any input weighted_exits list to possibly include
    relays that are invalid for the current circuit (thus we can create
    weighted_exits less often by only considering the port instead of the
    ip/port). Then we randomly select from that list until a suitable exit is
    found.
    """
    if (weighted_exits == None):
        # filter exit list
        exits = pathsim.filter_exits(cons_rel_stats, descriptors, fast,\
            stable, internal, ip, port)
        # create weights
        weights = None
        if (internal):
            weights = pathsim.get_position_weights(exits, cons_rel_stats, 'm',\
                        bw_weights, bwweightscale)
        else:
            weights = pathsim.get_position_weights(exits, cons_rel_stats, 'e',\
                bw_weights, bwweightscale)
        weighted_exits = pathsim.get_weighted_nodes(exits, weights)
        exits_exact = True

    if (exits_exact):
        # i = 1
        # while True:
        exit_node = pathsim.select_weighted_node(weighted_exits)
        # i += 1
        # if (internal and Flag.EXIT in cons_rel_stats[exit_node].flags):
        #     continue
        if pathsim._testing:
            print('select_exit_node() for {0} Circuit made choice. Got {1} Exit-Flag.'\
            .format(('internal' if internal else 'external'),
                    ('an' if Flag.EXIT in cons_rel_stats[exit_node].flags else 'no')))
        return exit_node
    else:
        # select randomly until acceptable exit node is found
        i = 1
        while True:
            exit_node = pathsim.select_weighted_node(weighted_exits)
            i += 1
            # if (internal and Flag.EXIT in cons_rel_stats[exit_node].flags):
            #     continue
            if pathsim._testing:
                print('select_exit_node() for {0} Circuit made choice #{1}. Got {2} Exit-Flag.'\
                .format(('internal' if internal else 'external'),
                        i,
                        ('an' if Flag.EXIT in cons_rel_stats[exit_node].flags else 'no')))
            if (pathsim.exit_filter(exit_node, cons_rel_stats, descriptors, fast,\
                stable, internal, ip, port, False)):
                return exit_node

def get_stream_port_weighted_exits(stream_port, stream,
    cons_rel_stats, descriptors, cons_bw_weights, cons_bwweightscale):
    """Returns weighted exit list for port of stream."""
    if (stream['type'] == 'connect'):
        stable = (stream_port in pathsim.TorOptions.long_lived_ports)
        internal = (stream_port==NOPORT)
        stream_exits =\
            pathsim.filter_exits_loose(cons_rel_stats,\
                descriptors, True, stable, internal,\
                None, stream_port)
        if pathsim._testing:
            print('# loose exits for stream on port {0}: {1}'.\
                format(stream_port, len(stream_exits)))
    elif (stream['type'] == 'resolve'):
        stream_exits =\
            pathsim.filter_exits(cons_rel_stats, descriptors, True,\
                False, False, None, None)
        if pathsiim._testing:
            print('# exits for RESOLVE stream: {0}'.\
                format(len(stream_exits)))
    else:
        raise ValueError(\
            'ERROR: Unrecognized stream type: {0}'.\
            format(stream['type']))
    if stream_port==NOPORT: # Circuit Internal:
        stream_exit_weights = pathsim.get_position_weights(\
            stream_exits, cons_rel_stats, 'm',\
            cons_bw_weights, cons_bwweightscale)
    else:
        stream_exit_weights = pathsim.get_position_weights(\
            stream_exits, cons_rel_stats, 'e',\
            cons_bw_weights, cons_bwweightscale)
    stream_weighted_exits = pathsim.get_weighted_nodes(\
        stream_exits, stream_exit_weights)
    return stream_weighted_exits


def create_circuit(is_hs, cons_rel_stats, cons_valid_after, cons_fresh_until,
    cons_bw_weights, cons_bwweightscale, descriptors, hibernating_status,
    guards, circ_time, circ_fast, circ_stable, circ_internal, circ_ip,
    circ_port, congmodel, pdelmodel, weighted_exits=None,
    exits_exact=False, weighted_middles=None, weighted_guards=None,
    callbacks=None):
    """Creates path for requested circuit based on the input consensus
    statuses and descriptors.
    Inputs:
        cons_rel_stats: (dict) relay fingerprint keys and relay status vals
        cons_valid_after: (int) timestamp of valid_after for consensus
        cons_fresh_until: (int) timestamp of fresh_until for consensus
        cons_bw_weights: (dict) bw_weights of consensus
        cons_bwweightscale: (should be float()able) bwweightscale of consensus
        descriptors: (dict) relay fingerprint keys and descriptor vals
        hibernating_status: (dict) indicates hibernating relays
        guards: (dict) contains guards of requesting client
        circ_time: (int) timestamp of circuit request
        circ_fast: (bool) all relays should be fast
        circ_stable: (bool) all relays should be stable
        circ_internal: (bool) circuit is for name resolution or hidden service
        circ_ip: (str) IP address of destination (None if not known)
        circ_port: (int) desired TCP port (None if not known)
        congmodel: congestion model
        pdelmodel: propagation delay model
        weighted_exits: (list) (middle, cum_weight) pairs for exit position
        exits_exact: (bool) Is weighted_exits exact or does it need rechecking?
            weighed_exits is special because exits are chosen first and thus
            don't depend on the other circuit positions, and so potentially are
            precomputed exactly.
        weighted_middles: (list) (middle, cum_weight) pairs for middle position
        weighted_guards: (list) (middle, cum_weight) pairs for middle position
        callbacks: object w/ method circuit_creation(circuit)
    Output:
        circuit: (dict) a newly created circuit with keys
            'time': (int) seconds from time zero
            'fast': (bool) relays must have Fast flag
            'stable': (bool) relays must have Stable flag
            'internal': (bool) is internal (e.g. for hidden service)
            'dirty_time': (int) timestamp of time dirtied, None if clean
            'path': (tuple) list in-order fingerprints for path's nodes
            'covering': (set) ports with needs covered by circuit
    """

    if (circ_time < cons_valid_after) or\
        (circ_time >= cons_fresh_until):
        raise ValueError('consensus not fresh for circ_time in create_circuit')

    num_attempts = 0
    ntor_supported = False
    while (num_attempts < pathsim.TorOptions.max_populate_attempts) and\
        (not ntor_supported):
        # select exit node
        i = 1
        while (True):
            exit_node = select_exit_node(cons_bw_weights, cons_bwweightscale,\
                cons_rel_stats, descriptors, circ_fast, circ_stable,\
                circ_internal, circ_ip, circ_port, weighted_exits, exits_exact)
    #        exit_node = select_weighted_node(weighted_exits)
            if (not hibernating_status[exit_node]):
                break
            if pathsim._testing:
                print('Exit selection #{0} is hibernating - retrying.'.\
                    format(i))
            i += 1
        if pathsim._testing:
            print('Exit node: {0} [{1}]'.format(
                cons_rel_stats[exit_node].nickname,
                cons_rel_stats[exit_node].fingerprint))

        # select guard node
        # Hibernation status again checked here to reflect how in Tor
        # new guards would be chosen and added to the list prior to a circuit-
        # creation attempt. If the circuit fails at a new guard, that guard
        # gets removed from the list.
        while True:
            # get first <= TorOptions.num_guards guards suitable for circuit
            circ_guards = get_guards_for_circ(is_hs, cons_bw_weights,\
                cons_bwweightscale, cons_rel_stats, descriptors,\
                circ_fast, circ_stable, guards,\
                exit_node,\
                circ_time, weighted_guards)
            guard_node = choice(circ_guards)
            if (hibernating_status[guard_node]):
                if (not guards[guard_node]['made_contact']):
                    del guards[guard_node]
                    if pathsim._testing:
                        print('[Time {0}]: Removed new hibernating guard: {1}.'\
                            .format(circ_time,
                                cons_rel_stats[guard_node].nickname))
                elif (guards[guard_node]['unreachable_since'] != None):
                    guards[guard_node]['last_attempted'] = circ_time
                    if pathsim._testing:
                        print('[Time {0}]: Guard retried but hibernating: {1}'.\
                            format(circ_time,
                                cons_rel_stats[guard_node].nickname))
                else:
                    guards[guard_node]['unreachable_since'] = circ_time
                    guards[guard_node]['last_attempted'] = circ_time
                    if pathsim._testing:
                        print('[Time {0}]: Guard newly hibernating: {1}'.\
                            format(circ_time,
                                cons_rel_stats[guard_node].nickname))
            else:
                guards[guard_node]['unreachable_since'] = None
                guards[guard_node]['made_contact'] = True
                break
        if pathsim._testing:
            print('Guard node: {0} [{1}]'.format(
                cons_rel_stats[guard_node].nickname,
                cons_rel_stats[guard_node].fingerprint))

        # select middle node
        # As with exit selection, hibernating status checked here to mirror Tor
        # selecting middle, having the circuit fail, reselecting a path,
        # and attempting circuit creation again.
        i = 1
        while (True):
            middle_node = pathsim.select_middle_node(cons_bw_weights,
                cons_bwweightscale, cons_rel_stats, descriptors, circ_fast,
                circ_stable, exit_node, guard_node, weighted_middles)
            if (not hibernating_status[middle_node]):
                break
            if pathsim._testing:
                print('Middle selection #{0} is hibernating - retrying.'.\
                    format(i))
            i += 1
        if pathsim._testing:
            print('Middle node: {0} [{1}]'.format(
                cons_rel_stats[middle_node].nickname,
                cons_rel_stats[middle_node].flags))

        # ensure one member of the circuit supports the ntor handshake
        ntor_supported = pathsim.circuit_supports_ntor(guard_node, middle_node,
            exit_node, descriptors)
        num_attempts += 1
    if pathsim._testing:
        if ntor_supported:
            print('Chose ntor-compatible circuit in {} tries'.\
                format(num_attempts))
    if (not ntor_supported):
        raise ValueError('ntor-compatible circuit not found in {} tries'.\
            format(num_attempts))

    circuit = {'time':circ_time,
            'fast':circ_fast,
            'stable':circ_stable,
            'internal':circ_internal,
            'dirty_time':None,
            'path':(guard_node, middle_node, exit_node),
            'covering':set()}

    # execute callback to allow logging on circuit creation
    if (callbacks is not None):
        callbacks.circuit_creation(circuit)

    return circuit

def create_circuits(network_states, streams, num_samples, congmodel,
    pdelmodel, callbacks=None):
    """Takes streams over time and creates circuits by interaction
    with create_circuit().
      Input:
        network_states: iterator yielding NetworkState objects containing
            the sequence of simulation network states, with a None value
            indicating most recent status should be repeated with consensus
            valid/fresh times advanced 60 minutes
        streams: *ordered* list of streams, where a stream is a dict with keys
            'time': timestamp of when stream request occurs
            'type': 'connect' for SOCKS CONNECT, 'resolve' for SOCKS RESOLVE
            'ip': IP address of destination
            'port': desired TCP port
        num_samples: (int) # circuit-creation samples to take for given streams
        congmodel: (CongestionModel) outputs congestion used by some path algs
        pdelmodel: (PropagationDelayModel) outputs prop delay
        callbacks: obj providing callback interface, cf. event_callbacks module
    Output:
        Uses callbacks to produce any desired output.
    """

    ### Simulation variables ###
    cur_period_start = None
    cur_period_end = None
    stream_start = 0
    stream_end = 0
    init = True
    # pathsim._testing = True

    # store old descriptors (for entry guards that leave consensus)
    # initialize with add_descriptors
    descriptors = {}

    port_needs_global = {}


    # print('_testing: {0}'.format(pathsim._testing))
    if pathsim._testing:
        print('num_client_guards: {0}\n\
        min_num_client_guards: {1}\n\
        client_guard_expiration_min: {2}\n\
        client_guard_expiration_max: {3}\n'\
        .format(pathsim.TorOptions.num_client_guards,
        pathsim.TorOptions.min_num_client_guards,
        (pathsim.TorOptions.client_guard_expiration_min/(24*60*60)),
        (pathsim.TorOptions.client_guard_expiration_max/(24*60*60))))

        print('num_hs_guards: {0}\n\
        min_num_hs_guards: {1}\n\
        hs_guard_expiration_min: {2}\n\
        hs_guard_expiration_max: {3}\n'\
        .format(pathsim.TorOptions.num_hs_guards,
        pathsim.TorOptions.min_num_hs_guards,
        (pathsim.TorOptions.hs_guard_expiration_min/(24*60*60)),
        (pathsim.TorOptions.hs_guard_expiration_max/(24*60*60))))

    # client states for each sample
    client_states = []
    # HS states for each sample
    hs_states = []
    for i in range(num_samples):
        # guard is dict with client guard state (expiration, bad_since, etc.)
        # port_needs are ports that must be covered by existing circuits
        # circuit vars are ordered by increasing time since create or dirty
        port_needs_covered = {}
        port_needs_covered_hs = {}
        client_states.append({'id':i,
                            'guards':{},
                            'port_needs_covered':port_needs_covered,
                            'clean_exit_circuits':collections.deque(),
                            'dirty_exit_circuits':collections.deque()})
        hs_states.append({'id':i,
                        'guards':{},
                        'port_needs_covered':port_needs_covered_hs,
                        'clean_exit_circuits':collections.deque(),
                        'dirty_exit_circuits':collections.deque()})
    ### End simulation variables ###

    # run simulation period one network state at a time
    for network_state in network_states:
        if (network_state != None):
            cons_valid_after = network_state.cons_valid_after
            cons_fresh_until = network_state.cons_fresh_until
            cons_bw_weights = network_state.cons_bw_weights
            cons_bwweightscale = network_state.cons_bwweightscale
            cons_rel_stats = network_state.cons_rel_stats
            hibernating_statuses = network_state.hibernating_statuses
            new_descriptors = network_state.descriptors

            if pathsim._testing:
                print(cons_bw_weights)


            # clear hibernating status to ensure updates come from ns_file
            hibernating_status = {}

            # update descriptors
            descriptors.update(new_descriptors)

        else:
            # gap in consensuses, just advance an hour, keeping network state
            cons_valid_after += 3600
            cons_fresh_until += 3600
            # set empty statuses, even though previous should have been emptied
            hibernating_statuses = []
            if pathsim._testing:
                print('Filling in consensus gap from {0} to {1}'.\
                format(cons_valid_after, cons_fresh_until))

        # update network state of callbacks object
        if (callbacks is not None):
            callbacks.set_network_state(cons_valid_after, cons_fresh_until,
                cons_bw_weights, cons_bwweightscale, cons_rel_stats,
                descriptors)

        # update simulation period
        if (cur_period_start == None):
            # first time, initial startup
            cur_period_start = cons_valid_after
        elif (cur_period_end == cons_valid_after):
            cur_period_start = cons_valid_after
        else:
            err = 'Gap/overlap in consensus times: {0}:{1}'.\
                    format(cur_period_end, cons_valid_after)
            raise ValueError(err)
        cur_period_end = cons_fresh_until

        # set initial hibernating status
        pathsim.set_initial_hibernating_status(hibernating_status,
            hibernating_statuses, cur_period_start, cons_rel_stats)

        if (init == True): # first period in simulation
            # seed port need
            port_needs_global[80] = \
                {'expires':(cur_period_start+pathsim.TorOptions.port_need_lifetime),
                'fast':True, 'stable':False, 'internal':False,
                'cover_num':pathsim.TorOptions.port_need_cover_num}
            port_needs_global[NOPORT] = \
                {'expires':(cur_period_start+pathsim.TorOptions.port_need_lifetime),
                'fast':True, 'stable':False, 'internal':True,
                'cover_num':pathsim.TorOptions.port_need_cover_num}
            for client_state in client_states:
                client_state['port_needs_covered'][80] = 0
                client_state['port_needs_covered'][NOPORT] = 0
            for hs_state in hs_states:
                hs_state['port_needs_covered'][80] = 0
                hs_state['port_needs_covered'][NOPORT] = 0
            init = False

        # Update client state based on relay status changes in new consensus by
        # updating guard list and killing existing circuits.
        for client_state in client_states:
            pathsim.period_client_update(client_state, cons_rel_stats,\
                cons_fresh_until, cons_valid_after)
        for hs_state in hs_states:
            pathsim.period_client_update(hs_state, cons_rel_stats,\
                cons_fresh_until, cons_valid_after)

        # filter exits for port needs and compute their weights
        # do this here to avoid repeating per client
        port_need_weighted_exits = {}
        for port, need in port_needs_global.items():
            port_need_exits = pathsim.filter_exits(cons_rel_stats, descriptors,\
                need['fast'], need['stable'], need['internal'], None, port)
            if pathsim._testing:
                print('# exits for port {0}: {1}'.\
                    format(port, len(port_need_exits)))
            if need['internal']:
                port_need_exit_weights = pathsim.get_position_weights(\
                    port_need_exits, cons_rel_stats, 'm', cons_bw_weights,\
                    cons_bwweightscale)
            else:
                port_need_exit_weights = pathsim.get_position_weights(\
                    port_need_exits, cons_rel_stats, 'e', cons_bw_weights,\
                    cons_bwweightscale)
            port_need_weighted_exits[port] =\
                pathsim.get_weighted_nodes(port_need_exits, port_need_exit_weights)

        # Store filtered exits for streams based only on port.
        # Conservative - never excludes a relay that exits to port for some ip.
        # Use port of None to store exits for resolve circuits.
        stream_port_weighted_exits = {}

        # filter middles and precompute cumulative weights
        potential_middles = filter(lambda x:  pathsim.middle_filter(x, cons_rel_stats,\
            descriptors, None, None, None, None), cons_rel_stats.keys())
        if pathsim._testing:
            print('# potential middles: {0}'.format(len(potential_middles)))
        potential_middle_weights = pathsim.get_position_weights(potential_middles,\
            cons_rel_stats, 'm', cons_bw_weights, cons_bwweightscale)
        weighted_middles = pathsim.get_weighted_nodes(potential_middles,\
            potential_middle_weights)

        # filter guards and precompute cumulative weights
        # New guards are selected infrequently after the experiment start
        # so doing this here instead of on-demand per client may actually
        # slow things down. We do it to improve scalability with sample number.
        potential_guards = pathsim.filter_guards(cons_rel_stats, descriptors)
        potential_guard_weights = pathsim.get_position_weights(potential_guards,\
            cons_rel_stats, 'g', cons_bw_weights, cons_bwweightscale)
        weighted_guards = pathsim.get_weighted_nodes(potential_guards,\
            potential_guard_weights)

        # for simplicity, step through time one minute at a time
        time_step = 60
        cur_time = cur_period_start
        while (cur_time < cur_period_end):
            # do updates that apply to all clients
            pathsim.timed_updates(cur_time, port_needs_global, client_states,
                hibernating_statuses, hibernating_status, cons_rel_stats)
            pathsim.timed_updates(cur_time, port_needs_global, hs_states,
                hibernating_statuses, hibernating_status, cons_rel_stats)

            # do timed individual client updates
            for client_state in client_states:
                if (callbacks is not None):
                    callbacks.set_sample_id(client_state['id'])

                timed_client_updates(False, cur_time, client_state,
                    port_needs_global, cons_rel_stats,
                    cons_valid_after, cons_fresh_until, cons_bw_weights,
                    cons_bwweightscale, descriptors, hibernating_status,
                    port_need_weighted_exits, weighted_middles,
                    weighted_guards, congmodel, pdelmodel, callbacks)
            for hs_state in hs_states:
               timed_client_updates(True, cur_time, hs_state,
                    port_needs_global, cons_rel_stats,
                    cons_valid_after, cons_fresh_until, cons_bw_weights,
                    cons_bwweightscale, descriptors, hibernating_status,
                    port_need_weighted_exits, weighted_middles,
                    weighted_guards, congmodel, pdelmodel, callbacks)

            # collect streams that occur during current period
            while (stream_start < len(streams)) and\
                (streams[stream_start]['time'] < cur_time):
                stream_start += 1
            stream_end = stream_start
            while (stream_end < len(streams)) and\
                (streams[stream_end]['time'] < cur_time + time_step):
                stream_end += 1

            # assign streams in this minute to circuits
            for stream_idx in range(stream_start, stream_end):
                stream = streams[stream_idx]

                # add need/extend expiration for ports in streams
                stream_update_port_needs(stream, port_needs_global,
                    port_need_weighted_exits, client_states, descriptors,
                    cons_rel_stats, cons_bw_weights, cons_bwweightscale)

                # stream port for purposes of using precomputed exit lists
                if (stream['type'] == 'resolve'):
                    stream_port = None
                else:
                    stream_port = stream['port']
                # create weighted exits for this stream's port
                if (stream_port not in stream_port_weighted_exits):
                    stream_port_weighted_exits[stream_port] =\
                        get_stream_port_weighted_exits(stream_port, stream,
                        cons_rel_stats, descriptors,
                        cons_bw_weights, cons_bwweightscale)

                # do client stream assignment
                for client_state, hs_state in zip(client_states, hs_states):
                    if (callbacks is not None):
                        callbacks.set_sample_id(client_state['id'])
                    if pathsim._testing:
                        print('Client {0} stream assignment.'.\
                            format(client_state['id']))
                    # client_guards = client_state['guards']
                    # hs_guards = hs_states['guards']


                    if stream['ip']== 'hiddenservice.onion':  # HiddenService
                        if pathsim._testing:
                            print('Client wants to connect to HiddenService.')

                        for num_attempts in range(pathsim.TorOptions.max_rend_client_attempts):
                            client_rendezvous_stream = client_assign_rendezvous_stream(
                                client_state, stream, cons_rel_stats,
                                cons_valid_after, cons_fresh_until,
                                cons_bw_weights, cons_bwweightscale,
                                descriptors, hibernating_status,
                                stream_port_weighted_exits[stream_port],
                                weighted_middles, weighted_guards,
                                congmodel, pdelmodel, callbacks)

                            rp = client_rendezvous_stream['path'][2]
                            stream['ip'] = descriptors[rp].address

                            try:
                                hs_rendezvous_stream = hs_assign_rendezvous_stream(\
                                    hs_state, stream, rp, cons_rel_stats,
                                    cons_valid_after, cons_fresh_until,
                                    cons_bw_weights, cons_bwweightscale,
                                    descriptors, hibernating_status,
                                    stream_port_weighted_exits[stream_port],
                                    weighted_middles, weighted_guards,
                                    congmodel, pdelmodel, callbacks)
                            except CircuitCreationGiveUP, e:
                                if pathsim._testing:
                                    print('create_circuits(): Could not assign HS'\
                                    + ' Rendezvous Stream: {0}'.format(e))
                                stream['ip'] = 'hiddenservice.onion'
                            else:
                                #if NO CircuitCreationGiveUP
                                break

                        else:
                            # if rend stream could not be assigned
                            if pathsim._testing:
                                print("create_circuits():"
                                    + "Could not assign Rend Stream to Client and HS in {} attempts"\
                                .format(num_attempts+1))
                            continue

                        if pathsim._testing:
                            print("create_circuits():"
                            + "Could assign Rend Stream to Client and HS in {} attempts"\
                            .format(num_attempts+1))

                        rendezvous_path = (client_rendezvous_stream['path'][0], #client guard
                        client_rendezvous_stream['path'][1], # client middle
                        client_rendezvous_stream['path'][2], # rp
                        hs_rendezvous_stream['path'][2], # hs exit
                        hs_rendezvous_stream['path'][1], # hs middle
                        hs_rendezvous_stream['path'][0]) # hs guard

                        stream['ip'] = 'hiddenservice.onion'
                        stream['path'] = rendezvous_path
                        rendezvous_circuit =  {'time':hs_rendezvous_stream['time'],
                                                'fast':hs_rendezvous_stream['fast'],
                                                'stable':hs_rendezvous_stream['stable'],
                                                'internal':hs_rendezvous_stream['internal'],
                                                'dirty_time':stream['time'],
                                                'path':rendezvous_path,
                                                'covering':set()}

                        if (callbacks is not None):
                            callbacks.rendezvous_stream_assignment(stream, rendezvous_circuit)

                    else:
                        if pathsim._testing:
                            print('Client wants to connect to {0}.'\
                            .format(stream['ip']))
                        stream_assigned =  pathsim.client_assign_stream(\
                        client_state, stream, cons_rel_stats,
                        cons_valid_after, cons_fresh_until,
                        cons_bw_weights, cons_bwweightscale,
                        descriptors, hibernating_status,
                        stream_port_weighted_exits[stream_port],
                        weighted_middles, weighted_guards,
                        congmodel, pdelmodel, callbacks)

            cur_time += time_step
