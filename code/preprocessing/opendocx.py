from util.functions import read_docx_as_text
import os
import pandas as pd

def main():    
    path = r"C:\Users\cryst\Desktop\personal_projects\post_mortem\data\rawdata\postmortems"
    ppldata = pd.read_pickle(r"C:\Users\cryst\Desktop\personal_projects\post_mortem\data\processed\master_df.pkl")
    for file in os.listdir(path):
        if file.endswith(".docx"):
            text = read_docx_as_text(os.path.join(path, file))
            ppldata.loc[ppldata['Filename'] == file, "text"] = text
    ppldata.to_pickle(r"C:\Users\cryst\Desktop\personal_projects\post_mortem\data\processed\postmortem_df.pkl")
    

if __name__ == "__main__":
    main()
