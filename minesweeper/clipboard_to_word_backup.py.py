from docx import Document
from PIL import ImageGrab
from io import BytesIO
from tkinter import *
from tkinter import ttk, filedialog
import time
import threading

class ClipboardCopier:
    
    image_list = []
    
    def __init__(self):
        self.go_on = True
    
    def get_image(self):
        try:
            clipboard_item = ImageGrab.grabclipboard()
            return clipboard_item
        except AttributeError:
            return None
        
    def create_document(self):
        file_location = save_file_dialog()
        doc = Document()
        image_list = self.image_list
        
        for image in image_list:
            doc.add_picture(image)
        doc.save(file_location)
 
    def stream(self):
        previous_clipboard = self.get_image()
        
        while self.go_on:
            current_clipboard = self.get_image()
            if previous_clipboard != current_clipboard:
                try:
                    image_stream = BytesIO()
                    previous_clipboard.save(image_stream, format="PNG")
                    self.image_list.append(image_stream)
                    print("Image saved!")
                    previous_clipboard = current_clipboard
                except AttributeError:
                    previous_clipboard = current_clipboard
            time.sleep(1)
           
        current_clipboard = self.get_image()
        try:
            image_stream = BytesIO()
            current_clipboard.save(image_stream, format = "PNG")
            self.image_list.append(image_stream)
            print("Last image saved!")
            print("Saving complete.")
        except AttributeError:
            print("Saving complete.")
    
    def stop_streaming(self):
        self.go_on = False
    
                
cc = ClipboardCopier()
def save_file_dialog():
    file_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Files", "*.docx"), ("All files", "*.*")])
    return file_path


def main():
    stream_thread = threading.Thread(target = cc.stream).start
    stop_thread = threading.Thread(target = cc.stop_streaming).start
    file_thread = threading.Thread(target = cc.create_document).start
                      
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
   
    ttk.Label(frm, text="Copy images!").grid(column=0, row=0)
    ttk.Button(frm, text="Start", command = stream_thread).grid(column=1, row=0)
    ttk.Button(frm, text="Stop", command = stop_thread).grid(column=1, row=1)
    ttk.Button(frm, text="Create File", command = file_thread).grid(column=2, row=0)
    ttk.Button(frm, text="Quit", command = root.destroy).grid(column=2, row=1)
    root.mainloop()
if __name__ == "__main__":
    main()

    
            
            