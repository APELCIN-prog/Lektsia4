from django.shortcuts import render
import requests


# Create your views here.
def add_pocemon(pocemon):
    return pocemon


def get_all_pocemons():
    response = requests.get(
        "https://pokeapi.co/api/v2/pokemon", params={"limit": 10000}
    )
    data = response.json()

    pocemons_names = []
    dict_pocemons = {}
    for pocemon in data["results"]:
        pocemons_names.append(pocemon["name"])
        dict_pocemons[pocemon["name"]] = pocemon["url"]

    return dict_pocemons


def find(pocemon):
    infprmation = {}
    url = f"https://pokeapi.co/api/v2/pokemon/{pocemon}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    info = response.json()
    image = info["sprites"]["front_default"]
    infprmation["image"] = image
    infprmation["name"] = info["name"]
    infprmation["type"] = info["types"][0]["type"]["name"]
    infprmation["weight"] = info["weight"]
    infprmation["height"] = info["height"]
    pocemon_abilities = []

    for item in info["abilities"]:
        pocemon_abilities.append(item["ability"]["name"])
    infprmation["abilities"] = pocemon_abilities

    for item in info["stats"]:
        name = item["stat"]["name"]
        value = item["base_stat"]
        infprmation[name] = value

    return infprmation


def batle_pocemons(poc1, poc2):
    pocemon1 = find(poc1)
    pocemon2 = find(poc2)
    move = []
    winner = ''
    if pocemon1 is None or pocemon2 is None:
        return 'Ошибка'

    if pocemon1['speed'] >= pocemon2['speed']:
        move = [pocemon1, pocemon2]
    else:
        move = [pocemon2, pocemon1]

    count = 0
    while True:
        attack_pocemon = move[count % 2]
        defense_pocemon = move[(count + 1) % 2]
        damage = max(5, attack_pocemon['attack'] - defense_pocemon['defense'] // 2)
        defense_pocemon['hp'] = defense_pocemon['hp'] - damage
        if defense_pocemon['hp'] <= 0:
            winner = attack_pocemon['name']
            break
        count += 1

    return f"{winner} победил!"




def index(request):
    my_command = request.session.get("my_command", [])
    all_pocemons = {}
    query = request.GET.get("pocemons", "")
    pocemon1 = request.GET.get("pocemon1", "")
    pocemon2 = request.GET.get("pocemon2", "")
    find_pocemon = None
    winner_text = None

    if "show_pocemons" in request.GET:
        all_pocemons = get_all_pocemons()

    if "add_pokemon" in request.GET:
        new_pocemon = request.GET.get("add_pokemon")
        if new_pocemon not in my_command:
            my_command.append(new_pocemon)
            request.session["my_command"] = my_command
            request.session.modified = True

    if query:
        find_pocemon = find(query)

    if pocemon1 and pocemon2:
        winner_text = batle_pocemons(pocemon1, pocemon2)

    if "find_poсemon" in request.GET:
        new_pocemon = request.GET.get("find_poсemon")
        find_pocemon = find(new_pocemon)
        query = find_pocemon["name"]

    if "delete_poсemon" in request.GET:
        new_pocemon = request.GET.get("delete_poсemon")
        my_command.remove(new_pocemon)
        request.session["my_command"] = my_command
        request.session.modified = True

    context = {
        "my_command": my_command,
        "all_pocemons": all_pocemons,
        "query": query,
        "find_pocemon": find_pocemon,
        "winner_text": winner_text
    }

    return render(request, "index.html", context)
