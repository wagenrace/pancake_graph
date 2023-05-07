# %% imports
import json
import os
from py2neo import Graph
from tqdm import tqdm

results_folder = "data"
os.makedirs(results_folder, exist_ok=True)
with open(os.path.join(results_folder, "downloaded_recipes.json"), "r") as fp:
    recipes_json = json.load(fp)

with open(
    os.path.join(results_folder, "ingredients2onfood_ingredients_corrected.json"), "r"
) as fp:
    ingredient_mapping = json.load(fp)

# %% Connect to graph
with open("config.json") as f:
    config = json.load(f)

neo4j_url = config.get("neo4jUrl", "bolt://localhost:7687")
user = config.get("user", "neo4j")
pswd = config.get("pswd", "password")

graph = Graph(neo4j_url, auth=(user, pswd))

# %% Get all unique ingredients
for recipe_json in tqdm(recipes_json):
    name = recipe_json["name"]
    description = recipe_json["description"]
    ingredients_raw = recipe_json["ingredients"]
    ingredients_uri = []

    for ingredient_raw in ingredients_raw:
        for temp in ingredient_raw:
            text = ingredient_raw[temp]["text"]
            ingredients_uri.append(ingredient_mapping[text]["uri"])

    graph.run(
        """
        CREATE (r:Recipe {name: $name, description: $description})
        WITH r
        UNWIND $ingredients_uri as ingredient_uri
        MATCH (i:Resource {uri: ingredient_uri})
        CREATE (r)-[:USES]->(i)
        """,
        ingredients_uri=ingredients_uri,
        name=name,
        description=description,
    ).data()

# %%
