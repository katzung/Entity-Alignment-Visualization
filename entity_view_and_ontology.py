import altair as alt
import pandas as pd

alt.data_transformers.enable("vegafusion")

def create_chart(alignmentAlgorithmOutputFilename):
    ########################################### Data
    alignmentData1 = pd.read_csv('data/' + alignmentAlgorithmOutputFilename + '.csv')

    alignmentData2 = pd.read_csv('data/' + alignmentAlgorithmOutputFilename + '.csv')
    alignmentData2.rename(columns = {'Ent1_ID':'temp'}, inplace = True)
    alignmentData2.rename(columns = {'Ent2_ID':'Ent1_ID'}, inplace = True)
    alignmentData2.rename(columns = {'temp':'Ent2_ID'}, inplace = True)

    onthologyNodesData = pd.read_csv('data/onthology_vertexes.csv')

    onthologyEdgesData = pd.read_csv('data/onthology_edges.csv')
    ###########################################

    xscale = alt.Scale(domain=[-100, 100])
    yscale = alt.Scale(domain=[-100, 100])
    selector = alt.selection_point(fields=['Type'])

    ########################################### First chart
    alignmentNodes1 = alt.Chart(alignmentData1, title='Alignment Results').properties(width=700, height=700).interactive(    
    ).add_params(selector).mark_circle(size=75).encode(
        x=alt.X('X:Q'),
        y=alt.Y('Y:Q'),
        tooltip=['Ent1_ID', 'X:Q', 'Y:Q', 'Ent1:O', 'Ent2:O', 'Language:N', 'Type:N'],
        color=alt.condition(selector, 'Type', alt.value('lightgray')),
        opacity=alt.condition(selector, alt.value(1.0), alt.value(0.3)),
        order=alt.condition(selector, alt.value(1), alt.value(0))
    )

    alignmentNodes2 = alt.Chart(alignmentData2).properties(width=700, height=700).interactive(    
    ).mark_circle(size=75).encode(
        x=alt.X('X:Q'),
        y=alt.Y('Y:Q'),
        tooltip=['Ent1_ID', 'X:Q', 'Y:Q', 'Ent1:O', 'Ent2:O', 'Language:N', 'Type:N'],
        color=alt.condition(selector, 'Type', alt.value('lightgray')),
        opacity=alt.condition(selector, alt.value(1.0), alt.value(0.0)),
        order=alt.condition(selector, alt.value(1), alt.value(0))
    )

    alignmentLookupData = alt.LookupData(alignmentData1, key="Ent1_ID", fields=["X", "Y"])

    alignmentEdges = alt.Chart(alignmentData1).mark_rule(strokeWidth=0.2).encode(
        x = alt.X('X:Q', scale=xscale),
        y = alt.Y('Y:Q', scale=yscale),
        x2 = alt.X2('X2:Q'),
        y2 = alt.Y2('Y2:Q'),
        opacity=alt.condition(selector, alt.value(1.0), alt.value(0.0)),
        color=alt.value('black'),
        order=alt.condition(selector, alt.value(1), alt.value(0))
    ).transform_lookup(
        lookup='Ent2_ID',
        from_=alignmentLookupData,
        as_=['X2', 'Y2']
    )
    ###########################################


    ########################################### Bar chart
    alignmentTypesBar = alt.Chart(alignmentData1).add_params(selector).mark_bar().encode(
        alt.Y('count()'),
        alt.X('Type:N').sort('-y'),
        color=alt.condition(selector, 'Type', alt.value('lightgray'))
    )
    ###########################################
    
    ########################################### Ontology chart

    countData = pd.read_csv('data/count_' + alignmentAlgorithmOutputFilename + '.csv')
    countData.rename(columns = {'subClass':'Type'}, inplace = True)
    countLookup = alt.LookupData(countData, key="Type", fields=["CountNodes"])

    onthologyNodes1 = alt.Chart(onthologyNodesData, title='Ontology Visualisation').mark_circle().add_params(selector).properties(width=700, height=700).interactive(
    ).encode(
        alt.X('X:Q'),
        alt.Y('Y:Q'),
        color=alt.condition(selector, alt.Color('Type:N'), alt.value('lightgray')),
        size=alt.Size('CountNodes:Q', scale=alt.Scale(range=[5, 5000])),
        opacity=alt.value(1.0),
        tooltip=['Type', 'Degree', 'CountNodes:Q']
    ).transform_lookup(
        lookup='Type',
        from_=alt.LookupData(alignmentData1, key="Type", fields=["Type"])
    ).transform_lookup(
        lookup='Type',
        from_=countLookup
    )

    fontSize_slider = alt.binding_range(min=2, max=13, step=1)
    fontSize_var = alt.param(bind=fontSize_slider, value=2, name="fontSize")
    onthologyNodesTextLabels = alt.Chart(onthologyNodesData).mark_text(fontSize=3).properties(width=700, height=700).encode(
        alt.X('X:Q'),
        alt.Y('Y:Q'),
        text='Type',
        size=fontSize_var
    ).add_params(fontSize_var)

    xscale2 = alt.Scale(domain=[-600, 400])
    yscale2 = alt.Scale(domain=[-500, 500])

    onthologyLookupData = alt.LookupData(onthologyNodesData, key="Type", fields=["X", "Y"])

    onthologyEdges = alt.Chart(onthologyEdgesData
    ).mark_rule(strokeWidth=0.75
    ).encode(
        x = alt.X('X:Q', scale=xscale2),
        y = alt.Y('Y:Q', scale=yscale2),
        x2 = alt.X2('X2:Q'),
        y2 = alt.Y2('Y2:Q'),
        opacity=alt.condition(selector, alt.value(1.0), alt.value(0.3))
    ).transform_lookup(
        lookup='Source',
        from_=onthologyLookupData
    ).transform_lookup(
        lookup='Target',
        from_=onthologyLookupData,
        as_=['X2', 'Y2']
    ).transform_lookup(
        lookup='Source',
        from_=alt.LookupData(alignmentData1, key="Type", fields=["Type"])
    )
    ###########################################

    ########################################### Entity View

    ###########################################

    chart = (((alignmentNodes1 + alignmentEdges + alignmentNodes2) | (onthologyEdges + onthologyNodes1 + onthologyNodesTextLabels))) & alignmentTypesBar

    return chart

