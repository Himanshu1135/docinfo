import re,os
from .utilis import *

file_path = r'D:\Projects\docinfo\extractor\name_corpus.txt'
# Open the file
with open(file_path, 'r') as file:
    # Read the contents of the file
    corpus_text = file.read()

#----------------------- Aadhaar Card
def Aadhaar_no(text):
    exp = "\d{4}\s\d{4}\s\d{4}"
    x = re.findall(exp, text)
    if len(x) != 0:
        y = re.sub("\s","",x[0])
        return y    
    else:
        return None

def gender(text):
    exp = "MALE|FEMALE|Male|Female"
    x = re.findall(exp, text)

    if len(x) != 0:
        return x[0]    
    else:
        return None 
def dob(text):
    exp = "\d{2}/\d{2}/\d{4}|\d{2}/\d{2}/\d \d{3}|\d{2}-\d{2}-\d{4}"
    x = re.findall(exp, text)
    if len(x) != 0:
        y = re.sub("\s","",x[0])
        return y    
    else:
        res = get_year_of_birth(text,"Year of Birth")
        return res
        
def get_year_of_birth(text, target_word):
    pattern = r'\b' + re.escape(target_word) + r'\b'
    match = re.search(pattern, text)
    if match:
        index = match.end()
        words = text[index:].split()
        txt = words[0]+ " " + words[1]
        pattern_2 = "\d{4}"
        match_2 = re.search(pattern_2, txt)
        if match_2:
            return match_2[0]
    else:    
        return None

def get_Aadhaar_name(text):
    
    '''
    input : text 
    working : find person name before target word {pattern}
    return : list of names
    '''
    
    target_word = "Year of Birth|DOB|D0B|Mother"
    # pattern = r'\b' + re.escape(target_word) + r'\b'
    pattern = r'\b' + target_word + r'\b'
    match = re.search(pattern, text)

#----- first match target word to split text

    if match:
        index = match.end()
        words = text[:index].split()
        
        if words:
            ext_txt = ' '.join(words)

            # names = extract_names_nltk(ext_txt)  #----------------For name extraction from nltk------------#
            
#---------- using extract name corpus function
            names = extract_name_corpus(ext_txt,corpus_text)
            if names != None:
                return names
            else:
                return None
    else:
        names = extract_name_corpus(text,corpus_text)
        if names != None:
            return names 
        else:
                return None

def aadhaar_info_extractor(img_path):
    '''
    input : image path
    working : Extract information from image using ocr and regex
    return : List of information
    '''
    result = []
    
#-------- for filename extraction 
    filename_with_extension = os.path.basename(img_path)       
    filename = os.path.splitext(filename_with_extension)[0]

#-------- for text extraction using pytess OCR 
    text = pytess_text(img_path)                               

#-------- Cleaning Text 

    text = text.strip().replace('\n', ' ').replace('  ', ' ')  
    text = re.sub(r'[^A-Za-z0-9/\s-]', '', text)

#------- infomation extracction 

    name_arr = get_Aadhaar_name(text)                           
    Gender =gender(text)
    Aadhaar_No=Aadhaar_no(text)
    Date = dob(text)

#-------- joining name and cleaning 
    Name = ' '.join(name_arr)
    Name = re.sub(r'[^A-Za-z\s]', '', Name)

    result.append([filename,Name,Gender,Aadhaar_No,Date,text])

    return result
#------------------------- Pan Card
def pan_No(text):
    exp = "[\d|\w]\w{4}\d{4}\w"
    x = re.findall(exp, text)
    if len(x) != 0:
        y = re.sub("\s","",x[0])
        return y    
    else:
        return None

def pan_names_person(text):
    '''
    input : text 
    working : find person name before target word {pattern}
    return : list of names
    '''
    pattern = "Father|Father's"
    match = re.search(pattern, text)
#----- first match target word to split text for seprating name with father name
    if match:
        index = match.end()
        words = text[:index].split()
        if words:
            words = ' '.join(words)
            names = extract_name_corpus(words,corpus_text)
            return names
    else:
        names = extract_name_corpus(text,corpus_text)
#-------------- if names contain more then 3 element then search for surname
        if len(names) > 3:  
            duplicates = surname_duplicates(names)
            if duplicates != None:
                return names[:duplicates+1]
            else:
                return names[:2]
        else:
            return names
    
def pan_names_father(text):
    pattern = "Father|Father's"
    match = re.search(pattern, text)
    
    if match:
        index = match.end()
        words = text[index:].split()
        if words:
            words = ' '.join(words)
            names = extract_name_corpus(words,corpus_text)
            return names
    else:
        names = extract_name_corpus(text,corpus_text)

        if len(names) > 3:
            duplicates = surname_duplicates(names)
            if duplicates != None:
                return names[duplicates+1:]
            else:
                return names[2:]
        else:
            return []   

def pan_info_extractor(img_path):
    '''
    input : image path
    working : Extract information from image using ocr and regex
    return : List of information
    '''
    res = []
    #-------- for filename extraction 
    filename_with_extension = os.path.basename(img_path)
    filename = os.path.splitext(filename_with_extension)[0]

    text = pytess_text(img_path)
#------------- cleaning text using regular expressions
    text = text.strip().replace('\n', ' ').replace('  ', ' ')
    text = re.sub(r'[^A-Za-z0-9/\s]', '', text)
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

    res.append([filename,Name,Date,pan_no,f_Name,text])
    return res