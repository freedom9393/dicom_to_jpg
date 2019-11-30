import os
import pydicom
import cv2
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# Folder path for .dcm images
in_path = "D:\\Projects\\Proba\\DCM"
# Folder path for storing .jpg images (it will be created if it doesn't exist)
out_path = "D:\\Projects\\Proba\\JPG"

if not os.path.isdir(out_path):
    os.mkdir(out_path)

def convert_dcm_to_jpg(input_folder, output_folder):
    if os.path.isdir(input_folder):
        for name in os.listdir(input_folder):
            if os.path.isdir(os.path.join(input_folder, name)):
                os.mkdir(os.path.join(output_folder, name))
        return [convert_dcm_to_jpg(os.path.join(input_folder, name), os.path.join(output_folder, name)) for name in os.listdir(input_folder)]

    try:
        ds = pydicom.dcmread(input_folder, force=True)
        print("filename: " + output_folder.replace('.dcm', '.jpg'))
        image_2d = ds.pixel_array.astype(float)
        ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
        image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0
        image_2d_scaled = np.uint8(image_2d_scaled)
        print(image_2d_scaled.shape)
        if len(image_2d_scaled.shape) > 2:
            image_2d_scaled = cv2.cvtColor(image_2d_scaled, cv2.COLOR_BGR2GRAY)
        equ = cv2.equalizeHist(image_2d_scaled)
        cv2.imwrite(output_folder.replace('.dcm', '.jpg'), equ)
    except:
        print("Corrupted image")


convert_dcm_to_jpg(in_path, out_path)

print()
print("Finished converting !!!")