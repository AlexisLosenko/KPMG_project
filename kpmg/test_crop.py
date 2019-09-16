from wand.image import Image as WandImg
import os


###test code###
## need one directory /png with some png ... and a /png_crop directory
files = []

for r, d, f in os.walk("./png"):
    for file in f:
        if ".png" in file:
            files.append(os.path.join(r, file))
print(files)

for i in files:
    file_path = os.path.abspath(i)
    crop_path_template = file_path.replace("\\png", "\\png_crop").replace(".png", "")

    with WandImg(filename=file_path, resolution=300) as source:
        source.compression_quality = 99
        images = source
        nr_of_pages = len(images)
        image_paths = []

        if str(i)[-5] == "0":
            images.crop(int(images.size[0]*0.16), int(images.size[1]*0.20), int(images.size[0]*0.95), int(images.size[1]*0.92))
            print(images.size)
        else:
            images.crop(int(images.size[0]*0.16), int(images.size[1]*0.052), int(images.size[0]*0.95), int(images.size[1]*0.92))
        img_crop_path = crop_path_template + "_" +"croped.png"
        WandImg(images).save(filename=img__crop_path)