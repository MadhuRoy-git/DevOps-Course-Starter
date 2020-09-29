import requests
import os
from card import Card
from flask import current_app as app

key = os.getenv('key')
token = os.getenv('token')
boardid = os.getenv('boardid')

TODO_LIST_ID = '5f3a9a92b421455eaa2ca175'
DOING_LIST_ID = '5f3a9a92b421455eaa2ca176'
DONE_LIST_ID = '5f3a9a92b421455eaa2ca177'


def get_items():
    """
    Fetches all cards from our Trello board.
    Returns:
        list: The nested list of cards containing all cards constructed using the Card class.
    """
    todo_cards = []
    doing_cards = []
    done_cards = []
    cards = get_cards_from_board(boardid)
    for card in cards :
        list_name = get_list_name(card['id'])
        new_card = Card(card['id'], card['name'], card['desc'], list_name, card['dateLastActivity'])
        if list_name == "To Do":
            todo_cards.append(new_card)
        elif list_name == "Doing":
            doing_cards.append(new_card)
        else:
            done_cards.append(new_card)
    return [todo_cards, doing_cards, done_cards]

def get_cards_from_board(board_id):
    """
    Fetches all cards from the board.

    Returns:
        list: The list of cards.
    """

    query = {
        'key': key,
        'token': token
    }
   
    url = f"https://api.trello.com/1/boards/{board_id}/cards"

    return requests.request("GET", url, params=query).json()

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
        'pos': len(get_cards_from_board(boardid)) + 1, 
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

def start_item(item_id):
    """
    Moves a card to the 'DOING' list of the board.
    """
    url = f"https://api.trello.com/1/cards/{item_id}"
    query = {
        'key': key,
        'token': token,
        'idList': DOING_LIST_ID
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
