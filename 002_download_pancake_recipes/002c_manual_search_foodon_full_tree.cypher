// Get the top full-text results and all its childern and parents
// Goes in for all generations
CALL {
    CALL db.index.fulltext.queryNodes("classLabel", "mashed potato") YIELD node, score
    RETURN node, node.uri as uri, node.rdfs__label as label, score limit 1
}

MATCH (p)-[r1:rdfs__subClassOf*0..]->(node)-[r2:rdfs__subClassOf*0..]->(k) 
RETURN p, node,k
