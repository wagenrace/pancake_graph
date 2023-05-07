// Find 25 top full-text results
CALL db.index.fulltext.queryNodes("classLabel", "nutmeg") YIELD node, score
RETURN node.uri as uri, node.rdfs__label as label, score limit 25