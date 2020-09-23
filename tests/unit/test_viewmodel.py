from viewmodel import ViewModel
import pytest

vm = ViewModel(["my todo items"], ["my doing items"], ["my done items"])

def test_todo_items():
    assert vm.todo_items == ["my todo items"]

def test_doing_items():
    assert vm.doing_items == ["my doing items"]

def test_done_items():
    assert vm.done_items == ["my done items"]