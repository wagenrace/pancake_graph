# %% imports
import json
import os
from py2neo import Graph

results_folder = "data"
os.makedirs(results_folder, exist_ok=True)
with open(os.path.join(results_folder, "downloaded_recipes.json"), "r") as fp:
    recipes_json = json.load(fp)

all_ingredients = []

# %% Get all unique ingredients
for recipe_json in recipes_json:
    ingredients = recipe_json["ingredients"]

    for ingredient in ingredients:
        for temp in ingredient:
            text = ingredient[temp]["text"]
            all_ingredients.append(text)

unique_ingredients = list(set(all_ingredients))
print(unique_ingredients)
print(len(unique_ingredients))

# %% Connect to graph
with open("config.json") as f:
    config = json.load(f)

neo4j_url = config.get("neo4jUrl", "bolt://localhost:7687")
user = config.get("user", "neo4j")
pswd = config.get("pswd", "password")

graph = Graph(neo4j_url, auth=(user, pswd))

# %% Connect to foodon in neo4j
linked_ingredients = {}

for ingredient in unique_ingredients:
    if ingredient == "eggs":
        ingredient_use_name = "egg"
    elif ingredient == "soymilk":
        ingredient_use_name = "soy milk"
    else:
        ingredient_use_name = ingredient
    response = graph.run(
        """
        CALL db.index.fulltext.queryNodes("classLabel", $ingredient) YIELD node, score
        RETURN node.uri as uri, node.rdfs__label as label, score limit 1
        """,
        ingredient=ingredient_use_name,
    ).data()
    if len(response) == 0:
        print(f"No match found for {ingredient}")
        continue
    print(f"{ingredient} : {response[0]['label']}")
    linked_ingredients[ingredient] = response[0]

# %% Save results
with open(
    os.path.join(results_folder, "ingredients2onfood_ingredients.json"), "w"
) as fp:
    json.dump(linked_ingredients, fp, indent=4)
