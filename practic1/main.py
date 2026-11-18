import requests
import json

response = requests.get("https://pokeapi.co/api/v2/pokemon")
data = response.json()
with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file)

pocemons_names = []
dict_pocemons = {}
for pocemon in data["results"]:
    pocemons_names.append(pocemon["name"])
    dict_pocemons[pocemon["name"]] = pocemon["url"]

print(pocemons_names)
while True:
    pocemon_name = input("Введите имя покемона: ")

    if pocemon_name in pocemons_names:
        pocemon_info = requests.get(dict_pocemons[pocemon_name])
        info = pocemon_info.json()
        with open("pocemon_info.json", "w") as f:
            json.dump(info, f)

        print(f"Имя: {info['name']}")
        print(f"Тип: {info['types'][0]['type']['name']}")
        print(f"Вес: {info['weight']}")
        print(f"Рост: {info['height']}")

        pocemon_abilities = []
        for item in info["abilities"]:
            pocemon_abilities.append(item["ability"]["name"])

        print(f"Способности: {pocemon_abilities}")
        break
    else:
        print("Такого покемона нет")
