class Event(object):
    pass

class Observable(object):
    def __init__(self):
        self.callbacks = {}
        
    def subscribe(self, event_name, callback):
        if not self.callbacks.get(event_name):
            self.callbacks[event_name] = []
        self.callbacks[event_name].append(callback)
        
    def fire(self, event_type, **attrs):
        event = Event()
        event.source = self
        event.type = event_type
        for key, value in attrs.items():
            setattr(event, key, value)
        for func in self.callbacks.get(event_type, []):
            func(event)
