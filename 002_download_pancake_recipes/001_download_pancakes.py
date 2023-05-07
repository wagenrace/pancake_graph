import json
import os

import requests
from tqdm import tqdm

url_food_search = "https://api.food.com/external/v1/nlp/search"

page_num = 1
all_clean_recipes = []
while True:
    # Download all recipes from a search food.com page
    data1 = {"contexts": [], "searchTerm": "pancake", "pn": page_num}
    pancakes_page_response = requests.get(url_food_search, data1)
    if pancakes_page_response.status_code != 200:
        break

    pancakes_page = pancakes_page_response.json()
    recipes = pancakes_page["response"]["results"]

    if len(recipes) == 0:
        # We are past the last page, we need to stop
        break

    for recipe in tqdm(recipes):
        full_url = recipe["record_url"]
        json_url = full_url.replace(r"https://www.", "https://api.") + "/as-json"
        recipe_full_response = requests.get(json_url)
        if recipe_full_response.status_code == 200:
            recipe_full = recipe_full_response.json()["recipe"]
            ingredients = recipe_full["ingredients"]
            filtered_ingredients = [
                ingredient["hyperlinkFoodTextList"] for ingredient in ingredients
            ]
            all_clean_recipes.append(
                {
                    "name": recipe_full["title"],
                    "description": recipe_full["description"],
                    "ingredients": filtered_ingredients,
                }
            )

results_folder = "data"
os.makedirs(results_folder, exist_ok=True)
with open(os.path.join(results_folder, "downloaded_recipes.json"), "w") as fp:
    json.dump(all_clean_recipes, fp)
