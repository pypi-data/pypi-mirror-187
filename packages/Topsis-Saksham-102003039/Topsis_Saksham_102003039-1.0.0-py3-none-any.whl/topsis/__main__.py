import pandas as pd
import sys 

class Parameters(Exception):
  pass
class InsufficientColumns(Exception):
  pass
class InsufficientData(Exception):
  pass
class impacterror(Exception):
  pass
def main():
    try:
        if(len(sys.argv)!=5):
            raise Parameters
        #reading the input data
        df, df_org = pd.read_csv(sys.argv[1]), pd.read_csv(sys.argv[1])
        
        if df.shape[1]<3:
            raise InsufficientColumns

        #drop the first column
        df = df.drop(df.columns[[0]], axis=1)
        cols = len(df.axes[1])

        #handling non-numeric values
        for i in range(1, cols):
            pd.to_numeric(df.iloc[:, i], errors='coerce')
            df.iloc[:, i].fillna((df.iloc[:, i].mean()), inplace=True)

        #reading the weights and imapcts
        weights = [float(i) for i in sys.argv[2].split(',')]
        impact = sys.argv[3].split(',')

        for i in range(len(impact)):
            if not((impact[i]=="+") or (impact[i]=="-")):
                raise impacterror
        
        if (len(weights) != cols) or (len(impact) != cols):
            raise InsufficientData
        
        #computing weighted normalised data
        for i in range(0,cols):
            rss=0
            for j in range(len(df)):
                rss=rss+(df.iloc[j,i]**2)
            rss=rss**0.5
            for j in range(len(df)):
                df.iloc[j,i]=(df.iloc[j,i]/rss)*weights[i]

        #finding the ideal best and ideal worst feature values
        ideal_best=[]
        ideal_worst=[]
        for j in range(0, cols):
            if impact[j]=='-':
                ideal_best.append(df.iloc[:,j].min())
                ideal_worst.append(df.iloc[:,j].max())
            else:
                ideal_best.append(df.iloc[:,j].max())
                ideal_worst.append(df.iloc[:,j].min())

        #computing s+ and s-
        s_pos=[0]*len(df)
        s_neg=[0]*len(df)
        for i in range(len(df)):
            temp1=0
            temp2=0
            for j in range(0,cols):
                temp1=temp1+((df.iloc[i,j]-ideal_best[j])**2)
                temp2=temp2+((df.iloc[i,j]-ideal_worst[j])**2)
            s_pos[i]=temp1**0.5
            s_neg[i]=temp2**0.5

        #computing the performance score
        score=[0]*len(df)
        for i in range(len(df)):
            score[i]=s_neg[i]/(s_pos[i]+s_neg[i])

        #generating the final file
        df_org['Topsis Score'] = score
        df_org['Rank'] = (df_org['Topsis Score'].rank(method='max', ascending=False))
        df_org = df_org.astype({"Rank": int})
        df_org.to_csv(sys.argv[4], index=False)

    except FileNotFoundError:
        print("File Not Found")
    except Parameters:
        print("Format : python topsis.py inputfile.csv '1,1,1,1' '-,+,+,+' result.csv")
    except InsufficientColumns:
        print("Columns in the input file are less than 3")
    except InsufficientData:
        print("Input weight/impact is not sufficient")
    except ValueError:
        print("Weights are not separated by comma")
    except impacterror:
        print("Impact must be either +/- and must be separated by comma")
if __name__=="__main__":
  main() 