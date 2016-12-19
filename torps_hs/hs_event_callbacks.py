### Classes that provide callback interface:
#     set_network_state(cons_valid_after, cons_fresh_until, cons_bw_weights,
#         cons_bwweightscale, cons_rel_stats, descriptors): called every simulation period on new
#         consensus and descriptor data
#     set_sample_id(id): updates ID of current sample being executed
#     circuit_creation(circuit): called on successful circuit creation on circuit dict
#     stream_assignment(stream, circuit): called on assignment of stream to circuit
###

import sys

### Print just stream assignments in several possible formats ###
class PrintStreamAssignments(object):

    def __init__(self, format, testing, file=sys.stdout):
        self.format = format
        self.testing = testing
        self.file = file
        self.descriptors = None
        self.sample_id = None

    def print_header(self):
        """Prints log header for stream lines."""
        if self.testing:
            return
        if (self.format == 'testing'):
            pass
        elif (self.format == 'relay-adv'):
            self.file.write('Sample\tTimestamp\tClient Compromise Code\tHS Compromise Code\n')
        elif (self.format == 'network-adv'):
            self.file.write('Sample\tTimestamp\tGuard ip\tExit IP\tDestination IP\n')
        else:
            self.file.write('Sample\tTimestamp\tGuard IP\tMiddle IP\tExit IP\tDestination IP\n')

    def set_network_state(self, cons_valid_after, cons_fresh_until, cons_bw_weights,
        cons_bwweightscale, cons_rel_stats, descriptors):
        self.descriptors = descriptors

    def set_sample_id(self, id):
        self.sample_id = id

    def circuit_creation(self, circuit):
        pass

    def get_compromise_code(self, circuit):
        # as in network_modifiers.AdversaryInsertion.add_adv_guards()
        guard_prefix = '000000000000000000000000000000'
        # as in network_modifiers.AdversaryInsertion.add_adv_exits()
        exit_prefix = 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
        # as in network_modifiers.AdversaryInsertion.add_adv_exits()
        middle_prefix = 'F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0'
        guard_bad = False
        exit_bad = False
        middle_bad = False

        if (circuit[0][0:30] == guard_prefix) or\
            (circuit[0][0:30] == exit_prefix) or\
            (circuit[0][0:30] == middle_prefix):
            guard_bad = True
        if (circuit[1][0:30] == guard_prefix) or\
            (circuit[1][0:30] == exit_prefix) or\
            (circuit[1][0:30] == middle_prefix):
            middle_bad = True
        if (circuit[2][0:30] == guard_prefix) or\
            (circuit[2][0:30] == exit_prefix) or\
            (circuit[2][0:30] == middle_prefix):
            exit_bad = True

        compromise_code = 0
        if (guard_bad and middle_bad and exit_bad):
            compromise_code = 7
        elif (guard_bad and exit_bad):
            compromise_code = 6
        elif (guard_bad and middle_bad):
            compromise_code = 5
        elif (exit_bad and middle_bad):
            compromise_code = 4
        elif guard_bad:
            compromise_code = 1
        elif middle_bad:
            compromise_code = 2
        elif exit_bad:
            compromise_code = 3

        return compromise_code

    def stream_assignment(self, stream, circuit):
        """Writes log line to file (default stdout) showing client, time, IPs, and
        fingerprints in path of stream."""

        if self.testing:
            return

        if (circuit is None):
            if (self.format == 'testing'):
                pass
            else:
                self.file.write('{0}\t{1}\n'.format(self.sample_id, stream['time']))
        else:
            guard_ip = self.descriptors[circuit['path'][0]].address
            middle_ip = self.descriptors[circuit['path'][1]].address
            exit_ip = self.descriptors[circuit['path'][2]].address
            if (stream['type'] == 'connect'):
                dest_ip = stream['ip']
            elif (stream['type'] == 'resolve'):
                dest_ip = 0
            else:
                raise ValueError('ERROR: Unrecognized stream in stream_assignment(): {0}'.\
                    format(stream['type']))

            if (self.format == 'testing'):
                pass
            elif (self.format == 'relay-adv'):
                compromise_code = self.get_compromise_code(circuit['path'])
                self.file.write('{0}\t{1}\t{2}\n'.format(self.sample_id, stream['time'],
                    compromise_code))
            elif (self.format == 'network-adv'):
                self.file.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(self.sample_id, stream['time'],
                    guard_ip, exit_ip, dest_ip))
            else:
                self.file.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(self.sample_id,
                    stream['time'], guard_ip, middle_ip, exit_ip, dest_ip))



    def rendezvous_stream_assignment(self, stream, circuit):
        """Writes log line to file (default stdout) showing client, time, IPs, and
        fingerprints in path of stream."""

        if self.testing:
            return

        if (circuit is None):
            if (self.format == 'testing'):
                pass
            else:
                self.file.write('{0}\t{1}\n'.format(self.sample_id, stream['time']))
        else:
            if len(circuit['path'])!=6:
                raise ValueError('ERROR: Expected rendezvous Circuit.')
            else:
                client_circuit = circuit['path'][0:3]
                hs_circuit = tuple(reversed(circuit['path'][3:6]))


                cl_guard_ip = self.descriptors[client_circuit[0]].address
                cl_middle_ip = self.descriptors[client_circuit[1]].address
                rp_ip = self.descriptors[client_circuit[2]].address

                hs_guard_ip = self.descriptors[hs_circuit[0]].address
                hs_middle_ip = self.descriptors[hs_circuit[1]].address
                hs_exit_ip = self.descriptors[hs_circuit[2]].address

                if (stream['type'] == 'connect'):
                    dest_ip = stream['ip']
                elif (stream['type'] == 'resolve'):
                    dest_ip = 0
                else:
                    raise ValueError('ERROR: Unrecognized stream in stream_assignment(): {0}'.\
                        format(stream['type']))

                if (self.format == 'testing'):
                    pass
                elif (self.format == 'relay-adv'):
                    client_compromise_code = self.get_compromise_code(client_circuit)
                    hs_compromise_code = self.get_compromise_code(hs_circuit)

                    self.file.write('{0}\t{1}\t{2}\t\t\t{3}\n'.format(self.sample_id, stream['time'],
                        client_compromise_code, hs_compromise_code))
                elif (self.format == 'network-adv'):
                    self.file.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(self.sample_id, stream['time'],
                        guard_ip, exit_ip, dest_ip))
                else:
                    self.file.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n'.format(self.sample_id,
                        stream['time'], cl_guard_ip, cl_middle_ip, rp_ip, hs_exit_ip, hs_middle_ip, hs_guard_ip))
