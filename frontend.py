import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ADD_BLOCK_URL = "http://127.0.0.1:5000/create_block"
VERIFY_TRANSACTION_URL = "http://127.0.0.1:5000/verify_transaction"

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
            background="#4CAF50",
            foreground="#ffffff",
        )
        style.map(
            "TButton",
            background=[("active", "#45a049"), ("disabled", "#d3d3d9")],
            foreground=[("active", "#ffffff"), ("disabled", "#888888")]
        )

    def create_heading(self):
        heading_label = tk.Label(
            self.scrollable_frame,
            text="SPV VERIFICATION",
            font=("Arial Black", 28, "bold"),
            fg="#ffffff",
            bg="#1e1e2e",
        )
        heading_label.pack(pady=(20, 40))  # Centralized with padding adjustments

    def create_spv_verification_section(self):
        spv_frame = tk.LabelFrame(
            self.scrollable_frame,
            text="SPV Verification Process",
            padx=20,
            pady=20,
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#1e1e2e",
            bd=3,
            relief="solid"
        )
        spv_frame.pack(padx=40, pady=20, fill="x")

        ttk.Label(
            spv_frame, text="Enter Transaction ID:", background="#ffffff", font=("Arial", 12)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.transaction_details = ttk.Entry(spv_frame, width=40, font=("Arial", 12))
        self.transaction_details.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(
            spv_frame, text="Select Block ID:", background="#ffffff", font=("Arial", 12)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.block_id = ttk.Entry(spv_frame, width=40, font=("Arial", 12))
        self.block_id.grid(row=1, column=1, padx=10, pady=10)

        verify_button = ttk.Button(
            spv_frame, text="Verify Transaction", command=self.simulate_spv_verification
        )
        verify_button.grid(row=2, column=0, columnspan=2, pady=20)

    def create_network_communication_section(self):
        network_frame = tk.LabelFrame(
            self.scrollable_frame,
            text="Network Communication Overview",
            padx=20,
            pady=20,
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#1e1e2e",
            bd=3,
            relief="solid"
        )
        network_frame.pack(padx=40, pady=20, fill="x")

        self.network_display = tk.Text(
            network_frame, height=8, wrap=tk.WORD, bg="#f5f5f5", font=("Arial", 12), width=80
        )
        self.network_display.grid(row=0, column=0, padx=10, pady=10)

        start_communication_button = ttk.Button(
            network_frame, text="Start Network Communication", command=self.simulate_network_communication
        )
        start_communication_button.grid(row=1, column=0, pady=10)

        clear_button = ttk.Button(
            network_frame,
            text="Clear Logs",
            command=lambda: self.network_display.delete(1.0, tk.END),
        )
        clear_button.grid(row=2, column=0, pady=10)

    def create_merkle_tree_section(self):
        merkle_frame = tk.LabelFrame(
            self.scrollable_frame,
            text="Merkle Tree Visualization",
            padx=20,
            pady=20,
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#1e1e2e",
            bd=3,
            relief="solid"
        )
        merkle_frame.pack(padx=40, pady=20, fill="x")

        merkle_button = ttk.Button(
            merkle_frame, text="Generate and Visualize Merkle Tree", command=self.generate_merkle_tree
        )
        merkle_button.pack(pady=20)

        self.canvas_frame = tk.Frame(merkle_frame, bg="#ffffff")
        self.canvas_frame.pack(fill="both", expand=True)

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
                messagebox.showerror("Server Error", f"Error: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def generate_merkle_tree(self):
        transactions = ["tx1", "tx2", "tx3", "tx4"]
        G = nx.DiGraph()

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

        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
        nx.draw(G, pos, with_labels=True, ax=ax, font_weight="bold", node_size=2000, node_color="lightblue")
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def simulate_network_communication(self):
        try:
            self.network_display.insert(tk.END, "Simulating network communication...\n")
            self.network_display.insert(tk.END, "Sending request to the server...\n")
            self.network_display.insert(tk.END, "Waiting for response...\n")
            response = "Network communication successful!"
            self.network_display.insert(tk.END, f"Response: {response}\n")
        except Exception as e:
            self.network_display.insert(tk.END, f"Error: {str(e)}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = SPVGUI(root)
    root.mainloop()
