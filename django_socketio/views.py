
from django.http import HttpResponse
from django_socketio.namespaces import ChatIONamespace
from socketio import socketio_manage


def socketio(request):
    """
    Socket.IO handler - maintains the lifecycle of a Socket.IO
    request, sending the each of the events. Also handles
    adding/removing request/socket pairs to the CLIENTS dict
    which is used for sending on_finish events when the server
    stops.
    """
    socketio_manage(request.environ, namespaces={'': ChatIONamespace}, request=request)
    return HttpResponse("")
