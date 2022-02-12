import pandas as pd

def dataframe_to_text(data:pd.DataFrame):
    def col_to(data:pd.DataFrame,index:int):
        return list(data.columns.values[0:index])

    def accum_col(data:pd.DataFrame):
        col_1=data.columns.values[-1]
        col_2=data.columns.values[-2]
        data=data\
            .groupby(col_to(data,-1), as_index=False,sort=False)\
            .agg(lambda x:"\n".join(list(x)))
        data[col_2]=data[col_2]+"\n"+data[col_1]
        return data.drop(col_1,axis=1)

    for _ in range(1,len(data.columns)):
        data=accum_col(data)

    return '\n'.join(list(data.iloc[:,0]))
