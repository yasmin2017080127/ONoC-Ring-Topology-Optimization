import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.main import main

def validate_inputs(values):
    """Validates user inputs and returns processed values."""
    try:
        num_nodes = int(values['nodes'])
        partition_size = int(values['partition'])
        wc = float(values['wc'])
        wt = float(values['wt'])
        sources = [int(x.strip()) for x in values['sources'].split(',')]
        targets = [int(x.strip()) for x in values['targets'].split(',')]
        
        # Additional validation
        if num_nodes < max(sources + targets + [1]):
            raise ValueError("Node indices must be less than total number of nodes")
        if partition_size >= num_nodes:
            raise ValueError("Partition size must be less than number of nodes")
        if not (0 <= wc <= 1 and 0 <= wt <= 1 and abs(wc + wt - 1) < 1e-6):
            raise ValueError("Weights must be between 0 and 1 and sum to 1")
            
        return num_nodes, partition_size, wc, wt, sources, targets
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
        return None

def run_simulation():
    """Runs the simulation with user-specified parameters."""
    try:
        num_nodes = int(entry_nodes.get())
        partition_size = int(entry_partition.get())
        wc = float(entry_wc.get())
        wt = float(entry_wt.get())
        sources = [int(x.strip()) for x in entry_sources.get().split(',')]
        targets = [int(x.strip()) for x in entry_targets.get().split(',')]
        
        main(num_nodes, partition_size, wc, wt, sources, targets)
        messagebox.showinfo("Success", "Simulation completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Simulation failed: {str(e)}")

# Create main window
root = tk.Tk()
root.title("ONoC Ring Topology Simulator")

# Create and pack the main frame
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create input fields with better default values
ttk.Label(frame, text="Number of Nodes:").grid(column=0, row=0, sticky=tk.W)
entry_nodes = ttk.Entry(frame, width=20)
entry_nodes.grid(column=1, row=0)
entry_nodes.insert(0, "20")

ttk.Label(frame, text="Source Nodes (comma-separated):").grid(column=0, row=1, sticky=tk.W)
entry_sources = ttk.Entry(frame, width=20)
entry_sources.grid(column=1, row=1)
entry_sources.insert(0, "0,10")

ttk.Label(frame, text="Target Nodes (comma-separated):").grid(column=0, row=2, sticky=tk.W)
entry_targets = ttk.Entry(frame, width=20)
entry_targets.grid(column=1, row=2)
entry_targets.insert(0, "5,15")

ttk.Label(frame, text="Partition Size:").grid(column=0, row=3, sticky=tk.W)
entry_partition = ttk.Entry(frame, width=20)
entry_partition.grid(column=1, row=3)
entry_partition.insert(0, "5")

ttk.Label(frame, text="Weight for Congestion (wc):").grid(column=0, row=4, sticky=tk.W)
entry_wc = ttk.Entry(frame, width=20)
entry_wc.grid(column=1, row=4)
entry_wc.insert(0, "0.7")

ttk.Label(frame, text="Weight for Temperature (wt):").grid(column=0, row=5, sticky=tk.W)
entry_wt = ttk.Entry(frame, width=20)
entry_wt.grid(column=1, row=5)
entry_wt.insert(0, "0.3")

# Create the Run button
run_button = ttk.Button(frame, text="Run Simulation", command=run_simulation)
run_button.grid(column=0, row=6, columnspan=2, pady=10)

if __name__ == "__main__":
    root.mainloop()
