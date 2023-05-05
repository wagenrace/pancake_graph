from owlready2 import get_ontology

onto = get_ontology(
    "https://raw.githubusercontent.com/FoodOntology/foodon/master/foodon.owl"
)
onto.load()
onto.save(file = "new_foodon.owl", format = "rdfxml")