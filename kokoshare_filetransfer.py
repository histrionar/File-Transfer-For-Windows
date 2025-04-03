import tkinter as tk
from tkinter import ttk
import socket
import threading
import os
from tkinter import filedialog, messagebox
import webbrowser
from tkinter import PhotoImage
import sys

# Warna & Tema yang lebih modern
BG_COLOR = "#1E293B"  # Darker background
FG_COLOR = "#F8FAFC"  # Light text
BUTTON_COLOR = "#3B82F6"  # Blue
BUTTON_COLOR_G = "#107d4e"  # Green
BUTTON_HOVER = "#2563EB"  # Darker blue for hover
FONT = ("Arial", 12)

class FileTransferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KokoShare - File Transfer V1.1.2")
        self.root.geometry("600x550")
        self.root.config(bg=BG_COLOR)
        
        # Mendapatkan path ke file PNG dalam bundle exe
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, 'app_icon.png')

        try:
            # Memuat ikon PNG menggunakan PhotoImage
            icon = tk.PhotoImage(file=icon_path)
            root.tk.call('wm', 'iconphoto', root._w, icon)
        except Exception as e:
            print(f"Error loading icon: {e}")

        # Menetapkan ikon untuk aplikasi
        root.tk.call('wm', 'iconphoto', root._w, icon)
                

        # Tab Navigasi
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Tab utama - File Transfer
        self.tab_main = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.tab_main, text="Transfer File")

        # Tab Cara Pakai
        self.tab_usage = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.tab_usage, text="Tutorial")

        # Tab About
        self.tab_about = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.tab_about, text="About")

        # Konten Transfer File (File Transfer)
        self.create_home_ui()

        # Konten Tutorial
        self.create_usage_ui()

        # Konten Tentang
        self.create_about_ui()

    def create_home_ui(self):
        """UI untuk File Transfer"""
        tk.Label(self.tab_main, text="🔄 File Transfer", font=("Helvetica", 20, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack(pady=20)

        self.mode = tk.StringVar(value="send")
        switch_frame = tk.Frame(self.tab_main, bg=BG_COLOR)
        switch_frame.pack(pady=15)

        tk.Radiobutton(switch_frame, text="📤 Kirim", variable=self.mode, value="send", font=FONT, bg=BG_COLOR, fg=FG_COLOR, selectcolor=BG_COLOR, command=self.update_ui).pack(side="left", padx=15)
        tk.Radiobutton(switch_frame, text="📥 Terima", variable=self.mode, value="receive", font=FONT, bg=BG_COLOR, fg=FG_COLOR, selectcolor=BG_COLOR, command=self.update_ui).pack(side="left", padx=15)

        self.content_frame = tk.Frame(self.tab_main, bg=BG_COLOR)
        self.content_frame.pack(pady=20)

        self.update_ui()

    def update_ui(self):
        """Memperbarui UI sesuai mode yang dipilih"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if self.mode.get() == "send":
            self.create_send_ui()
        else:
            self.create_receive_ui()

    def create_send_ui(self):
        """UI untuk mengirim file"""
        tk.Label(self.content_frame, text="Pilih File:", font=FONT, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
        self.entry_file = tk.Entry(self.content_frame, width=30, font=FONT, bg="#334155", fg=FG_COLOR, bd=2, relief="flat")
        self.entry_file.pack(pady=10)

        tk.Button(self.content_frame, text="📂 Pilih File", font=FONT, bg=BUTTON_COLOR, fg=FG_COLOR, activebackground=BUTTON_HOVER, command=self.choose_file).pack(pady=10, ipadx=15, ipady=5)

        tk.Label(self.content_frame, text="Masukkan IP Tujuan:", font=FONT, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
        self.ip_entry = tk.Entry(self.content_frame, width=30, font=FONT, bg="#334155", fg=FG_COLOR, bd=2, relief="flat")
        self.ip_entry.pack(pady=10)

        tk.Button(self.content_frame, text="📤 Kirim File", font=FONT, bg=BUTTON_COLOR, fg=FG_COLOR, activebackground=BUTTON_HOVER, command=self.send_file).pack(pady=15, ipadx=20, ipady=10)

    def create_receive_ui(self):
        """UI untuk menerima file otomatis"""
        ip_address = socket.gethostbyname(socket.gethostname())
        tk.Label(self.content_frame, text=f"💻 IP Anda: {ip_address}", font=FONT, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)

        self.status_label = tk.Label(self.content_frame, text="🔄 Menerima file...", font=FONT, bg=BG_COLOR, fg="orange")
        self.status_label.pack(pady=20)

        # Mulai server otomatis
        self.start_server()

    def choose_file(self):
        """Memilih file untuk dikirim"""
        file_path = filedialog.askopenfilename(title="Pilih file untuk dikirim")
        if file_path:
            self.entry_file.delete(0, tk.END)
            self.entry_file.insert(0, file_path)

    def send_file(self):
        """Mengirim file ke penerima"""
        file_path = self.entry_file.get()
        if not file_path:
            messagebox.showerror("Error", "Pilih file terlebih dahulu!")
            return

        server_ip = self.ip_entry.get().strip()
        if not server_ip:
            messagebox.showerror("Error", "Masukkan IP tujuan!")
            return

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, 5507))

            file_name = os.path.basename(file_path)
            client_socket.send(file_name.encode())

            with open(file_path, "rb") as file:
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    client_socket.send(data)

            client_socket.close()
            messagebox.showinfo("Sukses", "File berhasil dikirim!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengirim file: {e}")

    def start_server(self):
        """Menerima file dari pengirim"""
        def server_thread():
            try:
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.bind(("", 5507))
                server_socket.listen(1)

                while True:
                    conn, addr = server_socket.accept()

                    # Menerima nama file
                    file_name = conn.recv(1024).decode(errors="ignore")
                    
                    # Memilih lokasi penyimpanan file
                    save_path = filedialog.asksaveasfilename(initialfile=file_name, title="Simpan File")
                    if not save_path:
                        conn.close()
                        continue

                    # Menerima dan menyimpan file dalam mode BINARY
                    with open(save_path, "wb") as file:
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            file.write(data)

                    conn.close()
                    self.status_label.config(text="✅ File diterima!")
                    messagebox.showinfo("Sukses", f"File '{file_name}' berhasil diterima!")

            except Exception as e:
                messagebox.showerror("Error", f"Gagal menerima file: {e}")

        threading.Thread(target=server_thread, daemon=True).start()

    def create_usage_ui(self):
        """UI untuk halaman Cara Pakai"""
        tk.Label(self.tab_usage, text="Cara Pakai", font=("Helvetica", 20, "bold"), fg=FG_COLOR, bg=BG_COLOR).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=20)

        usage_text = (
            "1. Pilih mode Kirim atau Terima.\n"
            "2. Untuk mode Kirim, pilih file dan masukkan IP tujuan.\n"
            "3. Untuk mode Terima, cukup jalankan aplikasi dan tunggu file yang masuk."
        )

        tk.Label(self.tab_usage, text=usage_text, font=FONT, fg=FG_COLOR, bg=BG_COLOR, justify="left").grid(row=1, column=0, columnspan=2, sticky="w", padx=20, pady=20)

    def create_about_ui(self):
        """UI untuk halaman About"""
        tk.Label(self.tab_about, text="Tentang Aplikasi", font=("Arial", 20, "bold"), fg=FG_COLOR, bg=BG_COLOR).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=20)

        about_text = (
            "Aplikasi File Transfer ini memungkinkan Anda untuk mengirim dan menerima  \n"
            "file antar perangkat. \n"
            "Penggunaan sangat sederhana, cukup pilih mode Kirim atau Terima, \n"
            "dan ikuti instruksi."
        )
        tk.Label(self.tab_about, text=about_text, font=FONT, fg=FG_COLOR, bg=BG_COLOR, justify="left").grid(row=1, column=0, columnspan=2, sticky="w", padx=20, pady=20)

        # Informasi Developer dan Versi
        developer_info = f"Developer: Rizko Imsar\nVersi: 1.1.2\nPublisher: KokoDocs"
        tk.Label(self.tab_about, text=developer_info, font=FONT, fg=FG_COLOR, bg=BG_COLOR, justify="left").grid(row=2, column=0, columnspan=2, sticky="w", padx=20, pady=20)

        # Tombol Links
        self.create_social_links()

    def create_social_links(self):
        """Menambahkan tombol link tanpa ikon"""
        button_frame = tk.Frame(self.tab_about, bg=BG_COLOR)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="w", padx=20, pady=30)

        # Tombol GitHub
        github_button = tk.Button(button_frame, text="Visit My GitHub", font=FONT, bg=BUTTON_COLOR_G, fg=FG_COLOR, activebackground=BUTTON_HOVER, command=self.open_github)
        github_button.grid(row=0, column=0, padx=10, pady=5)

    def open_github(self):
        """Membuka halaman GitHub"""
        webbrowser.open("https://github.com/rizko77")


# Jalankan aplikasi

root = tk.Tk()
app = FileTransferApp(root)
root.mainloop()
