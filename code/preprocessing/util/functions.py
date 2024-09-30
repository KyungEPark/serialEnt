import pandas as pd
import numpy as np
import docx
import string

def read_docx_as_text(filepath):
    docx_file = docx.Document(filepath)
    text = "\n".join([para.text for para in docx_file.paragraphs])
    return text


# Cleaning from https://www.kaggle.com/code/jdparsons/interactive-abstract-and-expert-finder
def clean_newlines(text):
    text = text.replace('-\n', '')
    text = text.replace('\n', ' ').replace('\r',' ')
    
    return text



def clean_chars(text):
    text = "".join(i for i in text if ord(i) < 128) # remove all non-ascii characters
    text = text.replace('\t', ' ') # convert a tab to space
    # fastest way to remove all punctuation (except ' . and !) and digits
    text = text.replace('[Image: see text]', '')
    text = text.translate(str.maketrans('', '', '"#$%&()*+,-/:;<=>@[\\]^_`{|}~' + string.digits))
    
    return text.strip()




