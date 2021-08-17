
try:
    import Tkinter as Tk # python 2
except ModuleNotFoundError:
    import tkinter as Tk # python 3

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from side_panel import SidePanel

class View:
    def __init__(self, root, model):
        self.frame = Tk.Frame(root)
        self.model = model
        self.fig = Figure(figsize=(7.5, 4), dpi=80)
        self.ax0 = self.fig.add_axes((0.05, .05, .90, .90), facecolor=(.75, .75, .75), frameon=False)
        self.frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.sidepanel = SidePanel(root)

        self.sidepanel.plotBut.bind("<Button>", self.plot)
        self.sidepanel.clearButton.bind("<Button>", self.clear)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        # self.canvas.show()
        self.canvas.draw()

    def clear(self, event):
        self.ax0.clear()
        self.fig.canvas.draw()

    def plot(self, event):
        self.model.calculate()
        self.ax0.clear()
        self.ax0.contourf(self.model.res["x"], self.model.res["y"], self.model.res["z"])
        self.fig.canvas.draw()