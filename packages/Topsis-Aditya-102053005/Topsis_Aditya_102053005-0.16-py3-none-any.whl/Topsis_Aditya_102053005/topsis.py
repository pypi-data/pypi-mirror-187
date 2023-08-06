import pandas as pd
import sys
import os
def main() :
    if len(sys.argv) != 5 : #for the proper usage
        print("ERROR : NUMBER OF PARAMETERS")
        print("USAGE : python <filename>.py inputfile.csv '1,1,1,1' '+,+,-,+' result.csv ")
        exit(1)
    elif not os.path.isfile(sys.argv[1]): #for file not found
        print(f"ERROR : {sys.argv[1]} Doesn't exist, Please check if you have entered the right file")
        exit(1)
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]: #for csv format
        print(f"ERROR : Please enter {sys.argv[1]} in csv format")
        exit(1)
    else :
        dataset = pd.read_csv(sys.argv[1])
        ncol = len(dataset.columns.values)

        if ncol < 3 :
            print("ERROR : Minimum Number of Columns should be 3")
            exit(1)
        for i in range(1,ncol) :
            pd.to_numeric(dataset.iloc[:,i],errors='coerce')
            #if there are missing values
            #dataset.iloc[:,i].fillna((dataset[:,i].values.mean()),inplace=True)
    try :
        weights = [int(i) for i in sys.argv[2].split(',')]
    except :
        print('ERROR : Weights array not input properly')
        exit(1)
    
    #checking impact array
    for i in sys.argv[3].split(',') :
        if i not in ['+','-'] :
            print('Error : Impacts can only be + or -')
            exit(1)
    impact = sys.argv[3].split(',')

    if ncol != len(weights) + 1 or ncol != len(impact) + 1 :
        print("ERROR : The lenghts of either weights or impact doesn't match with the dataset length")
        print('Length of dataset : ',ncol-1,'\n Length of weights :',len(weights),'\nLenght of imapcts :',len(impact))
        exit(1)
    if('.csv' != (os.path.splitext(sys.argv[4]))[1]) :
        print('ERROR : output file should be in csv form')
        exit(1)
    topsis = Topsis()
    topsis.topsis(dataset,weights,impact,ncol)
class Topsis :
    def __Normalize(self,dataset,nCol,weight) :
        for i in range(1,nCol) :
            temp = 0
            for j in range(len(dataset)) :
                temp = temp + dataset.iloc[j,i] ** 2 #sum of squares
            temp = temp ** 0.5
            for j in range(len(dataset)) :
                dataset.iat[j,i] = (dataset.iloc[j,i] / temp) * weight[i-1] #adjusting according to weights
        #print(dataset)
        return dataset
    
    def __ideal_best_worst(self,dataset,ncol,impact) :
        ideal_best_values = (dataset.max().values)[1:]
        ideal_worst_values = (dataset.min().values)[1:]
        #print(ncol,len(impact))
        for i in range(1,ncol) :
            if impact[i-1] == '-' :
                ideal_best_values[i-1],ideal_worst_values[i-1] = ideal_worst_values[i-1],ideal_best_values[i-1]
        return ideal_best_values, ideal_worst_values
    
    def topsis(self,dataset,weights,impact,ncol) :
        #ncol = len(dataset.axes[1])
        dataset = self.__Normalize(dataset,ncol,weights)
        p_sln , n_sln = self.__ideal_best_worst(dataset,ncol,impact)
        score = []
        pp = [] #positive distances
        nn = [] #negative distances
        for i in range(len(dataset)) :
            temp_p,temp_n = 0,0
            for j in range(1,ncol) :
                temp_p += (p_sln[j-1] - dataset.iloc[i,j])**2
                temp_n += (n_sln[j-1] - dataset.iloc[i,j])**2
            temp_p,temp_n = temp_p**0.5,temp_n**0.5
            score.append(temp_n/(temp_p+temp_n))
            nn.append(temp_n)
            pp.append(temp_p)
        
        # dataset['positive distance'] = pp
        # dataset['negative distance'] = nn 
        #print(score)
        dataset['Topsis Score'] = score 
        dataset['Rank'] = (dataset['Topsis Score'].rank(method = 'max',ascending = False))
        dataset = dataset.astype({"Rank" : int})
        dataset.to_csv(sys.argv[4],index = False)

        
    

if __name__ == '__main__' :
    main()
