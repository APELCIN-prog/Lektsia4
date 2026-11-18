import requests
from django.shortcuts import render

# Create your views here.


def get_breeds_dogs():
    breeds = []

    response = requests.get("https://dog.ceo/api/breeds/list/all")
    data = response.json()
    # with open('dogs_names.json', 'w') as f:
    #     json.dump(data, f)

    for breed in data["message"]:
        if data["message"][breed]:
            for k in data["message"][breed]:
                b = breed + " - " + k
                breeds.append(b)
        else:
            breeds.append(breed)

    return breeds


def get_images(breeds_input):
    images = []
    for breed in breeds_input.split(", "):
        if "-" in breed:
            b = breed.split(" - ")
            breed_name = b[0] + "/" + b[1]
            url = f"https://dog.ceo/api/breed/{breed_name}/images/random"
        else:
            url = f"https://dog.ceo/api/breed/{breed}/images/random"
        response = requests.get(url)
        data = response.json()
        # Сохраняем словарь с именем породы и прямой ссылкой на фото
        images.append({"breed": breed, "url": data["message"]})

    return images


def index(request):
    all_breeds = []
    dog_images = []
    query = request.GET.get("breeds", "")

    if "show_breeds" in request.GET:
        all_breeds = get_breeds_dogs()

    if query:
        dog_images = get_images(query)

    context = {
        "all_breeds": all_breeds,
        "dog_images": dog_images,
        "query": query,
    }

    return render(request, "index.html", context)
