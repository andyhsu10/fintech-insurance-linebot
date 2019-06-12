from state.state import State
from linebot.models import *
from datetime import datetime, timedelta, timezone
import json

region_list = ["中日韓、紐澳", "東南亞", "歐洲、美加", "中東", "南美、南亞", "非洲"]
region_dict = {
    "eastAsia_oceania": "中日韓、紐澳", 
    "southEastAsis": "東南亞", 
    "west": "歐洲、美加", 
    "middleEast": "中東", 
    "southAmerica": "南美、南亞", 
    "africa": "非洲"
}

purpose_list = ["旅遊", "出差", "遊學"]
purpose_dict = {
    "travel": "旅遊",
    "business": "出差",
    "studyTour": "遊學"
}

flight_list = ["廉航", "頭等或商務艙", "經濟艙"]
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
            text='請問有多少人要投保呢？ (1~10人)',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label="1人", text="1人")),
                    QuickReplyButton(action=MessageAction(label="2人", text="2人")),
                    QuickReplyButton(action=MessageAction(label="3人", text="3人")),
                    QuickReplyButton(action=MessageAction(label="4人", text="4人")),
                    QuickReplyButton(action=MessageAction(label="5人", text="5人")),
                    QuickReplyButton(action=MessageAction(label="6人", text="6人")),
                    QuickReplyButton(action=MessageAction(label="7人", text="7人")),
                    QuickReplyButton(action=MessageAction(label="8人", text="8人")),
                    QuickReplyButton(action=MessageAction(label="9人", text="9人")),
                    QuickReplyButton(action=MessageAction(label="10人", text="10人")),
                    QuickReplyButton(action=MessageAction(label="上一步", text="上一步"))
                ]
            ))

    def on_event(self, event, data):
        if event == 'msg':
            num = int(data.split('人')[0])
            if num >= 1 or num <= 10:
                self.data['numOfPeople'] = num
                return RegionState(data=self.data)
            if data == '上一步':
                return InitState()
        return self

class RegionState(State):
    message = TextSendMessage(
            text='請問您要去哪裡呢？',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label="中日韓、紐澳", text="中日韓、紐澳")),
                    QuickReplyButton(action=MessageAction(label="東南亞", text="東南亞")),
                    QuickReplyButton(action=MessageAction(label="歐洲、美加", text="歐洲、美加")),
                    QuickReplyButton(action=MessageAction(label="中東", text="中東")),
                    QuickReplyButton(action=MessageAction(label="南美、南亞", text="南美、南亞")),
                    QuickReplyButton(action=MessageAction(label="非洲", text="非洲")),
                    QuickReplyButton(action=MessageAction(label="上一步", text="上一步"))
                ]
            ))
    
    def on_event(self, event, data):
        if event == 'msg':
            if data in region_list:
                self.data['region'] = data
                return PurposeState(data=self.data)
            if data == '上一步':
                return NumPeopleState(data=self.data)
        return self

class PurposeState(State):
    message = TextSendMessage(
            text='請問您這趟行程的目的是？',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label="旅遊", text="旅遊")),
                    QuickReplyButton(action=MessageAction(label="出差", text="出差")),
                    QuickReplyButton(action=MessageAction(label="遊學", text="遊學")),
                    QuickReplyButton(action=MessageAction(label="上一步", text="上一步"))
                ]
            ))

    def on_event(self, event, data):
        if event == 'msg':
            if data in purpose_list:
                self.data['purpose'] = data
                return StartDateState(data=self.data)
            if data == '上一步':
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
                        "initial": datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d"),
                        "max": (datetime.now(timezone(timedelta(hours=8))) + timedelta(days=364)).strftime("%Y-%m-%d"),
                        "min": datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d"),
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
                            "initial": (datetime.strptime(self.data['startDate'], "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d"),
                            "max":  (datetime.strptime(self.data['startDate'], "%Y-%m-%d") + timedelta(days=179)).strftime("%Y-%m-%d"),
                            "min":  (datetime.strptime(self.data['startDate'], "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d"),
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
                    QuickReplyButton(action=MessageAction(label="廉航", text="廉航")),
                    QuickReplyButton(action=MessageAction(label="頭等或商務艙", text="頭等或商務艙")),
                    QuickReplyButton(action=MessageAction(label="經濟艙", text="經濟艙")),
                    QuickReplyButton(action=MessageAction(label="上一步", text="上一步"))
                ]
            ))

    def on_event(self, event, data):
        if event == 'msg':
            if data in flight_list:
                self.data['flight'] = data
                return FinalState(data=self.data)
            if data == '上一步':
                return EndDateState(data=self.data)
        return self

class FinalState(State):
    def __init__(self, *args, **kwargs):
        self.data = {}
        if kwargs.get('data'):
            self.data = kwargs.get('data')
            self.message = TextSendMessage(text='以下是您輸入的資訊：\n人數：'+str(self.data['numOfPeople'])+'人\n地區：'+str(self.data['region'])+'\n目的：'+str(self.data['purpose'])+'\n日期：'+str(self.data['startDate'])+' ~ '+str(self.data['endDate'])+' (共'+str((datetime.strptime(self.data['endDate'], "%Y-%m-%d")-datetime.strptime(self.data['startDate'], "%Y-%m-%d")).days+1)+'天)\n搭乘：'+str(self.data['flight']))

    def on_event(self, event):
        if event == 'finish':
            return self.data
        return self