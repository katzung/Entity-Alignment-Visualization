import entity_view_and_ontology
import entity_view_with_types
import treemap
import os

if __name__ == '__main__':
    if os.path.isdir('results') == False:
        os.mkdir('results')

    alignmentAlgorithmOutputFilename = 'MultiKE_EN_RU_15K_V1'

    entitiesWithOntologyChart = entity_view_and_ontology.create_chart(alignmentAlgorithmOutputFilename)
    entitiesWithOntologyChart.save('results/ontology_' + alignmentAlgorithmOutputFilename + '.html')

    entitiesChart = entity_view_and_ontology.createEntity_chart(alignmentAlgorithmOutputFilename)
    entitiesChart.save('results/entities_' + alignmentAlgorithmOutputFilename + '.html')

    entitiesWithTypesChart = entity_view_with_types.create_chart(alignmentAlgorithmOutputFilename)
    entitiesWithTypesChart.save('results/entitiesWithTypes_' + alignmentAlgorithmOutputFilename + '.html')

    treemap.createTreemap(alignmentAlgorithmOutputFilename)

