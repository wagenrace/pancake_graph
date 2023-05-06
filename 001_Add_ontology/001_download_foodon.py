import os

from owlready2 import get_ontology

""" 
Loading the owl file directly will give an error because the formate is not recognized by n10s.
owlready2 does recognize the format but saves it in a different (also valid) owl format. 
This output of owlready2 is recognized by n10s.
"""
onto = get_ontology(
    "https://raw.githubusercontent.com/FoodOntology/foodon/master/foodon.owl"
)
onto.load()
onto.save(file=os.path.join("data", "new_foodon.owl"), format="rdfxml")
