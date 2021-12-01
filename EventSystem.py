

events = dict()

def __add_event(event_name):
	events[event_name] = []

def __trigger_listeners(event_name, *args, **kvargs):
	for listener in events[event_name]:
		listener(*args, **kvargs)

def register_listener(event_name, listener):
	if event_name not in events:
		return False

	events[event_name].append(listener)
	return True