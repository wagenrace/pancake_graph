import requests
from tqdm import tqdm

url = "https://api.food.com/external/v1/nlp/search"

page_num = 1
all_clean_recipes = []
while True:
    data1 = {"contexts": [], "searchTerm": "pancake", "pn": page_num}

    pancakes_page_response = requests.get(url, data1)
    if pancakes_page_response.status_code == 200:
        pancakes_page = pancakes_page_response.json()
        recipes = pancakes_page["response"]["results"]

        if len(recipes) == 0:
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
                # for ingredient in ingredients:
                #     filtered_ingredient = ingredient['hyperlinkFoodTextList']
