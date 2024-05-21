import os, sys
from PIL import Image

from json import loads
from subprocess import check_call
from time import sleep
from concurrent.futures import ThreadPoolExecutor, wait


def ocrImage(fn,folderName,outputPath):
    out_name=f'output_{fn.split(".")[0]}.json'
    out_name= os.path.join(outputPath,out_name)
    if os.path.exists(out_name):
        print('[e]', out_name)
        return "OCR Exists"

    output=check_call(f'gcloud ml vision detect-text "{os.path.join(folderName, fn)}">"{out_name}"' , shell=True)

    file= loads(open(out_name, 'rb').read())
    resp=file.get("responses")[0].get("fullTextAnnotation").get("text")
    print(repr(resp))
    print("[o]", out_name)
    # sleep(2)
    return resp

def sliceImage(table_image_path,file_name,foldername, numSlices= 17):
    if '_row_' in file_name:
        return False
    if not file_name.endswith('.jpg'):
        print(f"[ERR] {file_name} is not an image")
        return False
    table_image = Image.open(table_image_path)
    num_rows = numSlices  # Update with the desired number of rows
    image_width, image_height = table_image.size
    row_height = image_height // num_rows

    row_offset=0

    for i in range(num_rows):
        row_image_name = f'{file_name.replace(".jpg", "").replace(".JPG","")}_row_{i+1}.jpg'  # Adjust the naming convention as needed
        output_row_path=os.path.join(foldername, row_image_name)
        if os.path.exists(output_row_path):
            print('[e]', output_row_path)
        else:
            y_start = i * row_height - row_offset
            y_end = y_start + row_height - row_offset

            row_image = table_image.crop((0, y_start, image_width, y_end))
            row_image.save(output_row_path)
            print("[s]", output_row_path)



baseFolder= os.path.join(os.getcwd(), sys.argv[1])
for root,folders,files in os.walk(baseFolder):
    for f in files:
        if f in ('LF.jpg', 'LM.jpg'):
            continue
        # elif not f[0].isdigit():
        #     continue
        filePath=os.path.join(root,f)
        fileFolder=root
        # print(filePath)
        # print(fileFolder)
        slicesPath= os.path.join(fileFolder, f.replace('.jpg', '').replace('.JPG', '') + '_slices' )
        outputPath= os.path.join(slicesPath, 'output')
        if not '_row_' in slicesPath:

            if not os.path.exists(slicesPath):
                os.mkdir(slicesPath)
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)
            try:
                sliceImage(filePath,f,slicesPath)
            except Exception as e:
                print("SLICE ERROR", str(e))
                continue
            future_paths=[]
            with ThreadPoolExecutor(max_workers=5) as executor:
                for row in os.listdir(slicesPath):
                    rowPath= os.path.join(slicesPath, row)
                    if os.path.isfile(rowPath):
                        f= executor.submit(ocrImage,row,slicesPath,outputPath)
                        future_paths.append(f)
            wait(future_paths)
        # break