def createEntity_chart(alignmentAlgorithmOutputFilename):
    entityIDs = pd.read_csv('data/' + alignmentAlgorithmOutputFilename + '.csv')

    entityIDs2 = pd.read_csv('data/' + alignmentAlgorithmOutputFilename + '.csv')
    entityIDs2.rename(columns = {'Ent1_ID':'temp'}, inplace = True)
    entityIDs2.rename(columns = {'Ent2_ID':'Ent1_ID'}, inplace = True)
    entityIDs2.rename(columns = {'temp':'Ent2_ID'}, inplace = True)

    relTriplesEnRu = pd.read_csv('data/rel_triples_en_ru.csv', sep='\t', header=None, names=['Ent1_ID', 'Relation', 'Ent2_ID'])

    entities = entityIDs['Ent1_ID'].to_list()
    names = (entityIDs['Ent1_ID'].astype(str) + ": " + entityIDs['Ent1'].astype(str)).to_list()
    entityDropdown = alt.binding_select(options=entities, labels=names, name="Entity")
    entitySelection = alt.selection_point(fields=['Ent1_ID'], bind=entityDropdown, empty=False)

    ent1Chart = alt.Chart(entityIDs, width=500, height=500, title='Entity View').mark_circle(size=650).interactive().encode(
        x=alt.X('X'),
        y=alt.Y('Y'),
        color='Type',
        opacity=alt.condition(entitySelection, alt.value(1.0), alt.value(0.0)),
        tooltip=['Ent1_ID', 'X', 'Y', 'Ent1', 'Language', 'Type']
    ).add_params(entitySelection).transform_filter(entitySelection)

    ent1RelatedEntitiesChart = alt.Chart(relTriplesEnRu, width=500, height=500).mark_circle(size=100).interactive().encode(
        x=alt.X('X:Q'),
        y=alt.Y('Y:Q'),
        opacity=alt.condition(entitySelection, alt.value(1.0), alt.value(0.0)),
        color='Type:N',
        tooltip=['Ent2_ID', 'X:Q', 'Y:Q', 'Language:N', 'Type:N']
    ).transform_lookup(
        lookup='Ent1_ID',
        from_=alt.LookupData(entityIDs, key="Ent1Full", fields=['Ent1_ID'])
    ).transform_lookup(
        lookup='Ent2_ID',
        from_=alt.LookupData(entityIDs, key="Ent1Full", fields=['X', 'Y', 'Language', 'Type'])
    ).transform_filter(entitySelection)

    ent1EdgesToRelatedEntitiesChart = alt.Chart(relTriplesEnRu, width=500, height=500).mark_rule(strokeWidth=0.75).interactive().encode(
        x=alt.X('X:Q'),
        y=alt.Y('Y:Q'),
        x2=alt.X2('X2:Q'),
        y2=alt.Y2('Y2:Q'),
        opacity=alt.condition(entitySelection, alt.value(1.0), alt.value(0.0))
    ).transform_lookup(
        lookup='Ent1_ID',
        from_=alt.LookupData(entityIDs, key="Ent1Full", fields=['X', 'Y'])
    ).transform_lookup(
        lookup='Ent2_ID',
        from_=alt.LookupData(entityIDs, key="Ent1Full", fields=['X', 'Y']),
        as_=['X2', 'Y2']
    ).transform_lookup(
        lookup='Ent1_ID',
        from_=alt.LookupData(entityIDs, key="Ent1Full", fields=['Ent1_ID'])
    ).transform_filter(entitySelection)

    ent2Chart = alt.Chart(entityIDs2, width=500, height=500).mark_circle(size=650).interactive().encode(
        x=alt.X('X:Q'),
        y=alt.Y('Y:Q'),
        color='Type',
        opacity=alt.condition(entitySelection, alt.value(1.0), alt.value(0.0)),
        tooltip=['Ent1_ID', 'X', 'Y', 'Ent1', 'Language', 'Type']
    ).transform_filter(entitySelection)

    ent2RelatedEntitiesChart = alt.Chart(relTriplesEnRu, width=500, height=500).mark_circle(size=100).interactive().encode(
        x=alt.X('X:Q'),
        y=alt.Y('Y:Q'),
        opacity=alt.condition(entitySelection, alt.value(1.0), alt.value(0.0)),
        color='Type:N',
        tooltip=['Ent2_ID', 'X:Q', 'Y:Q', 'Language:N', 'Type:N']
    ).transform_lookup(
        lookup='Ent1_ID',
        from_=alt.LookupData(entityIDs2, key="Ent1Full", fields=['Ent1_ID'])
    ).transform_lookup(
        lookup='Ent2_ID',
        from_=alt.LookupData(entityIDs, key="Ent1Full", fields=['X', 'Y', 'Language', 'Type'])
    ).transform_filter(entitySelection)

    ent2EdgesToRelatedEntitiesChart = alt.Chart(relTriplesEnRu, width=500, height=500).mark_rule(strokeWidth=0.75).interactive().encode(
        x=alt.X('X:Q'),
        y=alt.Y('Y:Q'),
        x2=alt.X2('X2:Q'),
        y2=alt.Y2('Y2:Q'),
        opacity=alt.condition(entitySelection, alt.value(1.0), alt.value(0.0))
    ).transform_lookup(
        lookup='Ent1_ID',
        from_=alt.LookupData(entityIDs2, key="Ent1Full", fields=['X', 'Y'])
    ).transform_lookup(
        lookup='Ent2_ID',
        from_=alt.LookupData(entityIDs2, key="Ent1Full", fields=['X', 'Y']),
        as_=['X2', 'Y2']
    ).transform_lookup(
        lookup='Ent1_ID',
        from_=alt.LookupData(entityIDs2, key="Ent1Full", fields=['Ent1_ID'])
    ).transform_filter(entitySelection)

    relationsBetweenAlignedEntitiesChart = alt.Chart(entityIDs, width=500, height=500).mark_rule(strokeWidth=0.9).interactive().encode(
        x=alt.X('X:Q'),
        y=alt.Y('Y:Q'),
        x2=alt.X2('X2:Q'),
        y2=alt.Y2('Y2:Q'),
        opacity=alt.condition(entitySelection, alt.value(1.0), alt.value(0.0)),
        color=alt.value('red')
    ).transform_lookup(
        lookup='Ent2_ID',
        from_=alt.LookupData(entityIDs, key="Ent1_ID", fields=['X', 'Y']),
        as_=['X2', 'Y2']
    ).transform_filter(entitySelection)

    chart = (ent1EdgesToRelatedEntitiesChart + ent2EdgesToRelatedEntitiesChart + relationsBetweenAlignedEntitiesChart + ent2Chart + ent1Chart + ent1RelatedEntitiesChart + ent2RelatedEntitiesChart)
    chart.encode(
        order=alt.condition(entitySelection, alt.value(1), alt.value(0))
    )
    return chart

if __name__ == '__main__':
    alignmentAlgorithmOutputFilename = 'MultiKE_EN_RU_15K_V1'

    chartMultiKEType = create_chart(alignmentAlgorithmOutputFilename)
    chartMultiKEType.save('results/ontology_' + alignmentAlgorithmOutputFilename + '.html')

    chartEntitiesMultiKE = createEntity_chart(alignmentAlgorithmOutputFilename)
    chartEntitiesMultiKE.save('results/entities_' + alignmentAlgorithmOutputFilename + '.html')