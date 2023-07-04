import os
# import time
import re,csv
# import glob
import json
from .Entity import RESULT_PATH
from .utilis import *
from .DocsInteractor import *

def info_Extractor(option,img_path):
    print(option)
    '''
    input1 : Option{0,1} 0 = Aadhaar card , 1 = Pan Card docs
    input2 : image path
    input3 : result path where to save result directory
    working : Extract information from image using ocr and regex
    return : List of information
    '''    
    print("Starting : info_Extractor")
#-------- for filename extraction 
    filename_with_extension = os.path.basename(img_path)       
    filename = os.path.splitext(filename_with_extension)[0]

#-------- for text extraction using pytess OCR 
    text = pytess_text(img_path)                               
#-------- Cleaning Text 
    text = text.strip().replace('\n', ' ').replace('  ', ' ')  
    text = re.sub(r'[^A-Za-z0-9/\s]', '', text)

    if option == 'aadhar':
#-------------- Aadhaar Card

    #------- infomation extracction 
        name_arr = get_Aadhaar_name(text)                           
        Gender =gender(text)
        Aadhaar_No=Aadhaar_no(text)
        Date = dob(text)

    #-------- joining name and cleaning 
        Name = ' '.join(name_arr)
        Name = re.sub(r'[^A-Za-z\s]', '', Name)

        # result.append([filename,Name,Gender,Aadhaar_No,Date,text])

    # ----------- Storing data in json format
        data = {
        "Name": Name,
        "Gender": Gender,
        "Aadhaar_No": Aadhaar_No,
        "Date_of_Birth": Date,
        # "Text":text
    }
        if not os.path.exists(RESULT_PATH):
                os.makedirs(RESULT_PATH)
        try:
            with open(RESULT_PATH, 'w') as file:
                json.dump(data, file)
                print("JSON data written successfully.")
        except IOError as e:
            print("Error writing JSON data:", str(e))
        return data

    elif option == 'pan':
#--------------- Pan Card 

    #-------- Extracting info
        name = pan_names_person(text)
        f_name = pan_names_father(text)
        pan_no = pan_No(text)
        Date = dob(text)
    #----- Clean names info 
        Name = ' '.join(name)
        Name = re.sub(r'[^A-Za-z\s]', '', Name)
        f_Name = ' '.join(f_name)
        f_Name = re.sub(r'[^A-Za-z\s]', '', f_Name)
# ----------- Storing data in json format
        data = {
        "Name": Name,
        "Father_Name": f_Name,
        "Date_of_Birth": Date,
        "Pan_No": pan_no,
        # "Text":text

    }
        if not os.path.exists(RESULT_PATH):
            os.makedirs(RESULT_PATH)
        try:
            with open(RESULT_PATH, 'w') as file:
                json.dump(data, file)
                print("JSON data written successfully.")
        except IOError as e:
            print("Error writing JSON data:", str(e))
        return data

    else:
        return {}

# def aadhaar_Csv(folder_path,result_path):

#     '''
#     input1 : folder path as string
#     input2 : final result path as string
#     working : Create a csv for many input image 
#     return : csv file
#     '''  
#     print("Starting : aadhaar_Csv")
#     #------------ Use glob to get a list of all image file paths in the folder
#     image_files = []
#     for ext in Entity.IMAGE_EXTENTIONS:
#         image_files.extend(glob.glob(folder_path + '/' + ext))

#     #-------- for collecting all info in data 
#     data = []
#     data.append(['FileName','Name','Gender','Aadhaar_No','DOB','Text'])

#     # --------- for time taken 
#     t1 = time.time()

#     # --------- extracting info for each img and adding to data array
#     for img_path in image_files:
#         res = aadhaar_info_extractor(img_path)
#         data.append([res[0][0],res[0][1],res[0][2],res[0][3],res[0][4],res[0][5]])

#     # -------------- Open the file in write mode with newline=''

#     with open(result_path, 'w', newline='') as file:
#         writer = csv.writer(file)
#         # Write the data rows
#         for row in data:
#             writer.writerow(row)
#     print('written successfully.')

#     t2 = time.time()   
#     print("Time taken :",t2-t1)

# def pan_Csv(folder_path,result_path):

#     '''
#     input1 : folder path as string
#     input2 : final result path as string
#     working : Create a csv for many input image 
#     return : csv file
#     '''  
#     print("Starting : pan_Csv")
#     image_files = []
#     for ext in Entity.IMAGE_EXTENTIONS:
#         image_files.extend(glob.glob(folder_path + '/' + ext))

#     # --------- extracting info for each img and adding to data array

#     data = []
#     data.append(['FileName','Name','DOB','Pan_No','father_Name','Text'])
#     t1 = time.time()
#     for img_path in image_files:
#         res = pan_info_extractor(img_path)
#         data.append([res[0][0],res[0][1],res[0][2],res[0][3],res[0][4],res[0][5]])

#     # ------------Open the file in write mode with newline=''
#     with open(result_path, 'w', newline='') as file:
#         writer = csv.writer(file)
#         # Write the data rows
#         for row in data:
#             writer.writerow(row)

#     print(' written successfully.')
#     t2 = time.time()   
#     print("Time taken :",t2-t1)

