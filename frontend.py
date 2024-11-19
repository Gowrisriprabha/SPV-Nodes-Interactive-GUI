import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import pydot
import graphviz
from graphviz import Digraph
from graphviz import sources
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ADD_BLOCK_URL = "http://127.0.0.1:5000/create_block"
VERIFY_TRANSACTION_URL = "http://127.0.0.1:5000/verify_transaction"

#graphviz.backend.CALLBACKS['dot'] = r'C:\Users\Amodini\anaconda3\Lib\site-packages\dot'

class SPVGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SPV Verification Process")
        self.root.geometry("1200x850")
        self.root.configure(bg="#1e1e2e")
        self.set_background_image(r"D:\SPV-Nodes-Interactive-GUI\image.jpg")

        self.style_buttons()

        # Creating a Canvas for scrolling
        self.canvas = tk.Canvas(self.root, bg="#1e1e2e", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Adding a Scrollbar to the canvas
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Creating a Frame inside the Canvas for the scrollable content
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1e1e2e")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Bind the mouse scroll event (which will also capture touchpad scrolling)
        self.root.bind_all("<MouseWheel>", self.mouse_wheel_scroll)

        # Create the heading and other sections
        self.create_heading()
        self.create_spv_verification_section()
        self.create_network_communication_section()
        self.create_merkle_tree_section()

    def set_background_image(self, image_path):
        image = Image.open(image_path).filter(ImageFilter.GaussianBlur(15))
        self.background_label = tk.Label(self.root)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.update_background_image(image)
        self.root.bind('<Configure>', lambda event: self.update_background_image(image))

    def update_background_image(self, image):
        resized_image = image.resize((self.root.winfo_width(), self.root.winfo_height()))
        darkened_image = ImageEnhance.Brightness(resized_image).enhance(0.3)
        self.background_image = ImageTk.PhotoImage(darkened_image)
        self.background_label.config(image=self.background_image)

    def style_buttons(self):
        style = ttk.Style()
        style.configure(
            "TButton",
            font=("Arial", 12, "bold"),
            padding=10,
            background="#00008B",
            foreground="#00008B",
        )
        style.map(
            "TButton",
            background=[("active", "#00008B"), ("disabled", "#00008B")],
            foreground=[("active", "#00008B"), ("disabled", "#00008B")]
        )

    def create_heading(self):
        heading_label = tk.Label(
            self.scrollable_frame,
            text="SPV VERIFICATION",
            font=("Arial Black", 28, "bold"),
            fg="#ffffff",
            bg="#1e1e2e",
        )
        heading_label.pack(pady=(50, 50))  # Increased padding for centering

    def create_spv_verification_section(self):
        spv_frame = tk.LabelFrame(
            self.scrollable_frame,
            text="SPV Verification Process",
            padx=40,
            pady=40,
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#1e1e2e",
            bd=3,
            relief="solid"
        )
        spv_frame.pack(padx=500, pady=40, fill="x", anchor="center")

        ttk.Label(
            spv_frame, text="Enter Transaction ID:", background="#ffffff", font=("Arial", 12)
        ).grid(row=0, column=0, padx=20, pady=20, sticky="w")
        self.transaction_details = ttk.Entry(spv_frame, width=40, font=("Arial", 12))
        self.transaction_details.grid(row=0, column=1, padx=20, pady=20)

        ttk.Label(
            spv_frame, text="Select Block ID:", background="#ffffff", font=("Arial", 12)
        ).grid(row=1, column=0, padx=20, pady=20, sticky="w")
        self.block_id = ttk.Entry(spv_frame, width=40, font=("Arial", 12))
        self.block_id.grid(row=1, column=1, padx=20, pady=20)

        verify_button = ttk.Button(
            spv_frame, text="Verify Transaction", command=self.simulate_spv_verification
        )
        verify_button.grid(row=2, column=0, columnspan=2, pady=30)

    def create_network_communication_section(self):
        network_frame = tk.LabelFrame(
            self.scrollable_frame,
            text="Network Communication Overview",
            padx=40,
            pady=40,
            font=("Arial", 14, "bold"),
            bg="#FFFFFF",
            fg="#1e1e2e",
            bd=3,
            relief="solid"
        )
        network_frame.pack(padx=500, pady=40, fill="x", anchor="center")

        self.network_display = tk.Text(
            network_frame, height=8, wrap=tk.WORD, bg="#f5f5f5", font=("Arial", 12), width=80
        )
        self.network_display.grid(row=0, column=0, padx=20, pady=20)

        start_communication_button = ttk.Button(
            network_frame, text="Start Network Communication", command=self.simulate_network_communication
        )
        start_communication_button.grid(row=1, column=0, pady=20)

        clear_button = ttk.Button(
            network_frame,
            text="Clear Logs",
            command=lambda: self.network_display.delete(1.0, tk.END),
        )
        clear_button.grid(row=2, column=0, pady=20)

    def create_merkle_tree_section(self):
        merkle_frame = tk.LabelFrame(
            self.scrollable_frame,
            text="Merkle Tree Visualization",
            padx=40,
            pady=40,
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#1e1e2e",
            bd=3,
            relief="solid"
        )
        merkle_frame.pack(padx=500, pady=40, fill="x", anchor="center")

        # Generate Merkle Tree Button
        merkle_button = ttk.Button(
            merkle_frame, text="Generate and Visualize Merkle Tree", command=self.generate_merkle_tree
        )
        merkle_button.pack(pady=30)

        # Canvas to display the Merkle tree graph
        self.canvas_frame = tk.Frame(merkle_frame, bg="#00008B")
        self.canvas_frame.pack(fill="both", expand=True)

    def generate_merkle_tree(self):
        try:
            transactions = ["tx1", "tx2", "tx3", "tx4"]
            G = nx.DiGraph()

            # Build the Merkle tree
            while len(transactions) > 1:
                new_level = []
                for i in range(0, len(transactions), 2):
                    left = transactions[i]
                    right = transactions[i + 1] if i + 1 < len(transactions) else left
                    parent = f"Hash({left}+{right})"
                    new_level.append(parent)
                    G.add_edge(parent, left)
                    G.add_edge(parent, right)
                transactions = new_level

            # Create a graph for visualization using pydot
            pydot_graph = pydot.Dot(graph_type='digraph')

            # Add nodes and edges to the pydot graph
            for node in G.nodes:
                pydot_graph.add_node(pydot.Node(node))
            for u, v in G.edges:
                pydot_graph.add_edge(pydot.Edge(u, v))

            # Generate a visualization using pydot
            graph_image = pydot_graph.create_png()

            # Display the image in Tkinter canvas
            fig = Figure(figsize=(8, 6))
            ax = fig.add_subplot(111)
            ax.imshow(graph_image)
            ax.axis('off')
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def simulate_spv_verification(self):
        transaction = self.transaction_details.get().strip()
        block = self.block_id.get().strip()

        if not transaction:
            messagebox.showerror("Input Error", "Please provide the Transaction ID.")
            return

        try:
            params = {"tx_id": transaction}
            if block:
                params["block_index"] = int(block)

            response = requests.get(VERIFY_TRANSACTION_URL, params=params)

            if response.status_code == 200:
                result = response.json()
                print(f"Response JSON: {result}")  # Debugging
            
            # Check if transaction was found based on the message or transaction details
                if result.get("message") == "Transaction found" and result.get("transaction"):
                    messagebox.showinfo("Verification Success", "Transaction Verified Successfully!")
                else:
                    messagebox.showerror("Verification Failed", "Transaction Verification Failed!")
            else:
                messagebox.showerror("Error", "Doesn't exist")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def simulate_network_communication(self):
        # Simulate network communication and update logs
        self.network_display.insert(tk.END, "Starting communication...\n")
        self.network_display.insert(tk.END, "Communication successful!\n")
        self.network_display.yview(tk.END)

    def mouse_wheel_scroll(self, event):
        if event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        else:
            self.canvas.yview_scroll(1, "units")

def run_gui():
    root = tk.Tk()
    gui = SPVGUI(root)
    root.mainloop()

run_gui()
