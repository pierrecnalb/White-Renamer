class Event(object):
        def __init__(self, sender):
            self._sender = sender
            self._callbacks = set()

        def __iadd__(self, callback):
            self._callbacks.add(callback)

        def __isub__(self, callback):
            self._callbacks.remove(callback)

        def __call__(self, args):
            for callback in self._callbacks:
                callback(self._sender, args)
