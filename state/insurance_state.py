from state.state import State
from linebot.models import *
from datetime import datetime, timedelta
import json

region_dict = {
    "eastAsia_oceania": "中日韓、紐澳", 
    "southEastAsis": "東南亞", 
    "west": "歐洲、美加", 
    "middleEast": "中東", 
    "southAmerica": "南美、南亞", 
    "africa": "非洲"
}

purpose_dict = {
    "travel": "旅遊",
    "business": "出差",
    "studyTour": "遊學"
}

flight_dict = {
    "budgetAirline": "廉航",
    "first_business": "頭等或商務艙",
    "economy": "經濟艙"
}

class InitState(State):
    message = TemplateSendMessage(
            alt_text = '請問您需要什麼服務？',
            template = ButtonsTemplate(
                type = "buttons",
                title = '旅遊投保機器人',
                text = '您好，歡迎使用台科旅遊投保機器人，請問您需要什麼服務呢？',
                actions = [
                    {
                        "type":"postback",
                        "label":"投保試算",
                        "data":"calculate",
                    },
                    {
                        "type":"uri",
                        "label":"投保問題",
                        "uri":"https://www.ntust.edu.tw/home.php",
                        "altUri": {
                            "desktop": "https://www.ntust.edu.tw/home.php"
                        }
                    },
                    {
                        "type":"uri",
                        "label":"理賠問題",
                        "uri":"https://www.cs.ntust.edu.tw/index.php/zh/",
                        "altUri": {
                            "desktop": "https://www.cs.ntust.edu.tw/index.php/zh/"
                        }
                    },
                ]
            )
        )
    
    def on_event(self, event, data):
        if event == 'calculate':
            return NumPeopleState()
        return self

class NumPeopleState(State):
    message = TextSendMessage(
            text='請選擇投保人數',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=PostbackAction(label="1人", data="numOfPeople&1")),
                    QuickReplyButton(action=PostbackAction(label="2人", data="numOfPeople&2")),
                    QuickReplyButton(action=PostbackAction(label="3人", data="numOfPeople&3")),
                    QuickReplyButton(action=PostbackAction(label="4人", data="numOfPeople&4")),
                    QuickReplyButton(action=PostbackAction(label="5人", data="numOfPeople&5")),
                    QuickReplyButton(action=PostbackAction(label="6人", data="numOfPeople&6")),
                    QuickReplyButton(action=PostbackAction(label="7人", data="numOfPeople&7")),
                    QuickReplyButton(action=PostbackAction(label="8人", data="numOfPeople&8")),
                    QuickReplyButton(action=PostbackAction(label="9人", data="numOfPeople&9")),
                    QuickReplyButton(action=PostbackAction(label="10人", data="numOfPeople&10")),
                    QuickReplyButton(action=PostbackAction(label="上一步", data="back"))
                ]
            ))

    def on_event(self, event, data):
        if event == 'numOfPeople':
            self.data[event] = data
            return RegionState(data=self.data)
        elif event == 'back':
            return InitState()
        return self

class RegionState(State):
    message = TextSendMessage(
            text='請選擇旅遊地區',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=PostbackAction(label="中日韓、紐澳", data="region&eastAsia_oceania")),
                    QuickReplyButton(action=PostbackAction(label="東南亞", data="region&southEastAsis")),
                    QuickReplyButton(action=PostbackAction(label="歐洲、美加", data="region&west")),
                    QuickReplyButton(action=PostbackAction(label="中東", data="region&middleEast")),
                    QuickReplyButton(action=PostbackAction(label="南美、南亞", data="region&southAmerica")),
                    QuickReplyButton(action=PostbackAction(label="非洲", data="region&africa")),
                    QuickReplyButton(action=PostbackAction(label="上一步", data="back"))
                ]
            ))
    
    def on_event(self, event, data):
        if event == 'region':
            self.data[event] = data
            return PurposeState(data=self.data)
        elif event == 'back':
            return NumPeopleState(data=self.data)
        return self

