from todo import Todo

def test_add_and_list(tmp_path):
    db = tmp_path / "db.json"
    t = Todo(str(db))
    t.add("task1")
    assert "task1" in t.list()

def test_complete(tmp_path):
    db = tmp_path / "db.json"
    t = Todo(str(db))
    t.add("task1")
    t.complete(0)
    assert t.list() == []
