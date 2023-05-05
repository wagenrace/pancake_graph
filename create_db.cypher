CALL n10s.rdf.import.fetch("file:///C:\\Users\\wagen\\github\\foodnet\\new_foodon.owl","RDF/XML");

MATCH (p:Resource {uri: "http://purl.obolibrary.org/obo/FOODON_00002808"})-[r:rdfs__subClassOf*1..]->(k) RETURN p,k

