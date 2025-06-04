
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from tkinter import Tk
from tkinter import filedialog

def select_image():
    root = Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
    return image_path

def detect_parking_slots(image_path):
    num_rows = 10
    num_cols = 13
    threshold = 100

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape
    slot_height = height // num_rows
    slot_width = width // num_cols

    slots = []
    occupied_count = 0
    available_count = 0
    for row in range(num_rows):
        for col in range(num_cols):
            x = col * slot_width
            y = row * slot_height
            slot_img = image[y:y + slot_height, x:x + slot_width]
            gray_slot = cv2.cvtColor(slot_img, cv2.COLOR_RGB2GRAY)
            mean_intensity = np.mean(gray_slot)
            status = 'Occupied' if mean_intensity < threshold else 'Available'
            if status == 'Occupied':
                occupied_count += 1
            else:
                available_count += 1
            slots.append({'Row': row, 'Col': col, 'Status': status, 'X': x, 'Y': y})

    return {
        'Total Number of Slots': num_rows * num_cols,
        'Occupied Slots': occupied_count,
        'Available Slots': available_count
    }, image, slots

def visualize(image, slots):
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.imshow(image)
    for slot in slots:
        color = 'red' if slot['Status'] == 'Occupied' else 'green'
        rect = Rectangle((slot['X'], slot['Y']), image.shape[1] // 13, image.shape[0] // 10, linewidth=1.5, edgecolor=color, facecolor='none')
        ax.add_patch(rect)
        ax.text(slot['X'] + 5, slot['Y'] + 15, f"{slot['Status'][0]}", color=color, fontsize=8)
    plt.axis('off')
    plt.show()

def save_to_csv(output):
    df = pd.DataFrame([output])
    df.to_csv('parking slots status.csv', index=False)
    print("Output saved to parking slots status.csv")

def main():
    image_path = select_image()
    if image_path:
        output, image, slots = detect_parking_slots(image_path)
        print("Parking Lot Status:")
        for key, value in output.items():
            print(f"{key}: {value}")
        save_to_csv(output)
        visualize(image, slots)
    else:
        print("No image selected.")

if __name__ == "__main__":
    main()