######

### Print relay compromised codes of stream assignments, compromise from input adv relays. ###
class PrintStreamAssignmentsAdvRelays(object):

    def __init__(self, adv_relays_filename, testing, file=sys.stdout):
        self.testing = testing
        self.file = file
        self.descriptors = None
        self.sample_id = None
        # store adversary relay fingerprints
        self.adv_relays = set()
        with open(adv_relays_filename, 'r') as f:
            for line in f:
                self.adv_relays.add(line.strip())
        if self.testing:
            print('Found {} adversary relays'.format(len(self.adv_relays)))

    def print_header(self):
        """Prints log header for stream lines."""

        if self.testing:
            return
        self.file.write('Sample\tTimestamp\tCompromise Code\n')

    def set_network_state(self, cons_valid_after, cons_fresh_until, cons_bw_weights,
        cons_bwweightscale, cons_rel_stats, descriptors):
        self.descriptors = descriptors

    def set_sample_id(self, id):
        self.sample_id = id

    def circuit_creation(self, circuit):
        pass

    def stream_assignment(self, stream, circuit):
        """Writes log line to file showing client, time and compromise codes:
        0 if guard & exit good, 1 if guard bad only, 2 if exit bad only, 3 if guard and exit bad."""


        if (circuit is None):
            return

        if self.testing:
            return

        guard_bad = False
        exit_bad = False
        if (circuit['path'][0] in self.adv_relays):
            guard_bad = True
        if (circuit['path'][2] in self.adv_relays):
            exit_bad = True
        compromise_code = 0
        if (guard_bad and exit_bad):
            compromise_code = 3
        elif guard_bad:
            compromise_code = 1
        elif exit_bad:
            compromise_code = 2
        self.file.write('{0}\t{1}\t{2}\n'.format(self.sample_id , stream['time'], compromise_code))
