#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2008-2018 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    runner.py
# @author  Michael Behrisch
# @author  Daniel Krajzewicz
# @date    2011-03-04
# @version $Id$


from __future__ import print_function
from __future__ import absolute_import
import os
import sys
SUMO_HOME = os.environ.get('SUMO_HOME',
                           os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..'))
sys.path.append(os.path.join(SUMO_HOME, 'tools'))
import traci  # noqa
import sumolib  # noqa

sumoBinary = sumolib.checkBinary('sumo')
conns = []
sumoProcess = []
for i in range(2):
    traci.start([sumoBinary, "-c", "sumo.sumocfg"], label=str(i))
    conns.append(traci.getConnection(str(i)))
for c in conns:
    for step in range(3):
        print("step", step)
        c.simulationStep()
for c in conns:
    print("routes", c.route.getIDList())
    print("route count", c.route.getIDCount())
    routeID = "horizontal"
    print("examining", routeID)
    print("edges", c.route.getEdges(routeID))
    c.route.subscribe(routeID)
for c in conns:
    print(c.route.getSubscriptionResults(routeID))
    for step in range(3, 6):
        print("step", step)
        c.simulationStep(step)
        print(c.route.getSubscriptionResults(routeID))
    c.route.add("h2", ["1o"])
    print("routes", c.route.getIDList())
    print("edges", c.route.getEdges("h2"))
    c.close()
