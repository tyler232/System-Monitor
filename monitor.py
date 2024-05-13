import psutil
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import numpy as np

class SystemMonitorApp:
    def __init__(self, interval=1000):
        self.interval = interval
        self.root = ctk.CTk()
        self.root.title("System Monitor")

        self.figure = Figure(figsize=(5, 8), dpi=100)

        # CPU subplot
        self.cpu_subplot = self.figure.add_subplot(211)
        self.cpu_subplot.set_xlim(0, 60)
        self.cpu_subplot.set_ylim(0, 100)
        self.cpu_line, = self.cpu_subplot.plot([], [])
        self.cpu_subplot.set_title('CPU Usage')

        # Memory subplot
        self.mem_subplot = self.figure.add_subplot(212)
        self.mem_subplot.set_xlim(0, 60)
        self.mem_subplot.set_ylim(0, 100)
        self.mem_line, = self.mem_subplot.plot([], [])
        self.mem_subplot.set_title('Memory Usage')

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

        self.anim = animation.FuncAnimation(self.figure, self.update_plot, interval=self.interval, save_count=1000)

        self.cpu_usage = []
        self.mem_usage = []
        self.x_values = np.arange(0, 61)

    def update_plot(self, frame):
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory().percent

        self.cpu_usage.append(cpu_percent)
        self.mem_usage.append(mem_percent)
        self.cpu_usage = self.cpu_usage[-61:]
        self.mem_usage = self.mem_usage[-61:]

        self.cpu_line.set_ydata(self.cpu_usage)
        self.mem_line.set_ydata(self.mem_usage)

        self.x_values = np.arange(len(self.cpu_usage))
        self.cpu_line.set_xdata(self.x_values)
        self.mem_line.set_xdata(self.x_values)

        self.cpu_subplot.relim()
        self.cpu_subplot.autoscale_view()
        self.mem_subplot.relim()
        self.mem_subplot.autoscale_view()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SystemMonitorApp()
    app.run()
