#!/usr/bin/python
"""
Licensed to the Apache Software Foundation (ASF) under one or more
contributor license agreements.  See the NOTICE file distributed with
this work for additional information regarding copyright ownership.
The ASF licenses this file to You under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with
the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

    
    Copyright: 2012 Anton Zering <synth@lostprofile.de>

"""

import sys

try:
    import yapgvb
    import irclib
except:
    print "Some dependencies could not been fulfilled. Exiting."
    sys.exit(0)

SERVER = ("efnet.portlane.se", 6667)
NICK = "topologybot"
OUTPUT_FILE = "%s_topology.png" % SERVER[0]

def generate_links(links):
    """ create a clique of n nodes """

    # Create a new undirected graph
    graph = yapgvb.Graph('%s-clique' % 10)

    nodes = {}

    for link in links:
       nodes[link[0]] = graph.add_node(label= link[0])

    for link in links:
       if link[0] == link[1]:
          continue
       nodes[link[0]] >> nodes[link[1]]

    graph.layout(yapgvb.engines.dot)

    format = yapgvb.formats.png

    filename = OUTPUT_FILE
    graph.render(filename)


class IRCCat(irclib.SimpleIRCClient):
    def __init__(self):
        irclib.SimpleIRCClient.__init__(self)
        self.links = []
		
    def on_welcome(self, connection, event):
	print "connected, fetching links"
        connection.links()

    def on_links(self, connection, event):
        print event.arguments()
        self.links.append(event.arguments())

    def on_endoflinks(self, connection, event):
        print "rendering"
        generate_links(self.links)
        connection.disconnect()
		
    def on_disconnect(self, connection, event):
        sys.exit(0)

def main():
    c = IRCCat()

    try:
	print "connecting"
        c.connect(SERVER[0], SERVER[1], NICK)
    except irclib.ServerConnectionError, x:
        print x
        sys.exit(1)
    c.start()

if __name__ == "__main__":
    main()

