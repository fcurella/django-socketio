from django.template import RequestContext
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from django_socketio import events
import logging

logger = logging.getLogger(__name__)


class ChatIONamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def _get_context(self):
        return RequestContext(self.request)

    def recv_connect(self):
        events.on_connect.send(self.request, self.socket, self._get_context())

    def recv_disconnect(self):
        self.disconnect(silent=True)
        events.on_disconnect.send(self.request, self.socket, self._get_context())

    def on_chat(self, room, *args):
        self.emit_to_room(room, 'chat', *args)
        events.on_message.send(self.request, self.socket, self._get_context(), args)

    def on_subscribe(self, *args):
        for channel in args:
            self.join(channel)
            events.on_subscribe.send(self.request, self.socket, self._get_context(), channel)

    def on_unsubscribe(self, *args):
        for channel in args:
            self.leave(channel)
            events.on_unsubscribe.send(self.request, self.socket, self._get_context(), channel)

    def error(self, *args, **kwargs):
        super(ChatIONamespace, self).error(*args, **kwargs)
        events.on_error.send(self.request, self.socket, self._get_context(),  *args, **kwargs)

    def disconnect(self, *args, **kwargs):
        super(ChatIONamespace, self).disconnect(*args, **kwargs)
        events.on_finish.send(self.request, self.socket, self._get_context(), *args, **kwargs)
