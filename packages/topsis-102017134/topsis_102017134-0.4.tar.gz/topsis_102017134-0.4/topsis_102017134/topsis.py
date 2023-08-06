import sys
import pandas as pd

def main():
    if len(sys.argv) != 5:
        print("Invalid input. Use the following format- fileName InputDataFile weights impacts resultFileName")
        exit()

    inpFile = sys.argv[1]
    weight = sys.argv[2]
    impact = sys.argv[3]
    outFile = sys.argv[4]

    try:
        df = pd.read_csv(inpFile)
    except FileNotFoundError:
        print("Enter a valid file")
        exit()

    df1 = df.copy()

    if len(df.columns) < 3:
        print("Not sufficient number of columns")
        exit()

    for column in df.columns[1:]:
        if df[column].dtype.kind not in 'iufb':
            print("Non numerical value found")
            exit()

    imp = impact.split(sep=',')
    tw = weight.split(sep=',')

    if len(imp) != len(df.columns)-1 or len(tw) != len(df.columns)-1:
        print("Invalid number of weights or impacts")
        exit()
    for i in imp:
        if i != "+" and i != "-":
            print("Invalid impact")
            exit()
    w = []
    for i in tw:
        try:
            w.append(float(i))
        except:
            print("Invalid weight")
            exit()

    for column in df.columns[1:]:
        df[column] = df[column]/(sum(df[column]**2)**0.5)

    for i in range(len(w)):
        df.iloc[:, i+1] = df.iloc[:, i+1]*w[i]

    vp = []
    vm = []

    for i in range(len(imp)):
        if imp[i] == '+':
            vp.append(max(df.iloc[:, i+1]))
            vm.append(min(df.iloc[:, i+1]))
        else:
            vp.append(min(df.iloc[:, i+1]))
            vm.append(max(df.iloc[:, i+1]))

    sp = []
    sm = []

    for i in range(len(df)):
        sp.append((sum((df.iloc[i, 1:]-vp)**2))**0.5)
        sm.append((sum((df.iloc[i, 1:]-vm)**2))**0.5)

    p = []

    for i in range(len(sp)):
        p.append(sm[i]/(sp[i]+sm[i]))

    df['Score'] = p

    df1['Topsis Score'] = p
    df1['Rank'] = df['Score'].rank(ascending=False)
    print(df1)
    df1.to_csv(outFile, index=False)

if __name__ == "__main__":
    main()
    