from unittest import mock

import pytest

from asyncord.gateway.dispatcher import EventDispatcher, GatewayEvent


@pytest.fixture
def dispatcher():
    return EventDispatcher()


class CustomEvent(GatewayEvent):
    pass


class CustomEvent2(GatewayEvent):
    pass


def test_add_handler_with_event_type(dispatcher: EventDispatcher):
    async def handler(_: CustomEvent):
        pass

    dispatcher.add_handler(handler)

    assert CustomEvent in dispatcher._handlers
    assert handler in dispatcher._handlers[CustomEvent]


def test_add_handler_with_event_type_and_handler(dispatcher: EventDispatcher):
    async def handler(_: CustomEvent):
        pass

    dispatcher.add_handler(CustomEvent, handler)

    assert CustomEvent in dispatcher._handlers
    assert handler in dispatcher._handlers[CustomEvent]


def test_error_if_handler_is_not_callable(dispatcher: EventDispatcher):
    with pytest.raises(TypeError, match='must be Callable'):
        dispatcher.add_handler(CustomEvent, 'must be Callable')  # type: ignore

    with pytest.raises(TypeError, match='must be Callable'):
        dispatcher.add_handler('must be Callable')  # type: ignore


def test_error_if_event_type_is_not_a_type(dispatcher: EventDispatcher):
    with pytest.raises(TypeError, match='Event type must be specified'):
        dispatcher.add_handler('must be a type', lambda _: None)  # type: ignore


def test_add_handler_with_no_event_type(dispatcher):
    with pytest.raises(ValueError, match='Event handler must have at least one argument'):
        dispatcher.add_handler(lambda: None)  # type: ignore

    with pytest.raises(ValueError, match='Event handler must have at least one argument'):
        dispatcher.add_handler(lambda _: None)  # type: ignore


def test_add_handler_with_invalid_event_type(dispatcher):
    async def handler(_: mock.Mock()):  # type: ignore
        pass
    with pytest.raises(TypeError):
        dispatcher.add_handler(str, handler)


def test_add_argument(dispatcher):
    """Test adding an argument to the dispatcher.

    Test that the argument is added to the dispatcher's arguments and
    that it is added to the cached arguments for all handlers.
    """
    async def handler(_: CustomEvent, arg1: str):
        pass

    dispatcher.add_handler(GatewayEvent, handler)
    assert 'arg1' not in dispatcher._args
    assert 'arg1' not in dispatcher._cached_args[handler]

    dispatcher.add_argument('arg1', 'value1')

    assert 'arg1' in dispatcher._args
    assert dispatcher._args['arg1'] == 'value1'

    assert handler in dispatcher._cached_args
    assert 'arg1' in dispatcher._cached_args[handler]
    assert dispatcher._cached_args[handler]['arg1'] == 'value1'


async def test_dispatch(dispatcher):
    """Test dispatching an event.

    Test that the event is dispatched to the correct handler.
    """
    handler = mock.AsyncMock()
    handler.__code__ = mock.Mock(co_argcount=2, co_varnames=['event', 'arg1'])

    dispatcher.add_handler(CustomEvent, handler)
    dispatcher.add_argument('arg1', 'value1')

    event = CustomEvent()
    await dispatcher.dispatch(event)
    handler.assert_called_once_with(event, arg1='value1')


async def test_dispatch_with_no_handlers(dispatcher):
    await dispatcher.dispatch(CustomEvent)  # Should not raise any errors


async def test_dispatch_with_multiple_handlers(dispatcher):
    """Test dispatching an event with multiple handlers."""
    handler1 = mock.AsyncMock()
    handler1.__code__ = mock.Mock(co_argcount=1, co_varnames=['event'])
    handler2 = mock.AsyncMock()
    handler2.__code__ = mock.Mock(co_argcount=2, co_varnames=['event', 'arg1'])
    handler3 = mock.AsyncMock()
    handler3.__code__ = mock.Mock(co_argcount=1, co_varnames=['event'])
    dispatcher.add_argument('arg1', 'value1')

    dispatcher.add_handler(CustomEvent, handler1)
    dispatcher.add_handler(CustomEvent, handler2)
    dispatcher.add_handler(CustomEvent2, handler3)

    event = CustomEvent()

    await dispatcher.dispatch(event)
    handler1.assert_called_once_with(event)
    handler2.assert_called_once_with(event, arg1='value1')
    handler3.assert_not_called()
