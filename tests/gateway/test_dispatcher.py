import logging
from unittest import mock

import pytest

from asyncord.gateway.dispatcher import EventDispatcher, GatewayEvent


@pytest.fixture
def dispatcher() -> EventDispatcher:
    """Return an event dispatcher."""
    return EventDispatcher()


class CustomEvent(GatewayEvent):
    """Custom event for testing."""


class CustomEvent2(GatewayEvent):
    """Custom event for testing."""


def test_add_handler_with_event_type(dispatcher: EventDispatcher) -> None:
    """Test adding a handler with an event type."""

    async def handler(_: CustomEvent) -> None:
        pass

    dispatcher.add_handler(handler)

    assert CustomEvent in dispatcher._handlers
    assert handler in dispatcher._handlers[CustomEvent]


def test_add_handler_with_event_type_and_handler(dispatcher: EventDispatcher) -> None:
    """Test adding a handler with an event type and handler."""

    async def handler(_: CustomEvent) -> None:
        pass

    dispatcher.add_handler(CustomEvent, handler)

    assert CustomEvent in dispatcher._handlers
    assert handler in dispatcher._handlers[CustomEvent]


def test_error_if_handler_is_not_callable(dispatcher: EventDispatcher) -> None:
    """Test adding a handler that is not callable."""
    with pytest.raises(TypeError, match='must be Callable'):
        dispatcher.add_handler(CustomEvent, 'must be Callable')  # type: ignore

    with pytest.raises(TypeError, match=r'Event handler must be specified.*'):
        dispatcher.add_handler('must be Callable')  # type: ignore


def test_error_if_event_type_is_not_a_type(dispatcher: EventDispatcher) -> None:
    """Test adding a handler with an event type that is not a type."""
    with pytest.raises(TypeError, match='Event type must be specified'):
        dispatcher.add_handler('must be a type', lambda _: None)  # type: ignore


def test_add_handler_with_no_event_type(dispatcher: EventDispatcher) -> None:
    """Test adding a handler with no event type."""
    with pytest.raises(TypeError, match='Event handler must have at least one argument'):
        dispatcher.add_handler(lambda: None)  # type: ignore

    with pytest.raises(TypeError, match='Event handler must have at least one argument'):
        dispatcher.add_handler(lambda _: None)  # type: ignore


def test_add_handler_with_invalid_event_type(dispatcher: EventDispatcher) -> None:
    """Test adding a handler with an invalid event type."""

    async def handler(_: mock.Mock()) -> None:  # type: ignore
        pass

    with pytest.raises(TypeError, match=r'Event type must be specified.*'):
        dispatcher.add_handler(str, handler)  # type: ignore


def test_add_argument(dispatcher: EventDispatcher) -> None:
    """Test adding an argument to the dispatcher.

    Test that the argument is added to the dispatcher's arguments and
    that it is added to the cached arguments for all handlers.
    """

    async def handler(_: CustomEvent, arg1: str) -> None:
        pass

    dispatcher.add_handler(GatewayEvent, handler)  # type: ignore
    assert 'arg1' not in dispatcher._args
    assert 'arg1' not in dispatcher._cached_args[handler]

    dispatcher.add_argument('arg1', 'value1')

    assert 'arg1' in dispatcher._args
    assert dispatcher._args['arg1'] == 'value1'

    assert handler in dispatcher._cached_args
    assert 'arg1' in dispatcher._cached_args[handler]
    assert dispatcher._cached_args[handler]['arg1'] == 'value1'


async def test_dispatch(dispatcher: EventDispatcher) -> None:
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


async def test_dispatch_calls_correct_handler(dispatcher: EventDispatcher) -> None:
    """Test that dispatch calls the correct handler for a given event."""
    event = CustomEvent()
    handler_called = False

    async def handler(event: CustomEvent) -> None:
        nonlocal handler_called
        handler_called = True

    dispatcher.add_handler(CustomEvent, handler)
    await dispatcher.dispatch(event)

    assert handler_called, 'Handler was not called'


async def test_dispatch_does_not_call_incorrect_handler(dispatcher: EventDispatcher) -> None:
    """Test that dispatch does not call handlers for different events."""
    handler_called = False

    async def handler(event: CustomEvent2) -> None:
        nonlocal handler_called
        handler_called = True

    dispatcher.add_handler(CustomEvent2, handler)
    await dispatcher.dispatch(CustomEvent())

    assert not handler_called, 'Handler was incorrectly called'


async def test_dispatch_passes_arguments_to_handler(dispatcher: EventDispatcher) -> None:
    """Test that dispatch passes the correct arguments to the handler."""
    event = CustomEvent()
    received_args = None

    async def handler(event: CustomEvent, arg1: str) -> None:
        nonlocal received_args
        received_args = arg1

    dispatcher.add_handler(CustomEvent, handler)
    dispatcher.add_argument('arg1', 'value1')
    await dispatcher.dispatch(event)

    assert received_args == 'value1', 'Handler did not receive correct arguments'


async def test_dispatch_logs_exception(
    dispatcher: EventDispatcher,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that dispatch logs an exception if one is raised in the handler."""
    event = CustomEvent()

    async def handler(event: CustomEvent) -> None:
        raise Exception('Test exception')

    dispatcher.add_handler(CustomEvent, handler)
    with caplog.at_level(logging.ERROR):
        await dispatcher.dispatch(event)

    assert 'Unhandled exception in event handler' in caplog.text, 'Exception was not logged'


async def test_dispatch_with_no_handlers(dispatcher: EventDispatcher) -> None:
    """Test dispatching an event with no handlers.

    It should not raise any errors.
    """
    await dispatcher.dispatch(CustomEvent())


async def test_dispatch_with_multiple_handlers(dispatcher: EventDispatcher) -> None:
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
