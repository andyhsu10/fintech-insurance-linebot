from state.state import State
from linebot.models import *
from datetime import datetime, timedelta, timezone
import pandas as pd
import json

region_list = ["中日韓、紐澳", "東南亞", "歐洲、美加", "中東", "南美、南亞", "非洲"]
purpose_list = ["旅遊", "出差", "遊學"]
flight_list = ["廉航", "頭等或商務艙", "經濟艙"]

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
                        "uri":"https://www.fubon.com/insurance/b2c/content/travel_coverage/index.html",
                        "altUri": {
                            "desktop": "https://www.fubon.com/insurance/b2c/content/travel_coverage/index.html"
                        }
                    },
                    {
                        "type":"uri",
                        "label":"理賠問題",
                        "uri":"https://www.fubon.com/insurance/b2c/content/travel_coverage/index.html",
                        "altUri": {
                            "desktop": "https://www.fubon.com/insurance/b2c/content/travel_coverage/index.html"
                        }
                    },
                ]
            )
        )
    
    def on_event(self, event, data):
        if event == 'calculate':
            self.data['status'] = 'calculate'
            return NumPeopleState(data=self.data)
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
                    QuickReplyButton(action=MessageAction(label="上一步", text="上一步")),
                    QuickReplyButton(action=MessageAction(label="取消", text="取消"))
                ]
            ))

    def on_event(self, event, data):
        if event == 'msg':
            if data == '上一步' or data == '取消':
                return InitState()
            num = int(data.split('人')[0])
            if num >= 1 or num <= 10:
                self.data['numOfPeople'] = num
                return RegionState(data=self.data)
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
                    QuickReplyButton(action=MessageAction(label="上一步", text="上一步")),
                    QuickReplyButton(action=MessageAction(label="取消", text="取消"))
                ]
            ))
    
    def on_event(self, event, data):
        if event == 'msg':
            if data in region_list:
                self.data['region'] = data
                return PurposeState(data=self.data)
            if data == '上一步':
                return NumPeopleState(data=self.data)
            elif data == '取消':
                return InitState()
        return self

class PurposeState(State):
    message = TextSendMessage(
            text='請問您這趟行程的目的是？',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label="旅遊", text="旅遊")),
                    QuickReplyButton(action=MessageAction(label="出差", text="出差")),
                    QuickReplyButton(action=MessageAction(label="遊學", text="遊學")),
                    QuickReplyButton(action=MessageAction(label="上一步", text="上一步")),
                    QuickReplyButton(action=MessageAction(label="取消", text="取消"))
                ]
            ))

    def on_event(self, event, data):
        if event == 'msg':
            if data in purpose_list:
                self.data['purpose'] = data
                return StartDateState(data=self.data)
            if data == '上一步':
                return RegionState(data=self.data)
            elif data == '取消':
                return InitState()
        return self

