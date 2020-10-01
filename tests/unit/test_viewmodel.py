from viewmodel import ViewModel
import pytest
from datetime import datetime
import dateutil.parser
from card import Card

vm = ViewModel(["my todo items"], ["my doing items"], ["my done items"])
last_modified = '2020-09-20 11:18:26.051811'
today_mock = '2020-10-01 00:16:26.061713'
future_date = '2020-10-25 00:16:26.061713'

card1 = Card("1", "card1", "description1", "done", "2020-09-01 12:16:26.061713")
card2 = Card("2", "card2", "description2", "donerecent", "2020-10-01 11:16:26.061713")
card3 = Card("3", "card3", "description3", "done", "2020-09-02 12:16:26.061713")
items = [card1, card2, card3]

def test_todo_items():
    assert vm.todo_items == ["my todo items"]

def test_doing_items():
    assert vm.doing_items == ["my doing items"]

def test_done_items():
    assert vm.done_items == ["my done items"]

def test_today():
    assert vm.today().date() == datetime.today().date()

def test_older_date():
    assert vm.older_date(last_modified,datetime.today())

def test_not_older_date():
    assert not vm.older_date(future_date,datetime.today())

def test_same_date():
    assert vm.same_date(today_mock,datetime.today())

def test_not_same_date():
    assert not vm.same_date(last_modified,datetime.today())

def test_recent_done_items():
    assert vm.recent_done_items(items) == [card2]

def test_old_done_items():
    assert vm.old_done_items(items) == [card1, card3]