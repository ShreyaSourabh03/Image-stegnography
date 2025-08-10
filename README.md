# Image-stegnography
Image Steganography Application is a Python + Tkinter tool to hide and retrieve secret text in images using Least Significant Bit (LSB) steganography. Supports PNG/JPG formats, features a simple GUI, lossless encoding/decoding, and is perfect for learning or basic secure communication.
The application supports popular image formats such as PNG, JPG, and JPEG. Users can choose to encode a message by selecting a cover image, entering the desired secret text, and saving the resulting steganographic image. For decoding, users can simply load an encoded image, and the application will extract and display the hidden message instantly.

The core functionality is based on the LSB method, where each character of the secret message is converted into binary form and embedded into the least significant bits of the image’s pixel data. This subtle modification is visually imperceptible, ensuring that the image’s appearance remains unchanged while securely storing the message. To ensure accurate retrieval, a special termination marker (%%%) is appended to the message before encoding. During decoding, the application reads pixel data, reconstructs the binary message, and stops at the termination marker, guaranteeing precise extraction.

Key Features:

Simple, minimalistic, and intuitive graphical interface.

Lossless message embedding and extraction.

Support for multiple image formats.

Cross-platform compatibility with Python 3.

No prior knowledge of steganography required.

Technical Stack:

Python 3.x for application logic.

Tkinter for building the graphical user interface.

Pillow (PIL) for image processing and pixel-level data manipulation.

This application serves as both a practical utility and an educational resource. It is well-suited for students, hobbyists, and cybersecurity enthusiasts who wish to learn about steganography, data hiding, and image manipulation. Its compact codebase provides a clear example of how LSB steganography can be implemented in Python, making it an excellent starting point for further exploration into image security techniques.


