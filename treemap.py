import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from math import log, e
import os

def recursiveCount(df, className):
    classIndex = df.index[df['subClass'] == className].to_list().pop()
    summNodes = 0 + df.loc[classIndex]['CountNodes']
    subClassIndexes = df.index[df['Class'] == className].to_list()
    if len(subClassIndexes) != 0:
        for subClassIndex in subClassIndexes:
            summNodes = summNodes + recursiveCount(df, df.loc[subClassIndex]['subClass'])

    df.loc[classIndex, 'CountSubClassNodes'] = summNodes

    return summNodes

def applyCoef(df):
    def new_log(number, base=e):
        if number == 0:
            return number
        else:
            return log(number, base)

    df['CountSubClassNodesWithCoef'] = df['CountNodes'].apply(lambda x: new_log(x))

def createTreemap(alignmentAlgorithmOutputFilename):
    df = pd.read_csv('data/subClasses.csv')
    countMultiKE = pd.read_csv('data/count_' + alignmentAlgorithmOutputFilename + '.csv')

    result = pd.merge(df, countMultiKE, on='subClass', how='left')
    result['CountNodes'] = result['CountNodes'].replace(np.NaN, 0)

    classList = result['Class'].to_list()
    noParentClasses = set()
    for Class in classList:
        if (result['subClass'].isin([Class]).any() == False):
            noParentClasses.add(Class)

    for Class in noParentClasses:
        result.loc[ len(result.index )] = [Class, "", 0]

    result['CountSubClassNodes'] = result['CountNodes']

    applyCoef(result)
    recursiveCount(result, 'owl#Thing')

    fig = go.Figure(go.Treemap(
        labels=result['subClass'].to_list(),
        parents=result['Class'].to_list(),
        values=result['CountSubClassNodesWithCoef'].to_list(),
        text=("Recursive count: " + result['CountSubClassNodes'].astype(str) + ",\n Count: " + result['CountNodes'].astype(str)).to_list(),
        branchvalues = "remainder",
        root_color="lightgrey",
        marker_colorscale = 'YlOrRd',
        textinfo ="label+percent root",
        hoverinfo="text+label+value+percent parent",
        sort=True
    ))
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

    figure = fig.to_html()
    
    saveFolder = 'results/' + alignmentAlgorithmOutputFilename
    if os.path.isdir(saveFolder) == False:
        os.mkdir(saveFolder)
    with open(saveFolder + '/treemap_' + alignmentAlgorithmOutputFilename + '.html', 'w') as bruh:
        for line in figure:
            bruh.write(line)

if __name__ == '__main__':
    createTreemap('MultiKE_EN_RU_15K_V1')
