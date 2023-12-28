from asyncord.fbenum import UNKNOWN, FallbackEnum


def test_get_unknow_item():
    class TestFBEnum(FallbackEnum):
        A = 1
        B = 2

    item_a = TestFBEnum(1)
    assert item_a is TestFBEnum.A
    assert item_a.value == TestFBEnum.A.value

    unknown_item = TestFBEnum(3)
    assert isinstance(unknown_item, TestFBEnum)
    assert unknown_item.name == UNKNOWN
    assert unknown_item.value == 3

    unknown_item = TestFBEnum(35)
    assert isinstance(unknown_item, TestFBEnum)
    assert unknown_item.name == UNKNOWN
    assert unknown_item.value == 35
    assert unknown_item in TestFBEnum
    assert list(TestFBEnum) == [TestFBEnum.A, TestFBEnum.B]
