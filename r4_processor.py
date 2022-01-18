import pandas as pd
import glob


r4_l1=pd.read_csv("./raw/R4_L1.csv")
r4_l2=pd.read_csv("./raw/R4_L2.csv")


columns=["第2層","第3層","第4層","メモ"]
r4_l234 = pd.DataFrame(data=[],columns=columns)
tabs=r4_l1["タブ名"]
for tab in tabs:
    r4_l34_unit=pd.read_csv(f"./raw/R4_L3L4_{tab}.csv")
    r4_l234=pd.concat([r4_l234,r4_l34_unit.loc[:,columns]])

r4_l12=pd.merge(r4_l1,r4_l2,how="outer").iloc[:,[0,1,2,3,4]]
r4_full=pd.merge(r4_l12,r4_l234,how="outer")
r4_full.to_csv("./dist/r4_full.csv",encoding="utf_8_sig")
r4_no_disc=r4_full.loc[:,["第1層","第2層","第3層","第4層"]]
r4_no_disc.to_csv("./dist/r4_no_disc.csv",encoding="utf_8_sig")

def dataframe_to_text(data:pd.DataFrame):
    def col_to(data:pd.DataFrame,index:int):
        return list(data.columns.values[0:index])

    def accum_col(data:pd.DataFrame):
        col_1=data.columns.values[-1]
        col_2=data.columns.values[-2]
        data=pd.DataFrame({col_1:data.groupby(col_to(data,-1))[col_1].agg(lambda x:"\n".join(list(x)))}).reset_index()
        data[col_2]=data[col_2]+"\n"+data[col_1]
        return data.drop(col_1,axis=1)

    output = pd.concat([pd.DataFrame({"$index":data.index}),data],axis=1)
    for _ in range(1,len(output.columns)-1):
        output=accum_col(output)

    return '\n'.join(list(output.iloc[:,1]))

r4_full=r4_full.fillna("")
r4_to_md=pd.DataFrame(data=[],columns=["第1層","第2層","第3層","第4層"])
r4_to_md["第1層"]="\n"+"# "+r4_full["第1層"]+"\n\n"+r4_full["第1層説明"]+"\n"
r4_to_md["第2層"]="\n"+"## "+r4_full["第2層"]+"\n\n"+r4_full["第2層説明"]+"\n"
r4_to_md["第3層"]="\n"+"### "+r4_full["第3層"]+"\n"
r4_to_md["第4層"]="1. "+r4_full["第4層"]

r4_md_to_edit=pd.DataFrame(data=[],columns=["第1層","第2層","第3層","第4層"])
r4_md_to_edit["第1層"]="\n"+"# "+r4_full["第1層"]+"(第1層)\n\n"+r4_full["第1層説明"]+"\n"
r4_md_to_edit["第2層"]="\n"+"## "+r4_full["第2層"]+"(第2層)\n\n"+r4_full["第2層説明"]+"\n"
r4_md_to_edit["第3層"]="\n"+"### "+r4_full["第3層"]+"\n"
r4_md_to_edit["第4層"]="1. "+r4_full["第4層"]

r4_md_text=dataframe_to_text(r4_to_md)
with open("./dist/r4.md","w") as f:
    f.write(r4_md_text)

r4_md_text_to_edit=dataframe_to_text(r4_md_to_edit)
with open("./dist/r4_to_edit.md","w") as f:
    f.write(r4_md_text_to_edit)
