import entity_view_and_ontology
import entity_view_with_types
import treemap
import os

if __name__ == '__main__':
    alignmentAlgorithmOutputFilename = 'MultiKE_EN_RU_15K_V1_graph'
    saveFolder = 'results/' + alignmentAlgorithmOutputFilename

    if os.path.isdir(saveFolder) == False:
        os.mkdir(saveFolder)

    entitiesWithOntologyChart = entity_view_and_ontology.create_chart(alignmentAlgorithmOutputFilename)
    entitiesWithOntologyChart.save(saveFolder + '/ontology_' + alignmentAlgorithmOutputFilename + '.html')

    entitiesChart = entity_view_and_ontology.createEntity_chart(alignmentAlgorithmOutputFilename)
    entitiesChart.save(saveFolder + '/entities_' + alignmentAlgorithmOutputFilename + '.html')

    entitiesWithTypesChart = entity_view_with_types.create_chart(alignmentAlgorithmOutputFilename)
    entitiesWithTypesChart.save(saveFolder + '/entitiesWithTypes_' + alignmentAlgorithmOutputFilename + '.html')

    treemap.createTreemap(alignmentAlgorithmOutputFilename)

