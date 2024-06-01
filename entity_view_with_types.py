import altair as alt
import pandas as pd

alt.data_transformers.enable("vegafusion")

def create_chart(alignmentAlgorithmOutputFilename):
    xscale = alt.Scale(domain=[-125, 110])
    yscale = alt.Scale(domain=[-125, 110])

    # Data
    alignmentData1 = pd.read_csv('data/' + alignmentAlgorithmOutputFilename + '.csv')
    alignmentData2 = pd.read_csv('data/' + alignmentAlgorithmOutputFilename + '.csv')
    alignmentData2.rename(columns = {'Ent1_ID':'temp'}, inplace = True)
    alignmentData2.rename(columns = {'Ent2_ID':'Ent1_ID'}, inplace = True)
    alignmentData2.rename(columns = {'temp':'Ent2_ID'}, inplace = True)

    # Selectors
    types = [None] + alignmentData1['Type'].unique().tolist()
    type_dropdown = alt.binding_select(options=types, name="Type")
    selector_type_on_dropdown = alt.selection_point(bind=type_dropdown, fields=['Type'])
    selector_entity_on_press = alt.selection_point(fields=['Ent1_ID'], empty=False)

    #
    #
    # Alignment Results
    #
    # 
    alignmentNodes1 = alt.Chart(alignmentData1, title='Alignment Results').properties(width=700, height=700).interactive(    
    ).add_params(selector_entity_on_press, selector_type_on_dropdown).mark_circle(size=75).encode(
        x=alt.X('X:Q').scale(xscale),
        y=alt.Y('Y:Q').scale(yscale),
        tooltip=[   alt.Tooltip('Ent1_ID', title='Entity ID'),
                    'X:Q',
                    'Y:Q',
                    alt.Tooltip('Ent1:O', title='Entity Name'), 
                    alt.Tooltip('Ent2:O', title='Aligned Entity'), 
                    'Language:N', 
                    'Type:N'
                    ],
        color=alt.condition(selector_entity_on_press, alt.value('red'), 'Language'),
        opacity=alt.condition(selector_entity_on_press, alt.value(1.0), alt.value(0.75)),
        order=alt.condition(selector_entity_on_press, alt.value(1), alt.value(0)),
        size=alt.condition(selector_entity_on_press, alt.value(150), alt.value(75))
    ).transform_filter(selector_type_on_dropdown)

    alignmentNodes2 = alt.Chart(alignmentData2).properties(width=700, height=700
    ).mark_circle(size=75).encode(
        x=alt.X('X:Q'),
        y=alt.Y('Y:Q'),
        tooltip=[   alt.Tooltip('Ent1_ID', title='Entity ID'),
                    'X:Q',
                    'Y:Q',
                    alt.Tooltip('Ent1:O', title='Entity Name'), 
                    alt.Tooltip('Ent2:O', title='Aligned Entity'), 
                    'Language:N', 
                    'Type:N'
                ],
        color=alt.condition(selector_entity_on_press, alt.value('red'), 'Language'),
        opacity=alt.condition(selector_entity_on_press, alt.value(1.0), alt.value(0.0)),
        order=alt.condition(selector_entity_on_press, alt.value(1), alt.value(0)),
        size=alt.condition(selector_entity_on_press, alt.value(150), alt.value(75))
    ).transform_filter(selector_type_on_dropdown)
    
    alignmentLookupData = alt.LookupData(alignmentData1, key="Ent1_ID", fields=["X", "Y"])

    alignmentEdges = alt.Chart(alignmentData1).mark_rule(strokeWidth=0.5).properties(width=700, height=700
    ).encode(
        x = alt.X('X:Q'),
        y = alt.Y('Y:Q'),
        x2 = alt.X2('X2:Q'),
        y2 = alt.Y2('Y2:Q'),
        opacity=alt.condition(selector_entity_on_press, alt.value(1.0), alt.value(0.2)),
        color=alt.condition(selector_entity_on_press, alt.value('black'), alt.value('lightgrey')),
        order=alt.condition(selector_entity_on_press, alt.value(1), alt.value(0))
    ).transform_lookup(
        lookup='Ent2_ID',
        from_=alignmentLookupData,
        as_=['X2', 'Y2']
    ).transform_filter(selector_type_on_dropdown)
    
    chart1 = (alignmentEdges + alignmentNodes1 + alignmentNodes2)

    #
    #
    # Entity View
    #
    # 
    alignmentDataFullNames1 = pd.read_csv('data/' + alignmentAlgorithmOutputFilename + '.csv')
    alignmentDataFullNames2 = pd.read_csv('data/' + alignmentAlgorithmOutputFilename + '.csv')
    alignmentDataFullNames2.rename(columns = {'Ent1_ID':'temp'}, inplace = True)
    alignmentDataFullNames2.rename(columns = {'Ent2_ID':'Ent1_ID'}, inplace = True)
    alignmentDataFullNames2.rename(columns = {'temp':'Ent2_ID'}, inplace = True)

    relTriplesEnRu = pd.read_csv('data/rel_triples_en_ru.csv', sep=',', header=None, names=['Ent1_ID', 'Relation', 'Ent2_ID'])

    ent1Chart = alt.Chart(alignmentData1, width=500, height=500, title='Entity View').mark_circle(size=650
    ).interactive().encode(
        x=alt.X('X').scale(xscale),
        y=alt.Y('Y').scale(yscale),
        color='Language',
        opacity=alt.value(1.0),
        tooltip=[   alt.Tooltip('Ent1_ID', title='Entity ID'),
                    'X', 
                    'Y', 
                    alt.Tooltip('Ent1', title='Entity Name'), 
                    'Language', 
                    'Type'
                ]
    ).transform_filter(selector_entity_on_press)

    ent1RelatedEntitiesChart = alt.Chart(relTriplesEnRu).mark_circle(size=100).encode(
        x=alt.X('X:Q'),
        y=alt.Y('Y:Q'),
        opacity=alt.value(1.0),
        color='Language:N',
        tooltip=['ID:Q', 'Name:N', 'X:Q', 'Y:Q', 'Language:N', 'Type:N', 'Relation']
    ).transform_lookup(
        lookup='Ent1_ID',
        from_=alt.LookupData(alignmentDataFullNames1, key="Ent1Full", fields=['Ent1_ID'])
    ).transform_lookup(
        lookup='Ent2_ID',
        from_=alt.LookupData(alignmentDataFullNames1, key="Ent1Full", fields=['Ent1_ID', 'Ent1', 'X', 'Y', 'Language', 'Type']),
        as_=['ID', 'Name', 'X', 'Y', 'Language', 'Type']
    ).transform_filter(selector_entity_on_press)

    ent1EdgesToRelatedEntitiesChart = alt.Chart(relTriplesEnRu).mark_rule(strokeWidth=0.75).encode(
        x=alt.X('X:Q'),
        y=alt.Y('Y:Q'),
        x2=alt.X2('X2:Q'),
        y2=alt.Y2('Y2:Q'),
        opacity=alt.condition(selector_entity_on_press, alt.value(1.0), alt.value(0.0))
    ).transform_lookup(
        lookup='Ent1_ID',
        from_=alt.LookupData(alignmentDataFullNames1, key="Ent1Full", fields=['X', 'Y'])
    ).transform_lookup(
        lookup='Ent2_ID',
        from_=alt.LookupData(alignmentDataFullNames1, key="Ent1Full", fields=['X', 'Y']),
        as_=['X2', 'Y2']
    ).transform_lookup(
        lookup='Ent1_ID',
        from_=alt.LookupData(alignmentDataFullNames1, key="Ent1Full", fields=['Ent1_ID'])
    ).transform_filter(selector_entity_on_press)

    edgesText1 = alt.Chart(relTriplesEnRu).mark_text(fontSize=11).encode(
        x=alt.X('Xa:Q'),
        y=alt.Y('Ya:Q'),
        opacity=alt.condition(selector_entity_on_press, alt.value(1.0), alt.value(0.0)),
        text='Relation'
    ).transform_lookup(
        lookup='Ent1_ID',
        from_=alt.LookupData(alignmentDataFullNames1, key="Ent1Full", fields=['X', 'Y'])
    ).transform_lookup(
        lookup='Ent2_ID',
        from_=alt.LookupData(alignmentDataFullNames1, key="Ent1Full", fields=['X', 'Y']),
        as_=['X2', 'Y2']
    ).transform_lookup(
        lookup='Ent1_ID',
        from_=alt.LookupData(alignmentDataFullNames1, key="Ent1Full", fields=['Ent1_ID'])
    ).transform_filter(selector_entity_on_press
    ).transform_calculate(
        Xa='(datum.X + datum.X2) / 2',
        Ya='(datum.Y + datum.Y2) / 2'
    )

    ent2Chart = alt.Chart(alignmentData2).mark_circle(size=650
    ).encode(
        x=alt.X('X'),
        y=alt.Y('Y'),
        color='Language',
        opacity=alt.value(1.0),
        tooltip=[   alt.Tooltip('Ent1_ID', title='Entity ID'),
                    'X', 
                    'Y', 
                    alt.Tooltip('Ent1', title='Entity Name'), 
                    'Language', 
                    'Type'
                ]
    ).transform_filter(selector_entity_on_press)

    ent2RelatedEntitiesChart = alt.Chart(relTriplesEnRu).mark_circle(size=100).encode(
        x=alt.X('X:Q'),
        y=alt.Y('Y:Q'),
        opacity=alt.value(1.0),
        color='Language:N',
        tooltip=['ID:Q', 'Name:N', 'X:Q', 'Y:Q', 'Language:N', 'Type:N', 'Relation']
    ).transform_lookup(
        lookup='Ent1_ID',
        from_=alt.LookupData(alignmentDataFullNames2, key="Ent1Full", fields=['Ent1_ID'])
    ).transform_lookup(
        lookup='Ent2_ID',
        from_=alt.LookupData(alignmentDataFullNames2, key="Ent1Full", fields=['Ent1_ID', 'Ent1', 'X', 'Y', 'Language', 'Type']),
        as_=['ID', 'Name', 'X', 'Y', 'Language', 'Type']
    ).transform_filter(selector_entity_on_press)

    ent2EdgesToRelatedEntitiesChart = alt.Chart(relTriplesEnRu, width=500, height=500).mark_rule(strokeWidth=0.75).interactive().encode(
        x=alt.X('X:Q'),
        y=alt.Y('Y:Q'),
        x2=alt.X2('X2:Q'),
        y2=alt.Y2('Y2:Q'),
        opacity=alt.condition(selector_entity_on_press, alt.value(1.0), alt.value(0.0)),
    ).transform_lookup(
        lookup='Ent1_ID',
        from_=alt.LookupData(alignmentDataFullNames2, key="Ent1Full", fields=['X', 'Y'])
    ).transform_lookup(
        lookup='Ent2_ID',
        from_=alt.LookupData(alignmentDataFullNames2, key="Ent1Full", fields=['X', 'Y']),
        as_=['X2', 'Y2']
    ).transform_lookup(
        lookup='Ent1_ID',
        from_=alt.LookupData(alignmentDataFullNames2, key="Ent1Full", fields=['Ent1_ID'])
    ).transform_filter(selector_entity_on_press)

    edgesText2 = alt.Chart(relTriplesEnRu).mark_text(fontSize=11).encode(
        x=alt.X('Xa:Q'),
        y=alt.Y('Ya:Q'),
        opacity=alt.condition(selector_entity_on_press, alt.value(1.0), alt.value(0.0)),
        text='Relation'
    ).transform_lookup(
        lookup='Ent1_ID',
        from_=alt.LookupData(alignmentDataFullNames2, key="Ent1Full", fields=['X', 'Y'])
    ).transform_lookup(
        lookup='Ent2_ID',
        from_=alt.LookupData(alignmentDataFullNames2, key="Ent1Full", fields=['X', 'Y']),
        as_=['X2', 'Y2']
    ).transform_lookup(
        lookup='Ent1_ID',
        from_=alt.LookupData(alignmentDataFullNames2, key="Ent1Full", fields=['Ent1_ID'])
    ).transform_filter(selector_entity_on_press
    ).transform_calculate(
        Xa='(datum.X + datum.X2) / 2',
        Ya='(datum.Y + datum.Y2) / 2'
    )

    relationsBetweenAlignedEntitiesChart = alt.Chart(alignmentDataFullNames1).mark_rule(strokeWidth=0.9).encode(
        x=alt.X('X:Q'),
        y=alt.Y('Y:Q'),
        x2=alt.X2('X2:Q'),
        y2=alt.Y2('Y2:Q'),
        opacity=alt.condition(selector_entity_on_press, alt.value(1.0), alt.value(0.0)),
        color=alt.value('red')
    ).transform_lookup(
        lookup='Ent2_ID',
        from_=alt.LookupData(alignmentDataFullNames1, key="Ent1_ID", fields=['X', 'Y']),
        as_=['X2', 'Y2']
    ).transform_filter(selector_entity_on_press)
    
    chart2  =   relationsBetweenAlignedEntitiesChart + \
                ent1EdgesToRelatedEntitiesChart + \
                ent1Chart + \
                ent1RelatedEntitiesChart + \
                edgesText1 + \
                ent2EdgesToRelatedEntitiesChart + \
                ent2Chart + \
                edgesText2 + \
                ent2RelatedEntitiesChart
    

    return chart1 | chart2

if __name__ == '__main__':
    alignmentAlgorithmOutputFilename = 'MultiKE_EN_RU_15K_V1'

    alignmentChart = create_chart(alignmentAlgorithmOutputFilename)

    alignmentChart.save('results/entitiesWithTypes_' + alignmentAlgorithmOutputFilename + '.html')