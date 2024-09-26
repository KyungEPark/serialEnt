import pandas as pd
import numpy as np
import docx

def read_docx_as_text(filepath):
    docx_file = docx.Document(filepath)
    text = "\n".join([para.text for para in docx_file.paragraphs])
    return text








