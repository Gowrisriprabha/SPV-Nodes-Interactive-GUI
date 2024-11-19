import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk, ImageFilter, ImageEnhance

ADD_BLOCK_URL = "http://127.0.0.1:5000/create_block"
VERIFY_TRANSACTION_URL = "http://127.0.0.1:5000/verify_transaction"

class SPVGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SPV Verification Process")
        self.root.geometry("800x600")
        self.set_background_image(r"C:\Users\Gowri sri\OneDrive\Desktop\New folder\SPV-Nodes-Interactive-GUI\image.jpg")

        self.create_heading()
        self.main_container = tk.Frame(self.root, bg='white', padx=30, pady=30)
        self.main_container.pack(expand=True)
        self.create_spv_verification_section()
        self.create_network_communication_section()
        self.create_merkle_tree_section()

    def set_background_image(self, image_path):
        image = Image.open(image_path).filter(ImageFilter.GaussianBlur(10))
        self.background_label = tk.Label(self.root)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.update_background_image(image)
        self.root.bind('<Configure>', lambda event: self.update_background_image(image))

    def update_background_image(self, image):
        resized_image = image.resize((self.root.winfo_width(), self.root.winfo_height()))
        darkened_image = ImageEnhance.Brightness(resized_image).enhance(0.4)
        self.background_image = ImageTk.PhotoImage(darkened_image)
        self.background_label.config(image=self.background_image)

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
        self.verify_button = tk.Button(spv_frame, text="Verify Transaction", command=self.simulate_spv_verification)
        self.verify_button.grid(row=2, columnspan=2, pady=10)

    def create_network_communication_section(self):
        network_frame = tk.LabelFrame(self.main_container, text="Network Communication Overview", padx=10, pady=10, bg='white')
        network_frame.pack(padx=20, pady=10, fill="both")
        self.network_display = tk.Text(network_frame, height=10, width=50, wrap=tk.WORD, bg='white')
        self.network_display.grid(row=0, column=0, padx=5, pady=5)
        self.start_communication_button = tk.Button(network_frame, text="Start Network Communication", command=self.simulate_network_communication)
        self.start_communication_button.grid(row=1, column=0, pady=10)
        clear_button = tk.Button(network_frame, text="Clear Logs", command=lambda: self.network_display.delete(1.0, tk.END))
        clear_button.grid(row=2, column=0, pady=10)

    def create_merkle_tree_section(self):
        merkle_frame = tk.LabelFrame(self.main_container, text="Merkle Tree Generation", padx=10, pady=10, bg='white')
        merkle_frame.pack(padx=20, pady=10, fill="both")
        self.merkle_button = tk.Button(merkle_frame, text="Generate Merkle Tree", command=self.generate_merkle_tree)
        self.merkle_button.grid(row=0, column=0, pady=10)

    def simulate_spv_verification(self):
        transaction = self.transaction_details.get().strip()
        block = self.block_id.get().strip()

        if not transaction or not block:
            messagebox.showerror("Input Error", "Please provide both transaction details and block ID.")
            return

        try:
            response = requests.post(VERIFY_TRANSACTION_URL, json={"txid": transaction, "block": block})
            if response.status_code == 200:
                result = response.json()
                if result.get("verified"):
                    messagebox.showinfo("Verification Success", "Transaction Verified Successfully!")
                else:
                    messagebox.showerror("Verification Failed", "Transaction Verification Failed!")
            else:
                print(f"Server Error: {response.status_code} - {response.text}")
                messagebox.showerror("Error", f"Server Error: {response.text}")
        except Exception as e:
            print(f"Error during SPV Verification: {str(e)}")
            messagebox.showerror("Error", str(e))

    def generate_merkle_tree(self):
        try:
            transactions = ["tx1", "tx2", "tx3"]  # Replace with meaningful data as needed
            response = requests.post(ADD_BLOCK_URL, json={"transactions": transactions})
            if response.status_code == 200:
                messagebox.showinfo("Merkle Tree", "Merkle Tree Generated and Block Added!")
            else:
                print(f"Server Error: {response.status_code} - {response.text}")
                messagebox.showerror("Error", f"Server Error: {response.text}")
        except Exception as e:
            print(f"Error during Merkle Tree Generation: {str(e)}")
            messagebox.showerror("Error", str(e))

    def simulate_network_communication(self):
        self.network_display.insert(tk.END, "SPV Client: Sending Request for Block Header...\n")
        self.network_display.insert(tk.END, "Full Node: Sending Block Header Response...\n")
        self.network_display.insert(tk.END, "SPV Client: Requesting Merkle Proof for Transaction...\n")
        self.network_display.insert(tk.END, "Full Node: Sending Merkle Proof...\n")
        self.network_display.insert(tk.END, "SPV Client: Transaction Verification Completed!\n\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SPVGUI(root)
    root.mainloop()
