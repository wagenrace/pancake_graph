CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE;
CALL n10s.graphconfig.init();
CALL n10s.rdf.import.fetch("https://raw.githubusercontent.com/wagenrace/pancake_graph/main/001_Add_ontology/data/new_foodon.owl","RDF/XML");

// Test it by looking the taxonimy of olive oil (extra-virgin)
MATCH (p:Resource {uri: "http://purl.obolibrary.org/obo/FOODON_00002808"})-[r:rdfs__subClassOf*1..]->(k) RETURN p,k

