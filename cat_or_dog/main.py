import pygame, requests, json
from os import environ


def getImages(dogURL, catURL):
    dogImage = requests.get(dogURL)
    catImage = requests.get(catURL)