#!/usr/bin/env python
import time
import yaml
from pprint import pprint

from cashmoney import Bank, CashFlow, Manager 

#DEFAULT_CONFIG = """---

#name: Sarat Tallamraju
#banks:
    #wells_fargo: 
        #name: wells_fargo_checking
        #min_balance: 100.0

    #chase:
        #name: chase_checking
        #min_balance: 100.0
        
#cashflows: 
    #wells_fargo_checking:
        #livemagic:
            #name: lm_paycheck
            #amount: 2500.00
            #stime: 1380504706.865231
            #period: 2

#..."""

DEFAULT_CONFIG = "default.yaml"
ACCOUNTS_DIR = "accounts/"

def getargs():

    with open(DEFAULT_CONFIG, "r") as config:
        args = yaml.load(config)
        return args

def main():
    args = getargs()
    pprint(args)

    manager = Manager.init(args)

    #while True:
    for i in range(4):
        # ------------------------------------------------------------------

        print "Balance: %s" %(str(manager.balance()))    

        # ------------------------------------------------------------------
        time.sleep(1)

    args = Manager.serialize(manager)
    fname = ACCOUNTS_DIR + args["name"].lower().replace(" ", "_") + ".yaml"
    with open(fname, "w") as f:
        yaml.dump(args, f, indent=4)

if __name__ == "__main__":
    main()
