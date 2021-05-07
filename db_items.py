from flask import session
import requests
import os
from card import Card
import sys
import uuid
from datetime import date

def get_items(collection, board_id):
    """
    Fetches all cards from mongoDB collection.
    Returns:
        list: The nested list of cards containing all cards constructed using the Card class.
    """
    todo_cards = []
    doing_cards = []
    done_cards = []
    for list_name in ['todo', 'doing', 'done']:
        dbList = get_list(collection, board_id, list_name)
        if dbList != None:
            for obj in dbList:
                cards = obj["cards"]
                card_id = cards.get("card_id", "")
                card_name = cards.get("card_name", "")
                card_desc = cards.get("card_desc", "")
                card_dateLastActivity = cards.get("card_dateLastActivity", "")
                new_card = Card(card_id, card_name, card_desc, list_name, card_dateLastActivity)

                if list_name == "todo":
                    todo_cards.append(new_card)
                elif list_name == "doing":
                    doing_cards.append(new_card)
                else:
                    done_cards.append(new_card)
    return [todo_cards, doing_cards, done_cards]


def get_list(collection, board_id, list_name):
    """
    Fetches a given list by board id and list name from the DB.
    Returns:
        board: The list with the given name.
    """
    return list(collection.find(
        { 
            'board_id': board_id,
            'list_name': list_name
        }
    ))


def insert(collection, board_id, list_name, item_id, title, description):
    """
    Creates a card in a given list of the board.
    """
    collection.insert_one(
        { 
            'board_id': board_id,
            'list_name': list_name,
            'cards': {
                'card_id': item_id,
                'card_name': title,
                'card_desc': description,
                'card_dateLastActivity': str(date.today())
            }
        }
    )

def get(collection, item_id):
    """
    Gets a card from the given list (by index) of the board.
    """
    return collection.find_one(
        { 
            'cards.card_id': item_id
        }
    )

def delete(collection, item_id):
    """
    Removes a card from the given list (by index) of the board.
    """
    collection.delete_one(
        { 
            'cards.card_id': item_id
        }
    )

def create_item(collection, board_id, title, description):
    """
    Creates a card in the TO DO list of the board.
    """
    insert(collection, board_id, 'todo', str(uuid.uuid4()), title, description)

    
def start_item(collection, board_id, item_id):
    """
    Moves a card to the 'DOING' list of the board.
    """
    item = get(collection, item_id)
    if item != None:
        # remove item from todo list
        delete(collection, item_id)
        # insert item in doing list
        insert(collection, board_id, 'doing', item_id, item['cards']['card_name'], item['cards']['card_desc'])


def complete_item(collection, board_id, item_id):
    """
    Moves a card to the 'DONE' list of the board.
    """
    item = get(collection, item_id)
    if item != None:
        # remove item from doing list
        delete(collection, item_id)
        # insert item in done list
        insert(collection, board_id, 'done', item_id, item['cards']['card_name'], item['cards']['card_desc'])
    
def undo_item(collection, board_id, item_id):
    """
    Moves a card to the 'DOING' list of the board.
    """
    item = get(collection, item_id)
    if item != None:
        # remove item from doing list
        delete(collection, item_id)
        # insert item in done list
        insert(collection, board_id, 'todo', item_id, item['cards']['card_name'], item['cards']['card_desc'])

