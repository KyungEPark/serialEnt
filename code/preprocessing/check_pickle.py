import pandas as pd

def main():
    ppldata = pd.read_pickle(r"C:\Users\cryst\Desktop\personal_projects\post_mortem\data\processed\postmortem_df.pkl")
    print(ppldata.head())

if __name__ == "__main__":
    main()
