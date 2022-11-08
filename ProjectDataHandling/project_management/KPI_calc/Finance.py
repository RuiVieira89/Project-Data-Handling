
class Cost_ratios:

    def print_out(self, result, context):

        print(f'{context}={result:.2f}\n')
        
        return f'{context}={result:.2f}\n'

    def CIM(self, local_manufact_cost, overseas_manufact_cost):
        # CIM Cost Index Manufacturing
        # EU Manufacturing cost / overseas Manufacturing cost

        cim = local_manufact_cost/overseas_manufact_cost

        self.print_out(cim, 'CIM')

        return cim

    def CIL(self, local_manufact_cost, overseas_manufact_cost, overseas_logistic_cost, local_logistic_cost):
        # CIM Cost Index Landing =
        # EU Manufacturing cost / (overseas manufacturing cost + overseas Logistics cost)

        cil = (local_manufact_cost + local_logistic_cost)/(overseas_manufact_cost + overseas_logistic_cost)

        self.print_out(cil, 'CIL')

        return cil
