import pandas as pd

import ProjectDataHandling.utils.String_manipulation as util

import ProjectDataHandling.project_management.timelines.make_schedule_from_excel as Gantt
import ProjectDataHandling.project_management.KPI_calc.Finance as Fin
import ProjectDataHandling.data_analysis.charts as Chart

def main():

    names = []
    tabs = []
    comments = []

    objs = []
    obj_list = []

    objs.append(util.get_functions(Gantt))
    objs.append(util.get_functions(Fin))
    objs.append(util.get_functions(Chart))

    for import_ in objs:
        for obj in import_:
            names.append(obj[1]().name)
            tabs.append(obj[1]().tab)
            comments.append(obj[1]().comment)
            obj_list.append([obj[1]().name, obj[1]])

    d = {'Names': names, 'Tabs': tabs, 'Commments': comments}
    GUIfunctionality = pd.DataFrame(data=d)

    # obj_list[0][1](run=True)

    print(GUIfunctionality)
    


if __name__ == '__main__':

    main()
