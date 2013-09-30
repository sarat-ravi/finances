import logging
from bank import Bank
from inflow import CashFlow

class Manager(object):

    args = {}

    @staticmethod
    def init(args):
        return Manager.deserialize(args)

    @staticmethod
    def deserialize(args):
        manager = Manager(args["name"])

        try:
            for bank_name, bank_args in args["banks"].items():
                bank = Bank.init(bank_args)
                manager.add_bank(bank)
        except Exception as e:
            raise Exception("Unable to set up banks")

        try:
            for bank_name, cashflows in args["cashflows"].items():
                for flow_name, cashflow_args in cashflows.items():
                    flow = CashFlow.init(cashflow_args)
                    manager.add_cashflow(bank_name, flow)
        except Exception as e:
            raise Exception("Unable to set up cash flows")

        Manager.args = args
        return manager 

    @staticmethod
    def serialize(manager):
        args = {}
        args["name"] = manager.name

        banks = {}
        for bank_name, bank_args in Manager.args["banks"].items():
            bank = manager.get_bank(bank_args["name"])
            banks[bank_name] = Bank.serialize(bank)
        args["banks"] = banks

        cshflows = {}
        for bank_name, cashflows in Manager.args["cashflows"].items():
            flows = {}  
            for flow_name, cashflow_args in cashflows.items():
                bank = manager.get_bank(bank_name)
                cashflow = bank.inflows[cashflow_args["name"]]
                flows[flow_name] = CashFlow.serialize(cashflow)
            cshflows[bank_name] = flows
        args["cashflows"] = cshflows
        return args


    def __init__(self, name="manager"):
        self.name = name
        self.banks = {}
        self.log = logging.getLogger(__name__ + "." + self.name)

    def add_bank(self, bank):
        self.banks[bank.name] = bank

    def get_bank(self, bank_name):
        if not bank_name in self.banks:
            raise Exception("Bank '%s' not found" %(bank_name))

        return self.banks[bank_name]

    def add_cashflow(self, bank_name, cashflow):
        bank = self.get_bank(bank_name)
        bank.add_inflow(cashflow)

    def balance(self):
        balance = 0.0

        for bank_name, bank in self.banks.items(): 
            bank_balance = bank.balance
            self.log.info("got %s from %s" %(str(bank_balance), str(bank_name)))
            balance += bank_balance

        return balance


