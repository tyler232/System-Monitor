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
        self.root.geometry("1000x800")

        self.figure = Figure(figsize=(10, 3), dpi=100)
        self.figure.subplots_adjust(wspace=0.5)

        # CPU Usage subplot
        self.cpu_subplot = self.figure.add_subplot(131)
        self.cpu_subplot.set_xlim(0, 60)
        self.cpu_subplot.set_ylim(0, 100)
        self.cpu_line, = self.cpu_subplot.plot([], [])
        self.cpu_subplot.set_title('CPU Usage')

        # Memory Usage subplot
        self.mem_subplot = self.figure.add_subplot(132)
        self.mem_subplot.set_xlim(0, 60)
        self.mem_subplot.set_ylim(0, 100)
        self.mem_line, = self.mem_subplot.plot([], [])
        self.mem_subplot.set_title('Memory Usage')

        # Disk Usage subplot
        self.disk_subplot = self.figure.add_subplot(133)
        self.disk_subplot.set_title('Disk Usage')
        self.disk_usage = psutil.disk_usage('/')
        labels = ['Used', 'Free']
        sizes = [self.disk_usage.used, self.disk_usage.free]
        self.disk_subplot.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        self.disk_subplot.axis('equal')

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().place(x=0, y=500, width=1000, height=300)

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

        # update Disk usage
        disk_usage = psutil.disk_usage('/')
        labels = ['Used', 'Free']
        sizes = [disk_usage.used, disk_usage.free]
        self.disk_subplot.clear()
        self.disk_subplot.set_title('Disk Usage')
        self.disk_subplot.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        self.disk_subplot.axis('equal')

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SystemMonitorApp()
    app.run()

