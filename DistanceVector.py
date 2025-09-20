# Distance Vector project for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related 
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This 
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, Jeffrey Randow, new VM fixes by Jared Scott and James Lohse.

from Node import *
from helpers import *


class DistanceVector(Node):
    
    def __init__(self, name, topolink, outgoing_links, incoming_links):
        """ Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here."""

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)

        # TODO: Create any necessary data structure(s) to contain the Node's internal state / distance vector data
        self.dv = {name: 0}
        for neighbor in outgoing_links:
            self.dv[neighbor.name] = int(neighbor.weight)

    def send_initial_messages(self):
        """ This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here. 

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight """

        # TODO - Each node needs to build a message and send it to each of its neighbors
        # HINT: Take a look at the skeleton methods provided for you in Node.py
        msg = (self.name, self.dv)
        for up in self.neighbor_names:
            self.send_msg(msg, up)

    def process_BF(self):
        """ This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. """

        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:
        # TODO 1. Process queued messages
        updated = False
        for msg in self.messages:
            src = msg[0]
            dv = msg[1]
            weight_to_src = self.get_outgoing_neighbor_weight(src)[1]
            # print(f'Message from {src} to {self.name} with dv {dv}')
            for dst in dv:
                if dst == self.name:
                    continue
                if dv[dst] == -99:
                    new = -99
                else:
                    new = max(weight_to_src + dv[dst], -99)
                if dst not in self.dv or new < self.dv[dst]:
                    updated = True
                    self.dv[dst] = new

        # Empty queue
        self.messages = []

        # TODO 2. Send neighbors updated distances
        if updated:
            msg = (self.name, self.dv)
            for up in self.neighbor_names:
                self.send_msg(msg, up)

    def log_distances(self):
        """ This function is called immedately after process_BF each round.  It 
        prints distances to the console and the log file in the following format (no whitespace either end):
        
        A:(A,0) (B,1) (C,-2)
        
        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 """
        
        # TODO: Use the provided helper function add_entry() to accomplish this task (see helpers.py).
        # An example call that which prints the format example text above (hardcoded) is provided.
        pairs = [f"({key},{value})" for key, value in self.dv.items()]
        logstring = ' '.join(pairs)
        add_entry(str(self.name), logstring)
