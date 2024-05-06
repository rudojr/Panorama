import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from main import Panaroma
import imutils

class PanoramaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Panorama Image Stitching App")

        self.label1 = tk.Label(root, text="Enter the number of images you want to concatenate:")
        self.label1.pack()

        self.num_images_entry = tk.Entry(root)
        self.num_images_entry.pack()

        self.browse_button = tk.Button(root, text="Browse Images", command=self.browse_images)
        self.browse_button.pack()

        self.stitch_button = tk.Button(root, text="Stitch Images", command=self.stitch_images)
        self.stitch_button.pack()

    def browse_images(self):
        num_images = self.num_images_entry.get()
        if not num_images.isdigit() or int(num_images) < 2:
            messagebox.showinfo("Error", "Please enter a valid number of images.")
            return

        num_images = int(num_images)

        self.images = []
        for i in range(num_images):
            filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
            if filename:
                image = cv2.imread(filename)
                if image is not None:
                    self.images.append(image)
                else:
                    messagebox.showinfo("Error", f"Unable to read image {filename}")

    def stitch_images(self):
        if not hasattr(self, 'images') or len(self.images) < 2:
            messagebox.showinfo("Error", "Please select at least 2 images.")
            return

        for i in range(len(self.images)):
            self.images[i] = imutils.resize(self.images[i], width=400, height=400)

        panorama = Panaroma()
        if len(self.images) == 2:
            (result, matched_points) = panorama.image_stitch([self.images[0], self.images[1]], match_status=True)
        else:
            (result, matched_points) = panorama.image_stitch([self.images[-2], self.images[-1]], match_status=True)
            for i in range(len(self.images) - 2):
                (result, matched_points) = panorama.image_stitch([self.images[-i - 3], result], match_status=True)

        if result is not None and matched_points is not None:
            cv2.imshow("Keypoint Matches", matched_points)
            cv2.imshow("Panorama", result)

            cv2.imwrite("output/matched_points.jpg", matched_points)
            cv2.imwrite("output/panorama_image.jpg", result)

            cv2.waitKey(0)
            cv2.destroyAllWindows()

root = tk.Tk()
app = PanoramaApp(root)
root.mainloop()