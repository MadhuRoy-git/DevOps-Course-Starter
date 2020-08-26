import requests
import os
from card import Card

key = os.getenv('apiKey')
token = os.getenv('apiToken')

TODO_LIST_ID = '5f3a9a92b421455eaa2ca175'
DONE_LIST_ID = '5f3a9a92b421455eaa2ca177'

def get_cards_for_board():
    """
    Fetches all cards from the board.

    Returns:
        list: The list of cards.
    """

    query = {
        'key': key,
        'token': token
    }
   
    board_id = os.getenv('boardId')
    all_cards = []
    url = f"https://api.trello.com/1/boards/{board_id}/cards"
    cards = requests.request("GET", url, params=query)
    for card in cards.json():
        all_cards.append(Card(card['id'], card['pos'], card['name'], card['desc'], get_list_name(card['id'])))
    return all_cards

def get_list_name(card_id):
    """
    Gets the list name a specific card is in, based on the card's id.
    Returns:
        string: The list's name.
    """
    url = f"https://api.trello.com/1/cards/{card_id}/list"
    query = {
        'key': key,
        'token': token
    }
    list = requests.request("GET", url, params=query)
    return list.json()['name']


def create_item(title, description):
    """
    Creates a card in the TO DO list of the board.
    Returns:
        Card: The newly created Card object.
    """
    url = "https://api.trello.com/1/cards"
    query = {
        'key': key,
        'token': token,
        'name': title, 
        'desc': description,
        'pos': len(get_cards_for_board()) + 1, 
        'idList': TODO_LIST_ID
    }
    card = requests.request("POST", url, params=query)
    return card


def complete_item(item_id):
    """
    Moves a card to the 'DONE' list of the board.
    """
    url = f"https://api.trello.com/1/cards/{item_id}"
    query = {
        'key': key,
        'token': token,
        'idList': DONE_LIST_ID
    }
    requests.request("PUT", url, params=query)


def undo_item(item_id):
    """
    Moves a card to the 'TODO' list of the board.
    """
    url = f"https://api.trello.com/1/cards/{item_id}"
    query = {
        'key': key,
        'token': token,
        'idList': TODO_LIST_ID
    }
    requests.request("PUT", url, params=query)
