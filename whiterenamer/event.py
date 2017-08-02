class Event(object):
    """ Implementation of a C# style event.
    Usage example:
        class Subject(object):
            def __init__(self):
                self.changed = Event()

            def change(self):
                self.changed("I changed !!!")


        def do_something(*args, **kargs):
            print(*args)


        subject = Subject()
        subject.changed += do_something
        # Trigger the event:
        subject.change()
    """

    def __init__(self):
        self._handlers = set()

    def __iadd__(self, handler):
        self._handlers.add(handler)
        return self

    def __isub__(self, handler):
        try:
            self._handlers.remove(handler)
        except:
            raise ValueError("Handler is not handling this event, so cannot unhandle it.")
        return self

    def __call__(self, *args, **kargs):
        for handler in self._handlers:
            handler(*args, **kargs)