class PurposeState(State):
    message = TextSendMessage(
            text='請選擇旅遊目的',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=PostbackAction(label="旅遊", data="purpose&travel")),
                    QuickReplyButton(action=PostbackAction(label="出差", data="purpose&business")),
                    QuickReplyButton(action=PostbackAction(label="遊學", data="purpose&studyTour")),
                    QuickReplyButton(action=PostbackAction(label="上一步", data="back"))
                ]
            ))

    def on_event(self, event, data):
        if event == 'purpose':
            self.data[event] = data
            return StartDateState(data=self.data)
        elif event == 'back':
            return RegionState(data=self.data)
        return self

class StartDateState(State):
    message = TemplateSendMessage(
            alt_text = '選擇出發日期',
            template = ButtonsTemplate(
                title = '選擇出發日期',
                text = '請選擇您出發的日期',
                actions = [
                    {
                        "type": "datetimepicker",
                        "label": "選擇出發日期",
                        "data": "startDate",
                        "mode": "date",
                        "initial": datetime.now().strftime("%Y-%m-%d"),
                        "max": (datetime.now() + timedelta(days=364)).strftime("%Y-%m-%d"),
                        "min": datetime.now().strftime("%Y-%m-%d"),
                    }
                ]
            )
        )
    
    def on_event(self, event, data):
        if event == 'startDate':
            self.data[event] = data['date']
            return EndDateState(data=self.data)
        elif event == 'back':
            return PurposeState(data=self.data)
        return self

class EndDateState(State):
    def __init__(self, *args, **kwargs):
        self.data = {}
        if kwargs.get('data'):
            self.data = kwargs.get('data')
            self.message = TemplateSendMessage(
                alt_text = '選擇結束日期',
                template = ButtonsTemplate(
                    title = '選擇結束日期',
                    text = '請選擇您結束的日期',
                    actions = [
                        {
                            "type": "datetimepicker",
                            "label": "選擇結束日期",
                            "data": "endDate",
                            "mode": "date",
                            "initial": (datetime.strptime('2019-06-02', "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d"),
                            "max":  (datetime.strptime('2019-06-02', "%Y-%m-%d") + timedelta(days=179)).strftime("%Y-%m-%d"),
                            "min":  (datetime.strptime('2019-06-02', "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d"),
                        }
                    ]
                )
            )

    def on_event(self, event, data):
        if event == 'endDate':
            self.data[event] = data['date']
            return FlightState(data=self.data)
        elif event == 'back':
            return StartDateState(data=self.data)
        return self

class FlightState(State):
    message = TextSendMessage(
            text='請問您搭乘的是？',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=PostbackAction(label="廉航", data="flight&budgetAirline")),
                    QuickReplyButton(action=PostbackAction(label="頭等或商務艙", data="flight&first_business")),
                    QuickReplyButton(action=PostbackAction(label="經濟艙", data="flight&economy")),
                    QuickReplyButton(action=PostbackAction(label="上一步", data="back"))
                ]
            ))

    def on_event(self, event, data):
        if event == 'flight':
            self.data[event] = data
            return FinalState(data=self.data)
        elif event == 'back':
            return EndDateState(data=self.data)
        return self

class FinalState(State):
    def __init__(self, *args, **kwargs):
        self.data = {}
        if kwargs.get('data'):
            self.data = kwargs.get('data')
            self.message = TextSendMessage(text='以下是您輸入的資訊：\n人數：'+str(self.data['numOfPeople'])+'人\n地區：'+str(region_dict[self.data['region']])+'\n目的：'+str(purpose_dict[self.data['purpose']])+'\n日期：'+str(self.data['startDate'])+' ~ '+str(self.data['endDate'])+'\n搭乘：'+str(self.data['flight']))

    def on_event(self, event):
        if event == 'finish':
            return self.data
        return self