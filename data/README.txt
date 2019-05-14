This directory contains the inferred geographic relationships using the method 
described at http://wwww.caida.org/data/as-relationships-geo.

There are two files: 201603.as-rel-geo.txt and 201603.locations.txt.
The as-rel-geo file contains the geographic inferrences.
Each line contains a single AS relationship, it's inferred geographic
locations, and the method used to infer them.

    format: AS0|AS1|loc0,source0.0,source0.1,loc1|loc1,source1.0...
	sources:
	    bc : BGP communities
            itdk : Internet Topology Data Kit
            mlp : Multilateral Peering
            lg : Looking Glass
	    edge: Edge AS link
	3|3356|Boston-MA-USA,bc|San Jose-CA-USA,itdk
	    BGP communites where used to infer a link between
            AS3 and AS3356 in Boston, MA and the ITDK was used
            to infer the same link in Jose, CA, USA.

The locations file provides more information about individual locations. 

    # format: lid|continent|country|region|city|latitude|longitude|population
    Aabenraa-83-DNK|Europe|DNK|83|Aabenraa|55.0324|9.4417|10
	Population is left 0 if the population was not known.

NOTE: the two files 201603.as-rel-geo.txt and 201603.locations.txt were
replaced on 25-Apr-2017, correcting an error in the earlier versions.
