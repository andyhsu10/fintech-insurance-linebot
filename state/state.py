class State(object):
    """
    A state object which provides some utility functions for the individual states within the state machine.
    """

    def __init__(self, *args, **kwargs):
        self.data = {}
        if kwargs.get('data'):
            self.data = kwargs.get('data')

    def on_event(self, event):
        """
        Handle events that are delegated to this State.
        """
        pass

    def __repr__(self):
        """
        Leverages the __str__ method to describe the State.
        """
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__