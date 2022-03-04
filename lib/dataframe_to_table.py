from textwrap import dedent
import pandas as pd


def group_rows(table:pd.DataFrame,splitter:str=":::"):
    """ group samerows in dataframe"""
    columns=list(table.columns.values)
    output_table=table.copy().fillna("")
    template_table=output_table.copy()
    for i in range(0,len(columns)-1):
        to_indexed = columns[0:i+1]
        indexed =template_table.groupby(to_indexed,as_index=False,sort=False)\
            .count()\
            .apply(lambda x:[x[i]+splitter+str(x[i+1]),*[None]*(x[i+1]-1)],axis=1)
        indexed = sum(indexed,[])
        output_table.iloc[:,i]=indexed
    return output_table

def make_html_table(table:pd.DataFrame,group:bool=False):
    """ make html table from dataframe """
    SPLITTER="::-:-::"
    def to_table_cell(x):
        if x==None:
            return ""
        elif SPLITTER in x:
            s=x.split(SPLITTER)
            return f'<td rowspan="{s[1]}">{s[0]}</td>'
        else:
            return f"<td>{x}</td>"

    output_table= group_rows(table,SPLITTER) if group else table.copy().fillna("")
    columns=list(table.columns.values)

    output_table=output_table.applymap(to_table_cell)

    theader=f"<thead><tr><th>{'</th><th>'.join(columns)}</th></thead></tr>"
    tbody="<tbody>\n"
    for items in output_table.fillna("").itertuples():
        row=f"<tr>{''.join(items[1:])}</tr>\n"
        tbody += row
    tbody+="</tbody>\n"
    table_html=f"<table border=1>{theader}\n{tbody}</table>"
    return table_html

def repeat(char:str,count:int):
    """ repeat same char for count time """
    return "".join([char for x in range(count)])

def make_latex_table(table:pd.DataFrame,
    label:str="",
    layout:str="",
    caption:str="",
    group:bool=False):
    """ make latex table from dataframe """
    SPLITTER="::-:-::"
    def to_table_cell(x):
        if x==None:
            return ""
        elif SPLITTER in x:
            s=x.split(SPLITTER)
            return s[0]
        else:
            return x

    columns=list(table.columns.values)
    layout = layout if layout!="" else repeat("X",len(columns))
    output_table= group_rows(table,SPLITTER) if group else table.copy().fillna("")

    output_table=output_table.applymap(to_table_cell)

    theader=r"""
        \begin{xltabular}{\linewidth}{%s}
        \caption{\label{tbl:%s}%s} \\
        \toprule
    """ % (layout,label,caption)
    theader=dedent(theader)
    theader+=' & '.join(columns)+r" \\"
    tbody="\\midrule\n\\endhead\n"
    for items in output_table.itertuples():
        row=' & '.join(items[1:])+r" \\"+"\n"
        tbody += row
    tbody+=r"\bottomrule"
    table_latex=f"{theader}\n{tbody}"+dedent(r"""
        \end{xltabular}
    """)
    return table_latex

