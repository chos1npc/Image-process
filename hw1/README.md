Program Functions
Read and write image files, and rotate images before saving them.

Program Flow or Algorithm

Step 1: Define the Python GUI tkinter window title as "AIP61147050S."
Step 2: Create a button1 that, when clicked, opens a file from the computer (limited to JPG/BMP/PPM).
Step 3: Call the command function Openfile within button1.
Step 4: Use askopenfile to open a file within the system, process the image using Pillow, and resize it proportionally.
Step 5: Place the resized image in a photoimage and display it using a label.
Step 6: Create a button2 that rotates the image from button1.
Step 7: Call the command function transpose within button2.
Step 8: Use Pillow to rotate the image and place it in a photoimage, then display it using a label.




