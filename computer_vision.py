import requests
import urllib
from bs4 import BeautifulSoup
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def parse_text_from_image(image_url):
    ocr_url = "https://eastus.api.cognitive.microsoft.com/vision/v2.0/ocr"
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, "Content-Type": 'application/octet-stream'}
    params  = {'detectOrientation': 'true', 'language': 'zh-Hans'}

    with open(image_url, 'rb') as f:
        data = f.read()

    response = requests.post(ocr_url, headers=headers, params=params, data=data)
    response.raise_for_status()

    analysis = response.json()
    items = []
    for region in analysis["regions"]:
        for line in region["lines"]:
            item = ""
            words = line["words"]
            for word in words:
                try:
                    int(word["text"])
                except:
                    if word["text"]!="元":
                        item += (word["text"])
            if item != "":
                items.append(item)
    return get_images_of_food(items)

def get_images_of_food(items):
    imgs = []
    for item in items:
        img_dict = {}
        url = 'https://www.douguo.com/search/recipe/' + urllib.parse.quote(item.encode("utf-8"))
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        attributes = soup.find("a", class_="cook-img").attrs
        img = attributes["style"].split()[1][4:-1]
        img_dict["item"] = item
        img_dict["img"] = img

        attributes = soup.find("a", class_="cook-img").attrs
        food_id = attributes["href"].split("/")[2]
        img_dict["food_id"] = food_id
        imgs.append(img_dict)
    return imgs

def get_ingredients(food_id, language):
    url = "https://www.douguo.com/cookbook/" + food_id
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    ingredients = soup.findAll("span", class_="scname")
    return translate_ingredients(list(map(lambda x: x.text, ingredients)), language)

def translate_ingredients(ingredients, language):
    base_url = 'https://api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'
    params = '&to=' + language
    constructed_url = base_url + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscriptionKey,
        'Content-type': 'application/json'
    }

    body = [{
    'text' : ",".join(ingredients)
    }]
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()[0]["translations"][0]["text"]
    return response

items = parse_text_from_image("public/menu4.png")
print(items)
# print(get_images_of_food(items))