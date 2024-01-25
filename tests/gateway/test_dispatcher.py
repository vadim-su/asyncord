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
    async def handler(event: CustomEvent):
        pass

    dispatcher.add_handler(handler)
    assert GatewayEvent in dispatcher._handlers
    assert handler in dispatcher._handlers[GatewayEvent]


def test_add_argument(dispatcher):
    handler = mock.Mock()
    dispatcher.add_handler(GatewayEvent, handler)
    dispatcher.add_argument('arg1', 'value1')
    assert 'arg1' in dispatcher._args
    assert dispatcher._args['arg1'] == 'value1'
    assert handler in dispatcher._cached_args
    assert 'arg1' in dispatcher._cached_args[handler]
    assert dispatcher._cached_args[handler]['arg1'] == 'value1'


@pytest.mark.asyncio
async def test_dispatch(dispatcher, mocker):
    handler = mocker.Mock()
    dispatcher.add_handler(GatewayEvent, handler)
    dispatcher.add_argument('arg1', 'value1')
    event = mocker.Mock(spec=GatewayEvent)
    await dispatcher.dispatch(event)
    handler.assert_called_once_with(event, arg1='value1')


def test_add_handler_with_no_event_type(dispatcher, mocker):
    handler = mocker.Mock()
    dispatcher.add_handler(handler)
    assert GatewayEvent in dispatcher._handlers
    assert handler in dispatcher._handlers[GatewayEvent]


def test_add_handler_with_invalid_event_type(dispatcher, mocker):
    handler = mocker.Mock()
    with pytest.raises(TypeError):
        dispatcher.add_handler(str, handler)


def test_add_argument_with_existing_argument(dispatcher, mocker):
    handler = mocker.Mock()
    dispatcher.add_handler(GatewayEvent, handler)
    dispatcher.add_argument('arg1', 'value1')
    with pytest.raises(ValueError):
        dispatcher.add_argument('arg1', 'value2')


async def test_dispatch_with_no_handlers(dispatcher, mocker):
    event = mocker.Mock(spec=GatewayEvent)
    await dispatcher.dispatch(event)  # Should not raise any errors


async def test_dispatch_with_multiple_handlers(dispatcher, mocker):
    handler1 = mocker.Mock()
    handler2 = mocker.Mock()
    dispatcher.add_handler(GatewayEvent, handler1)
    dispatcher.add_handler(GatewayEvent, handler2)
    event = mocker.Mock(spec=GatewayEvent)
    await dispatcher.dispatch(event)
    handler1.assert_called_once_with(event)
    handler2.assert_called_once_with(event)


def test_update_args_cache(dispatcher, mocker):
    handler = mocker.Mock()
    dispatcher.add_handler(GatewayEvent, handler)
    dispatcher.add_argument('arg1', 'value1')
    dispatcher._update_args_cache(handler)
    assert 'arg1' in dispatcher._cached_args[handler]
    assert dispatcher._cached_args[handler]['arg1'] == 'value1'
