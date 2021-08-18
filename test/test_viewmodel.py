from todo_app.data.session_items import ViewModel,MyItem


def test_status():
    item1 = MyItem('100','Weather','Not Started')
    item2 = MyItem('101','Transport','Done')
    x = ViewModel([item1,item2])

    todoitems1 = x.todoitems
    doneitems = x.doneitems
    assert todoitems1 == [item1]
    assert doneitems == [item2]
