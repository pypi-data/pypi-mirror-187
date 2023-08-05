import pandas as pd
import sys
import os
import csv
import math

def euclidian_dist(row, ideal_best,ncol):
    dist = 0
    for i in range(ncol):
        dist = dist+(row[i]-ideal_best[i])**2
    return math.sqrt(dist)


def main():
    # If number of arguments are not correct
    if (len(sys.argv) != 5):
        print("Incorrect number of arguments")
        print("Give input as: topsis <InputDataFile.csv> <Weights> <Impacts> <Result.csv")

    # Error message for wrong inputs
    # This function specifies whether the path is existing file or not.
    elif not os.path.isfile(sys.argv[1]):
        print(f"{sys.argv[1]} does not exist")

    # os.path.splitext() method in Python is used to split the path name into a pair root and extension. [0]->path,[1]->extension
    elif (".csv" != (os.path.splitext(sys.argv[1]))[1]):
        print(f"{sys.argv[1]} is not a csv file")

    else:
        data = pd.read_csv(sys.argv[1])
        nrow = data.shape[0]
        #If number of columns less than 3
        if (data.shape[1] < 3):
            print("Input file has less than 3 columns")
            exit(1)
        else:
            final = data.iloc[:, 1:]
            ncol = final.shape[1]
            for i in final.columns:#col
                sum = 0
                for j in range(nrow): 
                    sum = sum+final.loc[j, i]**2
                final[i] = round(final[i]/math.sqrt(sum), 4)
            w1 = sys.argv[2]
            w = []
            for i in w1.split(','):
                w.append(int(i))
            j = 0
            for i in final.columns:
                final[i] = round(final[i]*w[j], 4)
                j += 1
            impact_st = sys.argv[3]
            impact = []
            for i in impact_st.split(','):
                impact.append(i)
            #check for number of weights and number of impacts
            if(len(w)!=len(impact)):
                print("Number of weights and impacts are not same")
                exit(1)
            ideal_best = []
            ideal_worst = []
            dist_ideal_best=[]
            dist_ideal_worst=[]
            j = 0
            for i in final.columns:
                if (impact[j] == "+"):
                    ideal_best.append(final[i].max())
                    ideal_worst.append(final[i].min())
                else:
                    ideal_best.append(final[i].min())
                    ideal_worst.append(final[i].max())
                j+=1
            j = 0
            for i in range(final.shape[0]):
                dist_from_ideal_best = euclidian_dist(final.iloc[i,:], ideal_best,ncol)
                dist_from_ideal_worst = euclidian_dist(final.iloc[i,:], ideal_worst,ncol)
                dist_ideal_best.append(dist_from_ideal_best)
                dist_ideal_worst.append(dist_from_ideal_worst)
            final['S+'] = dist_ideal_best
            final['S-'] = dist_ideal_worst
            performance_score = []
            for i in range(nrow):
                p_score = (dist_ideal_worst[i])/(dist_ideal_best[i]+dist_ideal_worst[i])
                performance_score.append(round(p_score, 4))
            data['Topsis score'] = performance_score
            data['Rank'] = (data['Topsis score'].rank(method='max', ascending=False))
            data = data.astype({'Rank': int})
            #Now we will write data to csv file.
            data.to_csv(sys.argv[4], index=False)
            # print(data)

if __name__=="__main__":
    main()