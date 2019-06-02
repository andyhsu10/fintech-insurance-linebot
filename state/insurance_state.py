from state import State
from linebot.models import *

class InitState(State):
    def on_event(self, event):
        if event == 'calculate':
            return NumPeopleState()
        return self

class NumPeopleState(State):
    def on_event(self, event, data):
        if event == 'numOfPeople':
            self.data[event] = data
            return RegionState(data=self.data)
        elif event == 'back':
            return InitState()
        return self

class RegionState(State):
    def on_event(self, event, data):
        if event == 'region':
            self.data[event] = data
            return PurposeState(data=self.data)
        elif event == 'back':
            return NumPeopleState(data=self.data)
        return self

class PurposeState(State):
    def on_event(self, event, data):
        if event == 'purpose':
            self.data[event] = data
            return StartDateState(data=self.data)
        elif event == 'back':
            return RegionState(data=self.data)
        return self

class StartDateState(State):
    def on_event(self, event, data):
        if event == 'startDate':
            self.data[event] = data
            return EndDateState(data=self.data)
        elif event == 'back':
            return PurposeState(data=self.data)
        return self

class EndDateState(State):
    def on_event(self, event, data):
        if event == 'endDate':
            self.data[event] = data
            return FinalState(data=self.data)
        elif event == 'back':
            return StartDateState(data=self.data)
        return self

class FinalState(State):
    def on_event(self, event):
        if event == 'finish':
            return self.data
        return self