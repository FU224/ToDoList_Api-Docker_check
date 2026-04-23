import requests


def get_programming_joke():
    response = requests.get(
        "https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,political,racist,sexist",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
