
class Cost_ratios:

    def print_out(self, result, context):

        print(f'{context}={result:.2f}\n')

    def CIM(self, european_manufact_cost, overseas_manufact_cost):
        # CIM Cost Index Manufacturing
        # EU Manufacturing cost / overseas Manufacturing cost

        cim = european_manufact_cost/overseas_manufact_cost

        self.print_out(cim, 'CIM')

        return cim

    def CIL(self, european_manufact_cost, overseas_manufact_cost, overseas_logistic_cost, european_logistic_cost):
        # CIM Cost Index Landing =
        # EU Manufacturing cost / (overseas manufacturing cost + overseas Logistics cost)

        cil = (european_manufact_cost + european_logistic_cost)/(overseas_manufact_cost + overseas_logistic_cost)

        self.print_out(cil, 'CIL')

        return cil


def main():

    costs = Cost_ratios()
    costs.CIM(7.186, 7.451)

if __name__ == "__main__":
    main()
