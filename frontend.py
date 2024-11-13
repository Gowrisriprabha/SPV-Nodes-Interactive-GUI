import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter, ImageEnhance

class SPVGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SPV Verification Process")
        self.root.geometry("800x600")
        self.set_background_image("C:\\Users\\Gowri sri\\OneDrive\\Desktop\\blockchain project\\SPV-Nodes-Interactive-GUI\\image.jpg")

        self.create_heading()
        self.main_container = tk.Frame(self.root, bg='white', padx=30, pady=30)
        self.main_container.pack(expand=True)
        self.create_spv_verification_section()
        self.create_network_communication_section()
        self.create_merkle_tree_section()
    
    def set_background_image(self, image_path):
        image = Image.open(image_path)
        blurred_image = image.filter(ImageFilter.GaussianBlur(10))
        enhancer = ImageEnhance.Brightness(blurred_image)
        darkened_image = enhancer.enhance(0.4)
        darkened_image = darkened_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(darkened_image)
        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_heading(self):
        heading_label = tk.Label(
            self.root,
            text="SPV VERIFICATION",
            font=("Lucida", 24, "italic"),
            fg="white",
            bg="#333333",
            pady=10
        )
        heading_label.pack(pady=(20, 10))

    def create_spv_verification_section(self):
        spv_frame = tk.LabelFrame(self.main_container, text="SPV Verification Process", padx=10, pady=10, bg='white')
        spv_frame.pack(padx=20, pady=10, fill="both")
        tk.Label(spv_frame, text="Enter Transaction Details:", bg='white').grid(row=0, column=0, padx=5, pady=5)
        self.transaction_details = tk.Entry(spv_frame, width=40)
        self.transaction_details.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(spv_frame, text="Select Block ID:", bg='white').grid(row=1, column=0, padx=5, pady=5)
        self.block_id = tk.Entry(spv_frame, width=40)
        self.block_id.grid(row=1, column=1, padx=5, pady=5)
        self.verify_button = tk.Button(spv_frame, text="Verify Transaction", command=self.toggle_spv_verification)
        self.verify_button.grid(row=2, columnspan=2, pady=10)
        self.verify_enabled = True

    def toggle_spv_verification(self):
        if self.verify_enabled:
            self.simulate_spv_verification()
        self.verify_enabled = not self.verify_enabled
        self.verify_button.config(text="Enable Verification" if not self.verify_enabled else "Verify Transaction")

    def create_network_communication_section(self):
        network_frame = tk.LabelFrame(self.main_container, text="Network Communication Overview", padx=10, pady=10, bg='white')
        network_frame.pack(padx=20, pady=10, fill="both")
        self.network_display = tk.Text(network_frame, height=10, width=50, wrap=tk.WORD, bg='white')
        self.network_display.grid(row=0, column=0, padx=5, pady=5)
        self.start_communication_button = tk.Button(network_frame, text="Start Network Communication", command=self.toggle_network_communication)
        self.start_communication_button.grid(row=1, column=0, pady=10)
        self.network_comm_enabled = True

    def toggle_network_communication(self):
        if self.network_comm_enabled:
            self.simulate_network_communication()
        self.network_comm_enabled = not self.network_comm_enabled
        self.start_communication_button.config(text="Enable Communication" if not self.network_comm_enabled else "Start Network Communication")

    def create_merkle_tree_section(self):
        merkle_frame = tk.LabelFrame(self.main_container, text="Merkle Tree Generation", padx=10, pady=10, bg='white')
        merkle_frame.pack(padx=20, pady=10, fill="both")
        self.merkle_button = tk.Button(merkle_frame, text="Generate Merkle Tree", command=self.toggle_merkle_tree)
        self.merkle_button.grid(row=0, column=0, pady=10)
        self.merkle_enabled = True

    def toggle_merkle_tree(self):
        if self.merkle_enabled:
            self.generate_merkle_tree()
        self.merkle_enabled = not self.merkle_enabled
        self.merkle_button.config(text="Enable Merkle Generation" if not self.merkle_enabled else "Generate Merkle Tree")

    def simulate_spv_verification(self):
        transaction = self.transaction_details.get()
        block = self.block_id.get()
        if not transaction or not block:
            messagebox.showerror("Input Error", "Please provide both transaction details and block ID.")
            return
        self.network_display.insert(tk.END, f"SPV Client: Verifying Transaction {transaction} in Block {block}...\n")
        self.network_display.insert(tk.END, "SPV Client: Requesting Merkle Proof from Full Node...\n")
        self.network_display.insert(tk.END, "Full Node: Sending Merkle Proof for Transaction...\n")
        self.network_display.insert(tk.END, "SPV Client: Verifying Transaction with Merkle Proof...\n")
        self.network_display.insert(tk.END, "SPV Client: Transaction Verified Successfully!\n\n")

    def simulate_network_communication(self):
        self.network_display.insert(tk.END, "SPV Client: Sending Request for Block Header...\n")
        self.network_display.insert(tk.END, "Full Node: Sending Block Header Response...\n")
        self.network_display.insert(tk.END, "SPV Client: Requesting Merkle Proof for Transaction...\n")
        self.network_display.insert(tk.END, "Full Node: Sending Merkle Proof...\n")
        self.network_display.insert(tk.END, "SPV Client: Transaction Verification Completed!\n\n")

    def generate_merkle_tree(self):
        self.network_display.insert(tk.END, "Merkle Tree: Generating Merkle Tree...\n")
        self.network_display.insert(tk.END, "Merkle Tree: Hashing Transaction Data...\n")
        self.network_display.insert(tk.END, "Merkle Tree: Combining Hashes...\n")
        self.network_display.insert(tk.END, "Merkle Tree: Merkle Root Created!\n\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SPVGUI(root)
    root.mainloop()
