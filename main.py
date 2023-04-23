import os
import requests
import json

from datetime import date, datetime, timezone, timedelta
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate

today = datetime.now()

# 微信公众测试号ID和SECRET
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

# 可把os.environ结果替换成字符串在本地调试
user_ids = os.environ["USER_ID"].split(',')
template_ids = os.environ["TEMPLATE_ID"].split(',')
cookies = os.environ["COOKIE"].split(',')
lotteryNums = os.environ["LOTTERYNUM"].split(',')

# 签到
def check_in():
    url = "https://glados.rocks/api/user/checkin"
    headers = {
        "cookie": cookies[0],
        "content-type": "application/json;charset=UTF-8"
    }
    data = {"token": "glados.network"}
    res = requests.post(url,data = json.dumps(data),headers = headers).json()
    message = res['message']
    checkinTime = res['list'][0]['time']
    return message, checkinTime

# 获取剩余天数
def get_leftdays():
    url = "https://glados.rocks/api/user/status"
    headers = {
        "cookie": cookies[0]
    }
    res = requests.get(url,headers = headers).json()
    leftDays = res['data']['leftDays']
    return leftDays
    
# 查询大乐透开奖
def get_lotteryres(num):
    url = "https://webapi.sporttery.cn/gateway/lottery/getDigitalDrawInfoV1.qry?param=85%2C0&isVerify=1"
    res = requests.get(url).json()
    lotteryres = res['value']['dlt']
    
    result = {
        # 开奖期号
        'lotteryDrawNum': lotteryres['lotteryDrawNum'],
        # 开奖结果
        'lotteryDrawResult': lotteryres['lotteryDrawResult'],
        # 开奖活动名
        'lotteryGameName': lotteryres['lotteryGameName'],
        # 开奖时间
        'lotteryDrawTime': lotteryres['lotteryDrawTime'],
        # 中奖等级
        'lotteryDrawLevel': '未中奖',
        # 中奖金额
        'lotteryDrawTime': '未中奖'
    }

    # 中奖情况
    redBallEx = num[0:14].replace(' ','|')
    blueBallEx = num[15:20].replace(' ','|')
    redPattern = re.compile(redBallEx)
    bluePattern = re.compile(redPattern)
    redRes = redPattern.findall(lotteryres['lotteryDrawResult'][0:14])
    blueRes = bluePattern.findall(lotteryres['lotteryDrawResult'][15:20])
    patterns = ['5&2','5&1','5&0','4&2','4&1','3&2','4&0','3&1|2&2','3&0|1&2|2&1|0&2']
    levels = ['一等奖','二等奖','三等奖','四等奖','五等奖','六等奖','七等奖','八等奖','九等奖']
    bonus = ['一千万','500万','10000','3000','300','200','100','15','5']
    finalRes = '{0}&{1}'.format(len(redRes), len(blueRes))
    for i in range(len(patterns)):
        iRes = re.search(patterns[i], finalRes)
        if iRes is not None:
            result['lotteryDrawLevel'] = levels[i]
            result['lotteryDrawBonus'] = '{0}元'.format(bonus[i])
            print(json.dumps(result,indent=1))
            break
    print(json.dumps(result,indent=1))
    return result

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

for i in range(len(user_ids)):
    checkInMessage, timeStr = check_in()
    ckUTCTime = datetime.utcfromtimestamp(int(timeStr) / 1000)
    ckTime = ckUTCTime.astimezone(timezone(timedelta(hours = 8)))
    checkinTime = ckTime.strftime("%Y-%m-%d %H:%M:%S")
    leftDays = get_leftdays()
    lotteryRes = get_lotteryres(lotteryNums[0])
    data = {
        "checkInMessage": {
                   "value":checkInMessage,
                   "color":"#173177"
               },
        "checkinTime": {
                   "value": checkinTime,
                   "color":"#173177"
               },
        "leftDays": {
                   "value":int(float(leftDays)),
                   "color":"#173177"
               },
        "lotteryDrawNum": {
                   "value": lotteryRes['lotteryDrawNum'],
                   "color":"#173177"
               },
        "lotteryDrawResult": {
                   "value": lotteryRes['lotteryDrawResult'],
                   "color":"#173177"
               },
        "lotteryGameName": {
                   "value": lotteryRes['lotteryGameName'],
                   "color":"#173177"
               },
        "lotteryDrawTime": {
                   "value": lotteryRes['lotteryDrawTime'],
                   "color":"#173177"
               },
        "lotteryDrawLevel": {
                   "value": lotteryRes['lotteryDrawLevel'],
                   "color":"#173177"
               },
        "lotteryDrawBonus": {
                   "value": lotteryRes['lotteryDrawBonus'],
                   "color":"#173177"
               },
        "messageTime": {
                   "value": datetime.now().astimezone(timezone(timedelta(hours = 8))).strftime("%Y-%m-%d %H:%M:%S"),
                   "color":"#173177"
               }
        }
    res = wm.send_template(user_ids[i], template_ids[i], data)
    print(res)

#GLaDOS签到成功，剩余{{leftDays.DATA}}天，签到时间：{{checkinTime.DATA}}，返回结果：{{checkInMessage.DATA}}

#{{lotteryGameName.DATA}}{{lotteryDrawNum.DATA}}期开奖
#开奖号码：{{lotteryDrawResult.DATA}}
#开奖时间：{{lotteryDrawTime.DATA}}
#中奖等级：{{lotteryDrawLevel.DATA}}
#中奖金额：{{lotteryDrawBonus.DATA}}

#推送时间：{{messageTime.DATA}}