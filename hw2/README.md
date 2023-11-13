Program Functions:

Read and write image files and perform image rotation before saving.
Draw a histogram of the grayscale image.

Program Flow or Algorithm

Step 1: Define the Python GUI tkinter window title as "AIP61147050S."
Step 2: Create a button1 that, when clicked, opens a file from the computer (limited to JPG/BMP/PPM).
Step 3: Call the command function Openfile within button1.
Step 4: Use askopenfile to open a file within the system, process the image using Pillow, and resize it proportionally.
Step 5: Place the resized image in a photoimage and display it using a label.
Step 6: Create a button2 that displays the grayscale histogram of the image from step 5.
Step 7: Call the command function hist().
Step 8: hist(): Convert the image to a one-dimensional array using numpy's ravel. Use plt.hist to display the histogram, with the x-axis representing 256 pixels and the y-axis displaying values between 0 and 1 (due to density=True).
Step 9: Save the histogram image as "hist.png" using plt.savefig and display it in tkinter using ImageOpen.
Step 10: Display the results of steps 8 to 10 in label3.
