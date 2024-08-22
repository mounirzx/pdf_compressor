import os
import sys
import ctypes
import subprocess
from tkinter import Tk, filedialog, Button, Label, PhotoImage, StringVar, Frame, ttk
from threading import Thread
import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Define the path to Ghostscript
GHOSTSCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'gs', 'gswin64c.exe')

def get_unique_filename(filepath):
    base, ext = os.path.splitext(filepath)
    counter = 1
    new_filepath = filepath
    while os.path.exists(new_filepath):
        new_filepath = f"{base} ({counter}){ext}"
        counter += 1
    return new_filepath

def compress_pdf(input_pdf, output_pdf, progress_callback):
    try:
        start_time = time.time()
        command = [
            GHOSTSCRIPT_PATH,
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/screen',
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            f'-sOutputFile={output_pdf}',
            input_pdf
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        while process.poll() is None:
            elapsed_time = time.time() - start_time
            progress = 50  # Placeholder for progress percentage
            progress_callback(progress)
            time.sleep(1)  # Adjust polling interval as needed
        
        process.wait()
        progress_callback(100)  # Final progress update
        return True
    except Exception as e:
        print(f"Error during compression: {e}")
        progress_callback(0)  # Reset progress in case of error
        return False

def run_compression(input_pdf, output_pdf):
    def progress_callback(progress):
        progress_var.set(progress)
        progress_label.config(text=f"{progress}%")
        root.update_idletasks()
    
    # Hide the upload button and show the progress bar
    upload_button.pack_forget()
    progress_bar_frame.pack(pady=20, fill='x')
    progress_bar.pack(fill='x', padx=20)
    
    # Run compression in a separate thread to avoid blocking the GUI
    success = compress_pdf(input_pdf, output_file, progress_callback)
    
    # Hide the progress bar and show the upload button
    progress_bar_frame.pack_forget()
    upload_button.pack(pady=20)
    
    if success:
        result_var.set(f"Compression complete! Saved as: {output_file}")
    else:
        result_var.set("Compression failed!")

def open_file_dialog():
    global output_file  # Define as global to be accessible in run_compression
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        output_file = get_unique_filename(os.path.splitext(file_path)[0] + "_compressed.pdf")
        # Run compression in a separate thread to avoid blocking the GUI
        compression_thread = Thread(target=run_compression, args=(file_path, output_file))
        compression_thread.start()

if __name__ == "__main__":
    if is_admin():
        root = Tk()
        root.title("PDF Compressor")
        root.geometry("600x400")
        root.config(bg="#f7f7f7")

        # Add an icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'images', 'logo.png')
            root.iconphoto(False, PhotoImage(file=icon_path))
        except Exception as e:
            print(f"Error loading icon: {e}")

        # Add a logo
        try:
            logo_path = os.path.abspath(os.path.join('images', 'logo.png'))
            logo = PhotoImage(file=logo_path)
            logo_label = Label(root, image=logo, bg="#f7f7f7")
            logo_label.image = logo  # Keep a reference to avoid garbage collection
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading logo: {e}")

        # Add title
        title_label = Label(root, text="PDF Compressor", font=("Helvetica", 24, "bold"), bg="#f7f7f7", fg="#333")
        title_label.pack(pady=10)

        # Add upload button
        upload_button = Button(root, text="Upload PDF", font=("Helvetica", 16), command=open_file_dialog, bg="#007bff", fg="white", relief="flat", width=20)
        upload_button.pack(pady=20)

        # Progress bar frame with margin
        progress_bar_frame = Frame(root, bg="#f7f7f7")
        progress_var = StringVar()
        progress_bar = ttk.Progressbar(progress_bar_frame, length=300, mode='determinate', maximum=100, variable=progress_var)
        progress_label = Label(progress_bar_frame, text="0%", font=("Helvetica", 12), bg="#f7f7f7", fg="#333")

        # Pack progress bar and label
        progress_bar.pack(fill='x', padx=20)
        progress_label.pack()

        # Result label
        result_var = StringVar()
        result_var.set("")
        result_label = Label(root, textvariable=result_var, font=("Helvetica", 12), bg="#f7f7f7", fg="#333", wraplength=550)
        result_label.pack(pady=10, padx=20, fill='x')

        # Footer with developer name and copyright
        footer = Frame(root, bg="#f7f7f7")
        footer.pack(side='bottom', fill='x', pady=10)

        developer_label = Label(footer, text="Developed by Abes Mounir", font=("Helvetica", 10), bg="#f7f7f7", fg="#777")
        developer_label.pack(side='left', padx=10)

        copyright_label = Label(footer, text="© 2024", font=("Helvetica", 10), bg="#f7f7f7", fg="#777")
        copyright_label.pack(side='right', padx=10)

        root.mainloop()
    else:
        # Re-run the script with administrator privileges, hiding the console
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 0
        )
