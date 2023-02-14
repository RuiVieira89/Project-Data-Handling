
class Cost_ratios:

    def __init__(self):
        
        self.tab = "Project Management"
        self.name = "Cost ratio"
        self.comment = "Compares two suplliers and returns the cost ratio"

    def print_out(self, result, context):

        print(f'{context}={result:.2f}\n')
        
        return f'{context}={result:.2f}\n'

    def CIM(self, local_manufact_cost, overseas_manufact_cost):
        print("Running Cost_ratios.CIM")
        # CIM Cost Index Manufacturing
        # EU Manufacturing cost / overseas Manufacturing cost

        cim = local_manufact_cost/overseas_manufact_cost

        self.print_out(cim, 'CIM')

        return cim

    def CIL(self, local_manufact_cost, overseas_manufact_cost, overseas_logistic_cost, local_logistic_cost):
        print("Running Cost_ratios.CIL")
        # CIM Cost Index Landing =
        # EU Manufacturing cost / (overseas manufacturing cost + overseas Logistics cost)

        cil = (local_manufact_cost + local_logistic_cost)/(overseas_manufact_cost + overseas_logistic_cost)

        self.print_out(cil, 'CIL')

        return cil
