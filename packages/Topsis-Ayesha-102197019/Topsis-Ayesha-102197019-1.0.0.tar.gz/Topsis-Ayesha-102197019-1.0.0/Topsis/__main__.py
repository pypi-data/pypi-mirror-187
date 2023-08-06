def main():
    import sys
    import pandas as pd
    import os
    import copy
    import numpy as np
    def topsis():
        k=0
        if(len(sys.argv)==5):
            input_file=sys.argv[1]
            weight=sys.argv[2]
            impact=sys.argv[3]
            result_file=sys.argv[4]
            data=pd.read_csv(input_file)
            #print(data.head())

            #Checking existence of file
            if(os.path.exists(input_file)):
                data=pd.read_csv(input_file)
                #print(data)
            else:
                print('Improper inputs:Input data file doesnt exist')
                return
            #Checking No of columns
            if(data.shape[1]<3):
                print('No of columns less than 3')
                return
            #Checking numeric values
            for i in range(1,data.shape[1]):
                if(not(np.issubdtype(data.iloc[:,1].values.dtype, np.number))):
                    print('Please ensure all input values from 2nd to last column are numeric')
                    return
            #Splitting and converting weights and impact
            weight=[float(x) for x in weight.split(',')]
            impact=impact.split(',')
            #Checking impact values
            for i in impact:
                if(i!='+' and i!='-'):
                    print('Improper inputs: Check impact values')
                    return
                    
            #Checking number of specified weights impact and columns
            if(len(weight)!=len(impact) or len(impact)!=(data.shape[1]-1)):
                print('Improper inputs: Check usage')
                return
            
            #Find root of sum of squares for each column
            rs=[]
            for i in range(1,data.shape[1]):
                arr=data.iloc[:,i]
                arr=arr**2
                #print((arr))
                #print(sum(arr)**(0.5))
                k=sum(arr)**(0.5)
                rs.append(k)
            #Normalising data
            
            norm=copy.deepcopy(data)
            for i in range(1,data.shape[1]):
                norm.iloc[:,i]=norm.iloc[:,i]/rs[i-1]
        
            for i in range(1,data.shape[1]):
                norm.iloc[:,i]=norm.iloc[:,i]*weight[i-1]
            
            #Ideal best and Ideal worst calculation
            best=[]
            worst=[]
            for i in range(1,data.shape[1]):
                if(impact[i-1]=='-'):
                    #print(impact[i-1])
                    best.append(min(norm.iloc[:,i]))
                    worst.append(max(norm.iloc[:,i]))
                elif(impact[i-1]=='+'):
                    #print(impact[i-1])
                    best.append(max(norm.iloc[:,i]))
                    worst.append(min(norm.iloc[:,i]))
            
            #Euclidean distance calculations
            sb=[]
            sw=[]
            for j in range(0,data.shape[0]):
                #print(norm.iloc[j,:])
                #print(norm.iloc[j,1:]-best)
                dvec=norm.iloc[j,1:]-best
                dvec=dvec**2
                dvecs=sum(dvec)
                dvecs=dvecs**0.5
                #print(dvecs)
                sb.append(dvecs)
                
                dvec=norm.iloc[j,1:]-worst
                dvec=dvec**2
                dvecs=sum(dvec)
                dvecs=dvecs**0.5
                #print(dvecs)
                sw.append(dvecs)
                
            #print(sb)
            #print(sw)
            
            #Performace score calculation
            perf_score=[]
            for j in range(0,data.shape[0]):
                #print(sw[j]/(sw[j]+sb[j]))
                perf_score.append(sw[j]/(sw[j]+sb[j]))
            #print(perf_score)
            norm.loc[:,'Topsis Score']=perf_score
            data.loc[:,'Topsis Score']=perf_score
            #Ranking Calculation
            s = np.array(perf_score)
            sort_index = np.argsort(s)
            rank=[0]*(data.shape[0])
            #print(sort_index+1)
            for i in range(0,data.shape[0]):
                rank[sort_index[i]]=data.shape[0]-i
            #print(rank)
            norm.loc[:,'Ranks']=rank
            data.loc[:,'Ranks']=rank
            #print("hey")
            #print(data)
            
            #Putting data in result file
            data.to_csv(result_file)
            
            #df=pd.read_csv(result_file)
            #print(df)
            
                    
        else:
            print('Improper inputs: Check usage')
            return


            


            
            
    topsis()

if __name__=='__main__':
    main()
