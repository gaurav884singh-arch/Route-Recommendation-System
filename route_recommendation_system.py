import heapq
import tkinter as tk
from tkinter import ttk, messagebox
import math
import time
from typing import Dict, List, Tuple, Optional
import threading

class CityGraph:
    def __init__(self):
        self.positions = {}  # City positions for visualization
        self.graph = {}      # Adjacency list
        self.heuristics = {} # Heuristic values
        
    def add_city(self, city: str, x: int, y: int, heuristic: int):
        self.positions[city] = (x, y)
        self.graph[city] = {}
        self.heuristics[city] = heuristic
        
    def add_connection(self, city1: str, city2: str, distance: int):
        if city1 in self.graph and city2 in self.graph:
            self.graph[city1][city2] = distance
            self.graph[city2][city1] = distance

class RouteRecommendationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Route Recommendation System - Best First Search")
        self.root.geometry("1600x950")
        # Modern gradient-like background using dark blue
        self.root.configure(bg='#0f172a')
        
        self.graph = CityGraph()
        self.setup_graph()
        self.setup_gui()
        self.current_animation = None
        self.animation_step = 0
        
    def setup_graph(self):
        # Add Indian cities with positions (x, y) and heuristic values
        cities_data = [
            ("Delhi", 100, 300, 366), ("Jaipur", 50, 200, 374), ("Chandigarh", 50, 100, 380),
            ("Agra", 250, 250, 253), ("Lucknow", 50, 400, 329), ("Kanpur", 150, 450, 244),
            ("Varanasi", 250, 500, 241), ("Patna", 350, 550, 242), ("Kolkata", 450, 500, 160),
            ("Bhopal", 350, 350, 193), ("Indore", 400, 200, 176), ("Nagpur", 500, 400, 100),
            ("Mumbai", 600, 350, 0), ("Pune", 600, 450, 77), ("Hyderabad", 700, 300, 80),
            ("Bangalore", 800, 250, 151), ("Chennai", 900, 300, 161), ("Coimbatore", 750, 150, 199),
            ("Kochi", 650, 100, 226), ("Trivandrum", 550, 50, 234)
        ]
        
        for city, x, y, heuristic in cities_data:
            self.graph.add_city(city, x, y, heuristic)
            
        # Add connections between Indian cities
        connections = [
            ("Delhi", "Jaipur", 280), ("Delhi", "Agra", 240), ("Delhi", "Lucknow", 550),
            ("Jaipur", "Chandigarh", 500), ("Chandigarh", "Agra", 380),
            ("Lucknow", "Kanpur", 90), ("Kanpur", "Varanasi", 330),
            ("Varanasi", "Patna", 250), ("Patna", "Kolkata", 560),
            ("Kolkata", "Nagpur", 1100), ("Kolkata", "Bhopal", 1500),
            ("Bhopal", "Agra", 600), ("Bhopal", "Nagpur", 480),
            ("Agra", "Indore", 760), ("Indore", "Mumbai", 590),
            ("Nagpur", "Mumbai", 850), ("Mumbai", "Pune", 150),
            ("Mumbai", "Hyderabad", 710), ("Hyderabad", "Bangalore", 570),
            ("Bangalore", "Chennai", 350), ("Chennai", "Coimbatore", 500),
            ("Coimbatore", "Kochi", 190), ("Kochi", "Trivandrum", 220)
        ]
        
        for city1, city2, distance in connections:
            self.graph.add_connection(city1, city2, distance)
    
    def setup_gui(self):
        # Modern dark theme with better styling
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for dark theme
        bg_color = '#0f172a'
        fg_color = '#e2e8f0'
        accent_color = '#3b82f6'
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TLabelframe', background=bg_color, foreground=fg_color)
        style.configure('TLabelframe.Label', background=bg_color, foreground=accent_color)
        style.configure('TButton', background=accent_color, foreground='white')
        style.map('TButton', background=[('active', '#2563eb')])
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left panel - Controls
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        # Title
        title_label = ttk.Label(left_frame, text="🚀 Indian Route Finder", 
                               font=('Segoe UI', 18, 'bold'), foreground='#60a5fa')
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(left_frame, text="Best-First Search Algorithm", 
                                  font=('Segoe UI', 10), foreground='#94a3b8')
        subtitle_label.pack(pady=(0, 20))
        
        # City selection
        selection_frame = ttk.LabelFrame(left_frame, text="📍 City Selection", padding=12)
        selection_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(selection_frame, text="Start City:", font=('Segoe UI', 10)).pack(anchor=tk.W, pady=(0, 5))
        self.start_var = tk.StringVar()
        self.start_combo = ttk.Combobox(selection_frame, textvariable=self.start_var, 
                                       values=list(self.graph.positions.keys()), state='readonly')
        self.start_combo.pack(fill=tk.X, pady=(0, 12))
        self.start_combo.set("Delhi")
        
        ttk.Label(selection_frame, text="Destination City:", font=('Segoe UI', 10)).pack(anchor=tk.W, pady=(0, 5))
        self.goal_var = tk.StringVar()
        self.goal_combo = ttk.Combobox(selection_frame, textvariable=self.goal_var,
                                      values=list(self.graph.positions.keys()), state='readonly')
        self.goal_combo.pack(fill=tk.X, pady=(0, 12))
        self.goal_combo.set("Mumbai")
        
        # Control buttons
        button_frame = ttk.Frame(selection_frame)
        button_frame.pack(fill=tk.X)
        
        self.search_btn = ttk.Button(button_frame, text="🔍 Find Route", 
                                   command=self.start_search)
        self.search_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        
        self.reset_btn = ttk.Button(button_frame, text="🔄 Reset", 
                                  command=self.reset_search)
        self.reset_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Animation controls
        anim_frame = ttk.LabelFrame(left_frame, text="⚡ Animation Speed", padding=12)
        anim_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(anim_frame, text="Slow ← → Fast", font=('Segoe UI', 9)).pack(anchor=tk.W, pady=(0, 8))
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(anim_frame, from_=0.1, to=3.0, variable=self.speed_var,
                               orient=tk.HORIZONTAL)
        speed_scale.pack(fill=tk.X)
        
        # Results display
        results_frame = ttk.LabelFrame(left_frame, text="📊 Search Results", padding=12)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 0))
        
        # Text widget for results
        self.results_text = tk.Text(results_frame, height=20, width=35, wrap=tk.WORD,
                                   bg='#1e293b', fg='#e2e8f0', font=('Consolas', 9),
                                   insertbackground='#60a5fa', relief=tk.FLAT, bd=0)
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right panel - Visualization
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas for graph visualization
        self.canvas = tk.Canvas(right_frame, bg='#1e293b', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to search...")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.FLAT,
                              font=('Segoe UI', 9), foreground='#94a3b8')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=10)
        
        # Draw initial graph
        self.draw_graph()
    
    def draw_graph(self):
        self.canvas.delete("all")
        
        # Draw connections with gradient-like effect
        for city1 in self.graph.graph:
            for city2, distance in self.graph.graph[city1].items():
                x1, y1 = self.graph.positions[city1]
                x2, y2 = self.graph.positions[city2]
                # Modern line styling
                self.canvas.create_line(x1, y1, x2, y2, fill='#475569', width=2.5, tags="connection")
                
                # Draw distance label with better styling
                mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
                self.canvas.create_text(mid_x, mid_y, text=str(distance), 
                                       fill='#cbd5e1', font=('Segoe UI', 8, 'bold'), tags="distance")
        
        # Draw cities with modern node design
        for city, (x, y) in self.graph.positions.items():
            # Outer glow effect
            self.canvas.create_oval(x-28, y-28, x+28, y+28, fill='#334155', 
                                  outline='#334155', width=0, tags=("glow", city))
            
            # Main city circle with gradient-like appearance
            self.canvas.create_oval(x-22, y-22, x+22, y+22, fill='#3b82f6', 
                                  outline='#60a5fa', width=2, tags=("city", city))
            
            # Inner highlight for 3D effect
            self.canvas.create_oval(x-18, y-22, x+18, y-10, fill='#60a5fa', 
                                  outline='', tags=("highlight", city))
            
            # City name
            self.canvas.create_text(x, y-32, text=city, fill='#e2e8f0', 
                                  font=('Segoe UI', 10, 'bold'), tags=("label", city))
            
            # Heuristic value
            self.canvas.create_text(x, y+28, text=f"h={self.graph.heuristics[city]}", 
                                  fill='#fbbf24', font=('Segoe UI', 8, 'bold'), tags=("heuristic", city))
    
    def highlight_city(self, city, color='#ef4444'):
        """Highlight a city with specified color"""
        self.canvas.itemconfig(city, fill=color, outline='#fca5a5')
        
    def draw_path(self, path, color='#10b981', width=5):
        """Draw the final path with smooth animation"""
        for i in range(len(path) - 1):
            city1, city2 = path[i], path[i+1]
            x1, y1 = self.graph.positions[city1]
            x2, y2 = self.graph.positions[city2]
            
            # Draw path line with arrow
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width, 
                                  arrow=tk.LAST, arrowshape=(18, 22, 8), tags="final_path")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
        self.root.update()
    
    def log_result(self, message):
        """Add message to results text"""
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END)
        self.root.update()
    
    def animate_exploration(self, current_city, path, distance, heuristic, step):
        """Animate the current exploration step with smooth transitions"""
        # Improved animation with multiple frames for smooth movement
        self.canvas.delete("current_highlight")
        self.canvas.delete("path_highlight")
        
        # Highlight current city with pulsing effect
        x, y = self.graph.positions[current_city]
        pulse_size = 28 + (5 * math.sin(time.time() * 4))
        self.canvas.create_oval(x-pulse_size, y-pulse_size, x+pulse_size, y+pulse_size, 
                              outline='#ef4444', width=3, tags="current_highlight")
        
        # Highlight path taken so far with gradient effect
        for i in range(len(path) - 1):
            city1, city2 = path[i], path[i+1]
            x1, y1 = self.graph.positions[city1]
            x2, y2 = self.graph.positions[city2]
            # Animated path with varying opacity effect
            self.canvas.create_line(x1, y1, x2, y2, fill='#f59e0b', width=4, 
                                  tags="path_highlight")
        
        # Update results log with better formatting
        self.log_result(f"Step {step}: Exploring {current_city}")
        self.log_result(f"  Path: {' → '.join(path)}")
        self.log_result(f"  Distance: {distance}km | Heuristic: {heuristic}")
        self.log_result("")
        
        # Smoother animation timing based on speed
        animation_delay = 0.5 / self.speed_var.get()
        time.sleep(animation_delay)
    
    def best_first_search(self, start, goal):
        """Perform Best-First Search with animation"""
        if start not in self.graph.graph or goal not in self.graph.graph:
            return None, 0
        
        priority_queue = []
        heapq.heappush(priority_queue, (self.graph.heuristics[start], start, [start], 0))
        visited = set()
        step = 0
        
        self.log_result("🚀 Starting Best-First Search...")
        self.log_result(f"📍 Start: {start}")
        self.log_result(f"🎯 Goal: {goal}")
        self.log_result("=" * 40)
        self.log_result("")
        
        while priority_queue:
            if self.current_animation == "stop":
                break
                
            current_heuristic, current_city, path, distance_so_far = heapq.heappop(priority_queue)
            
            if current_city in visited:
                continue
                
            visited.add(current_city)
            step += 1
            
            # Animate current step
            self.animate_exploration(current_city, path, distance_so_far, current_heuristic, step)
            
            if current_city == goal:
                self.log_result("=" * 40)
                self.log_result("🎉 Destination reached!")
                self.log_result(f"✅ Final path: {' → '.join(path)}")
                self.log_result(f"📏 Total distance: {distance_so_far}km")
                self.log_result(f"📊 Steps explored: {step}")
                return path, distance_so_far
            
            # Explore neighbors
            for neighbor, dist in self.graph.graph[current_city].items():
                if neighbor not in visited:
                    new_distance = distance_so_far + dist
                    new_path = path + [neighbor]
                    heapq.heappush(priority_queue, 
                                 (self.graph.heuristics[neighbor], neighbor, new_path, new_distance))
        
        return None, 0
    
    def start_search(self):
        """Start the search in a separate thread"""
        start_city = self.start_var.get()
        goal_city = self.goal_var.get()
        
        if not start_city or not goal_city:
            messagebox.showerror("Error", "Please select both start and destination cities")
            return
        
        if start_city == goal_city:
            messagebox.showinfo("Info", "Start and destination cities are the same!")
            return
        
        # Reset UI
        self.results_text.delete(1.0, tk.END)
        self.draw_graph()
        self.search_btn.config(state='disabled')
        self.current_animation = "running"
        self.update_status("🔍 Searching for optimal route...")
        
        # Run search in separate thread
        def run_search():
            try:
                path, total_distance = self.best_first_search(start_city, goal_city)
                
                # Draw final path
                if path:
                    self.draw_path(path)
                    self.log_result("\n⭐ SEARCH COMPLETED SUCCESSFULLY!")
                    self.update_status(f"✅ Route found: {' → '.join(path)}")
                else:
                    self.log_result("\n❌ NO PATH FOUND!")
                    self.update_status("❌ No path available")
                    
            except Exception as e:
                self.log_result(f"\n💥 Error: {str(e)}")
                self.update_status(f"❌ Error: {str(e)}")
            finally:
                self.search_btn.config(state='normal')
                self.current_animation = None
        
        threading.Thread(target=run_search, daemon=True).start()
    
    def reset_search(self):
        """Reset the search and visualization"""
        self.current_animation = "stop"
        self.results_text.delete(1.0, tk.END)
        self.draw_graph()
        self.update_status("Ready to search...")
        self.search_btn.config(state='normal')

def main():
    root = tk.Tk()
    app = RouteRecommendationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()