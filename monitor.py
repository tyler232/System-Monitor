import os
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

        self.init_info()

        self.figure = Figure(figsize=(10, 3), dpi=100)
        self.figure.subplots_adjust(wspace=0.5)
        self.init_subplot()

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        self.anim = animation.FuncAnimation(self.figure, self.update, interval=self.interval, save_count=1000)

        self.cpu_usage = []
        self.mem_usage = []
        self.x_values = np.arange(0, 61)

        self.root.bind("<Configure>", self.on_window_resize)

    def on_window_resize(self, event):
        self.canvas.get_tk_widget().config(width=event.width, height=event.height)


    def init_info(self):
        self.process_info_label = ctk.CTkLabel(self.root, text="Processes: ")
        self.load_info_label = ctk.CTkLabel(self.root, text="Load Average: ")
        self.cpu_label = ctk.CTkLabel(self.root, text="CPU: ")
        self.memory_label = ctk.CTkLabel(self.root, text="Memory: ")
        self.swap_label = ctk.CTkLabel(self.root, text="Swap: ")
        self.network_label = ctk.CTkLabel(self.root, text="Network I/O: ")
        self.diskio_label = ctk.CTkLabel(self.root, text="Disk I/O: ")
        self.battery_label = ctk.CTkLabel(self.root, text="Battery: ")

        self.process_info_label.pack(side='top', padx=10, pady=10)
        self.load_info_label.pack(side='top', padx=10, pady=10)
        self.cpu_label.pack(side='top', padx=10, pady=10)
        self.memory_label.pack(side='top', padx=10, pady=10)
        self.swap_label.pack(side='top', padx=10, pady=10)
        self.network_label.pack(side='top', padx=10, pady=10)
        self.diskio_label.pack(side='top', padx=10, pady=10)
        self.battery_label.pack(side='top', padx=10, pady=10)

    def init_subplot(self):
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

    def update(self, frame):
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

        # update info
        self.update_info()
        
        

    def update_info(self):
        self.update_process_info()
        self.update_load_info()
        self.update_cpu_info()
        self.update_memory_info()
        self.update_networkio_info()
        self.update_diskio_info()
        self.update_battery_info()

    def update_process_info(self):
        processes = psutil.pids()
        self.process_info_label.configure(text=f"Processes: {len(processes)} total")
    
    def update_load_info(self):
        load_avg = os.getloadavg()
        self.load_info_label.configure(text=f"Load Average: {load_avg[0]:.2f} (1 min), {load_avg[1]:.2f} (5 min), {load_avg[2]:.2f} (15 min)")
    
    def update_cpu_info(self):
        logical_cpus = psutil.cpu_count()
        physical_cpus = psutil.cpu_count(logical=False)
        cpu_freq = psutil.cpu_freq()

        self.cpu_label.configure(text=f"CPU: {logical_cpus} logical, {physical_cpus} physical, {cpu_freq.current:.2f} MHz")

    def update_memory_info(self):
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        total_memory = memory.total
        used_memory = memory.used
        available_memory = memory.available
        
        total_swap = swap.total
        used_swap = swap.used
        free_swap = swap.free

        self.memory_label.configure(text=f"Memory: {used_memory/1024/1024:.2f} MB used, {available_memory/1024/1024:.2f} MB available, {total_memory/1024/1024:.2f} MB total")
        self.swap_label.configure(text=f"Swap: {used_swap/1024/1024:.2f} MB used, {free_swap/1024/1024:.2f} MB free, {total_swap/1024/1024:.2f} MB total")
        
    def update_networkio_info(self):
        net_counters = psutil.net_io_counters()
        bytes_in = net_counters.bytes_recv
        bytes_out = net_counters.bytes_sent

        self.network_label.configure(text=f"Network I/O: {bytes_out/1024/1024:.2f} MB sent, {bytes_in/1024/1024:.2f} MB received")

    def update_diskio_info(self):
        disk_counters = psutil.disk_io_counters()
        bytes_read = disk_counters.read_bytes
        bytes_written = disk_counters.write_bytes

        self.diskio_label.configure(text=f"Disk I/O: {bytes_read/1024/1024:.2f} MB read, {bytes_written/1024/1024:.2f} MB written")

    def update_battery_info(self):
        battery = psutil.sensors_battery()
        if battery is None:
            self.battery_label.configure(text=f"Battery Not Detected")
            return
        battery_percent = battery.percent
        power_plugged = battery.power_plugged
        power_plugged_status = "Plugged In" if power_plugged else "Not Plugged In"
        self.battery_label.configure(text=f"Battery: {battery_percent}% {power_plugged_status}")
        

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SystemMonitorApp()
    app.run()
