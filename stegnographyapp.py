from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from io import BytesIO
import os

class SteganographyApp:
    def __init__(self):
        self.root = None
        self.encode_image = None
        self.d_image_size = 0
        self.d_image_w = 0
        self.d_image_h = 0

    def main(self, root):
        self.root = root
        root.title("Image Steganography")
        root.geometry("500x600")
        root.resizable(width=True, height=True)
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        main_frame = Frame(root)
        main_frame.grid()

        title = Label(main_frame, text="Image Steganography")
        title.config(font=('Courier', 30))
        title.grid(row=1, pady=10)

        encode_btn = Button(main_frame, text='Encode', padx=14, 
                          command=lambda: self.show_encode_interface(main_frame))
        encode_btn.config(font=('Courier', 14))
        encode_btn.grid(row=2, pady=12)

        decode_btn = Button(main_frame, text='Decode', padx=14,
                          command=lambda: self.show_decode_interface(main_frame))
        decode_btn.config(font=('Courier', 14))
        decode_btn.grid(row=3, pady=12)

        ascii_art = Label(main_frame, text=''' 
       by Shreya ''')
        ascii_art.config(font=('Courier', 7))
        ascii_art.grid(row=4, pady=50)

    def show_encode_interface(self, frame):
        frame.destroy()
        encode_frame = Frame(self.root)
        
        Label(encode_frame, text='ENCODE', font=("Courier", 25)).grid(row=0, pady=20)
        
        # Image selection
        Label(encode_frame, text="Select cover image:", font=("Courier", 14)).grid(pady=10)
        Button(encode_frame, text="Browse", font=("Courier", 12),
              command=self.select_encode_image).grid(pady=5)
        
        # Text input
        Label(encode_frame, text="Secret message:", font=("Courier", 14)).grid(pady=10)
        self.encode_text = Text(encode_frame, width=40, height=5, font=("Courier", 12))
        self.encode_text.grid()
        
        # Encode button
        Button(encode_frame, text="Encode & Save", font=("Courier", 14),
              command=self.encode_and_save).grid(pady=15)
        
        # Back button
        Button(encode_frame, text="Back", font=("Courier", 12),
              command=lambda: self.return_to_main(encode_frame)).grid(pady=10)
        
        encode_frame.grid()

    def show_decode_interface(self, frame):
        frame.destroy()
        decode_frame = Frame(self.root)
        
        Label(decode_frame, text='DECODE', font=("Courier", 25)).grid(row=0, pady=20)
        
        # Image selection
        Label(decode_frame, text="Select encoded image:", font=("Courier", 14)).grid(pady=10)
        Button(decode_frame, text="Browse", font=("Courier", 12),
              command=self.decode_image).grid(pady=5)
        
        # Back button
        Button(decode_frame, text="Back", font=("Courier", 12),
              command=lambda: self.return_to_main(decode_frame)).grid(pady=10)
        
        decode_frame.grid()

    def select_encode_image(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ('Image Files', '*.png;*.jpg;*.jpeg')
        ])
        if file_path:
            try:
                self.encode_image = Image.open(file_path)
                messagebox.showinfo("Success", "Image loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")

    def encode_and_save(self):
        if not self.encode_image:
            messagebox.showerror("Error", "No image selected!")
            return
            
        secret_text = self.encode_text.get("1.0", "end-1c")
        if not secret_text:
            messagebox.showinfo("Alert", "Please enter a secret message!")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[('PNG Files', '*.png')]
        )
        
        if save_path:
            try:
                encoded_image = self.encode_image.copy()
                self.encode_data(encoded_image, secret_text)
                encoded_image.save(save_path)
                messagebox.showinfo("Success", f"Image saved successfully at:\n{save_path}")
                self.return_to_main(None)
            except Exception as e:
                messagebox.showerror("Encoding Error", str(e))

    def encode_data(self, image, data):
        data += "%%%"  # Add termination marker
        binary_data = ''.join(format(ord(char), '08b') for char in data)
        pixels = list(image.getdata())
        
        if len(binary_data) > len(pixels) * 3:
            raise ValueError("Image too small for the message")
            
        index = 0
        for i in range(len(pixels)):
            pixel = list(pixels[i])
            for j in range(3):  # RGB channels
                if index < len(binary_data):
                    pixel[j] = pixel[j] & ~1 | int(binary_data[index])
                    index += 1
            pixels[i] = tuple(pixel)
            
        image.putdata(pixels)

    def decode_image(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ('Image Files', '*.png;*.jpg;*.jpeg')
        ])
        if not file_path:
            return
            
        try:
            image = Image.open(file_path)
            decoded_text = self.decode_data(image)
            self.show_decoded_text(decoded_text)
        except Exception as e:
            messagebox.showerror("Error", f"Decoding failed:\n{str(e)}")

    def decode_data(self, image):
        pixels = list(image.getdata())
        binary_data = []
        for pixel in pixels:
            for value in pixel[:3]:  # RGB channels
                binary_data.append(str(value & 1))
                
        binary_str = ''.join(binary_data)
        decoded_text = ''
        for i in range(0, len(binary_str), 8):
            byte = binary_str[i:i+8]
            decoded_text += chr(int(byte, 2))
            if decoded_text[-3:] == '%%%':  # Termination marker
                return decoded_text[:-3]
                
        return decoded_text

    def show_decoded_text(self, text):
        window = Toplevel(self.root)
        window.title("Decoded Message")
        
        Label(window, text="Hidden Message:", font=("Courier", 14)).pack(pady=10)
        text_area = Text(window, width=50, height=10, font=("Courier", 12))
        text_area.insert(INSERT, text)
        text_area.pack(padx=20, pady=10)
        
        Button(window, text="Close", command=window.destroy).pack(pady=10)

    def return_to_main(self, frame):
        if frame:
            frame.destroy()
        self.main(self.root)

if __name__ == "__main__":
    root = Tk()
    app = SteganographyApp()
    app.main(root)
    root.mainloop()