class StartDateState(State):
    message = TemplateSendMessage(
            alt_text = '選擇出發日期',
            template = ButtonsTemplate(
                title = '出發日期',
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
        self.type = 'Reply'
        if kwargs.get('data'):
            self.data = kwargs.get('data')
            self.message = TemplateSendMessage(
                alt_text = '選擇結束日期',
                template = ButtonsTemplate(
                    title = '結束日期',
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
            self.data['numOfDays'] = (datetime.strptime(self.data['endDate'], "%Y-%m-%d")-datetime.strptime(self.data['startDate'], "%Y-%m-%d")).days+1
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
                    QuickReplyButton(action=MessageAction(label="上一步", text="上一步")),
                    QuickReplyButton(action=MessageAction(label="取消", text="取消"))
                ]
            ))

    def on_event(self, event, data):
        if event == 'msg':
            if data in flight_list:
                self.data['flight'] = data
                return ResultState(data=self.data)
            if data == '上一步':
                return EndDateState(data=self.data)
            elif data == '取消':
                return InitState()
        return self

class ResultState(State):
    def __init__(self, *args, **kwargs):
        self.data = {}
        self.type = 'NoneReply'
        if kwargs.get('data'):
            self.data = kwargs.get('data')
            detail_items = [QuickReplyButton(action=MessageAction(label="不用了，謝謝！", text="不用了，謝謝！"))]
            self.data_detail_items = []

            data = pd.read_csv('insurance.csv', header=0)
            if self.data['purpose'] == '遊學':
                days = '30~280'
            elif self.data['numOfDays'] >= 1 and self.data['numOfDays'] < 10:
                days = '1~10'
            elif self.data['numOfDays'] >= 10 and self.data['numOfDays'] < 30:
                days = '10~30'
            else:
                days = '30~280'
            selection = data.loc[(data['Region'] == self.data['region']) & (data['Purpose'] == self.data['purpose']) & (data['Days'] == days) & (data['Flight'] == self.data['flight']), '旅平險':'總保費']
            header = list(selection)
            text = ''
            for i in range(len(header)-1):
                if selection[header[i]].values[0] and str(selection[header[i]].values[0]) != 'nan':
                    text += str(header[i])+'：'+str(selection[header[i]].values[0])+'\n'
                    if str(header[i]) != '旅平險':
                        detail_items.append(QuickReplyButton(action=MessageAction(label=str(header[i])[0:4], text=str(header[i])[0:4])))
                        self.data_detail_items.append(str(header[i])[0:4])


            fee = selection['總保費'].values[0] * self.data['numOfPeople']
            text = '推薦的保單內容如下：\n\n'+text+'\n總保費：'+str(fee)+'元'

            self.message = [
                TextSendMessage(
                    text='以下是您輸入的資訊：\n人數：'+str(self.data['numOfPeople'])+'人\n地區：'+str(self.data['region'])+'\n目的：'+str(self.data['purpose'])+'\n日期：'+str(self.data['startDate'])+' ~ '+str(self.data['endDate'])+' (共'+str(self.data['numOfDays'])+'天)\n搭乘：'+str(self.data['flight'])
                ), 
                TextSendMessage(text=text),
                TextSendMessage(
                    text='欲知保單詳細內容，可以點擊下方快速鍵以了解更多詳情哦～',
                    quick_reply=QuickReply(
                        items=detail_items
                    )
                )
            ]

    def on_event(self, event, data):
        if event == 'msg':
            if data in self.data_detail_items:
                self.data['select_detail_item'] = data
                self.data['detail_items'] = self.data_detail_items
                return DetailState(data=self.data)
            elif data == '不用了，謝謝！':
                return FinalState()
        return self

class DetailState(State):
    def __init__(self, *args, **kwargs):
        self.data = {}
        self.type = 'Reply'
        if kwargs.get('data'):
            self.data = kwargs.get('data')
            detail_data = pd.read_csv('insurance_datail.csv', header=0)
            selection = detail_data.loc[(detail_data['Type'].str.contains(self.data['select_detail_item'])), 'Type':'Detail']

            detail_items = [QuickReplyButton(action=MessageAction(label="不用了，謝謝！", text="不用了，謝謝！"))]
            for val in self.data['detail_items']:
                detail_items.append(QuickReplyButton(action=MessageAction(label=str(val), text=str(val))))
            self.message = [
                TextSendMessage(text=str(selection['Type'].values[0])+'\n\n'+str(selection['Detail'].values[0])),
                TextSendMessage(
                    text='您還有什麼想要了解的內容嗎？',
                    quick_reply=QuickReply(
                        items=detail_items
                    )
                )
            ]

    def on_event(self, event, data):
        if event == 'msg':
            if data in self.data['detail_items']:
                self.data['select_detail_item'] = data
                return DetailState(data=self.data)
            elif data == '不用了，謝謝！':
                return FinalState()
        return self

class FinalState(State):
    message = TextSendMessage(text='感謝您使用本服務，期待很快能再次為您服務，祝您旅途愉快！！')
