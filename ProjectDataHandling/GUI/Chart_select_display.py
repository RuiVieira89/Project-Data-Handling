
import PySimpleGUI as sg
import inspect
import matplotlib

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')

def select_display(option_funcs_dict, data):
    
    #  The magic function that makes it possible.... glues together tkinter and pyplot using Canvas Widget
    def draw_figure(canvas, figure):
        if not hasattr(draw_figure, 'canvas_packed'):
            draw_figure.canvas_packed = {}
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        widget = figure_canvas_agg.get_tk_widget()
        if widget not in draw_figure.canvas_packed:
            draw_figure.canvas_packed[widget] = figure
            widget.pack(side='top', fill='both', expand=1)
        return figure_canvas_agg
    
    def delete_figure_agg(figure_agg):
        
        figure_agg.get_tk_widget().forget()
        try:
            draw_figure.canvas_packed.pop(figure_agg.get_tk_widget())
        except Exception as e:
            print(f'Error removing {figure_agg} from list', e)
        plt.close('all')

    
    figure_w, figure_h = 650, 650
    # define the form layout
    listbox_values = list(option_funcs_dict)
    col_listbox = [[sg.Listbox(values=listbox_values, enable_events=True, 
                            size=(28, len(listbox_values)), key='-LISTBOX-')],
                [sg.Text(' ' * 12), sg.Exit(size=(5, 2))]]

    layout = [[sg.Text('Matplotlib Plot Test', font=('current 18'))],
            [sg.Col(col_listbox, pad=(5, (3, 330))), 
            sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-') ,
            sg.MLine(size=(70, 35), pad=(5, (3, 90)), key='-MULTILINE-')],]

    # create the form and show it without the plot
    window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', 
                    layout, grab_anywhere=False, finalize=True)

    figure_agg = None
    # The GUI Event Loop
    while True:
        event, values = window.read()
        # print(event, values)                  # helps greatly when debugging
        if event in (sg.WIN_CLOSED, 'Exit'):             # if user closed window or clicked Exit button
            break
        if figure_agg:
            # ** IMPORTANT ** Clean up previous drawing before drawing again
            delete_figure_agg(figure_agg)
        choice = values['-LISTBOX-'][0]                 # get first listbox item chosen (returned as a list)
        func = option_funcs_dict[choice]                         # get function to call from the dictionary
        window['-MULTILINE-'].update(inspect.getsource(func))  # show source code to function in multiline
        try:
            fig = func(data)                                    # call function to get the figure
            figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)  # draw the figure
        except Exception as e:
            print('Exception in fucntion', e)
    window.close()
