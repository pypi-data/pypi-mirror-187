name='bilibili_joker'
# python setup.py sdist
# python setup.py bdist_wheel --universal
# twine check dist/*
# twine upload dist/*
class Joker:
    """
    ###############################
    ######   author: joker   ######
    ######   QQ: 524276169   ######
    ###############################

    findPhonePlace:参数手机号，获取手机号所在地址
    createProgressBar: create a progress bar,
        params:
            max_value[the end value]
            update_value[every epoch update value]
            sleep: whether to set a delay
    sendMessage:send message
        params:
            phone: you know
            message:the message you want send
        notice: remember to change your userid,account and password in the url
    quickAnswer:when you want to attack somebody,you can use this function
        params:
            interval: every interval time send a message
            filename: write the message you want to send into the file,and split it with enter,make sure that every line only have one message
    freeApi: some interesting free api demo
        mode:
            0: every day a sentence, no return value
            1: comfort somebody ,no return value
            2: according to the real time,the function will give a sentence, no return value
            3: save a pretty girl video named 1.mp4 in your file root path, no return value
    """

    def __init__(self):
        pass

    def findPhonePlace(self, number=None):
        from phone import Phone
        p = Phone()
        print(p.find(number))
        # pip install phone

    def createProgressBar(self, max_value, update_value, sleep=True):
        # pip install progressbar2
        import time
        import progressbar
        p = progressbar.ProgressBar()  # 实例化进度条
        max_value = max_value
        p.start(max_value)
        n = 0
        while n < 100:
            p.update(n)  # 更新
            n += update_value
            if sleep:
                time.sleep(0.1)
        p.finish()

    def sendMessage(self, phone, message):
        import requests
        url = f'http://47.105.48.125:8888/sms.aspx?action=send&userid=541&account=深度学习' \
              f'&password=123456&mobile={phone}&content=【萨维塔的小屋】您的验证码为: {message}（若非本人操作，请删除本短信）'
        resp = requests.post(url)
        print(resp.text)

    def quickAnswer(self, interval=0.5, filename=None):
        import time
        import random
        from pynput.keyboard import Key, Controller
        if filename:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            keyboard = Controller()
            choice = random.randint(0, len(lines) - 1)
            command = lines[choice].rstrip()
            keyboard.type(command)
            keyboard.press(Key.enter)
            time.sleep(self.interval)
        else:
            print("you don't select a file")
            return None

    def freeApi(self, mode=0, ip=None):
        import requests
        if mode == 0:
            # a single useless sentence
            resp = requests.get('https://v.api.aa1.cn/api/yiyan/index.php')
            text = resp.text.split('>')[1].split('<')[0]
            print(text)
        elif mode == 1:
            # when somebody feel sad,you should use this api to comfort him/her
            resp = requests.get('https://v.api.aa1.cn/api/api-wenan-anwei/index.php?type=json')
            text = resp.text.split(":")[1].split('"')[1]
            print(text)
        elif mode == 2:
            # according to the real time,it will return you different sentences
            resp = requests.get('https://v.api.aa1.cn/api/time-tx/index.php')
            print(eval(resp.text).get("nxyj"))
        elif mode == 3:
            # save a pretty girl video  (0o0)
            resp = requests.get('https://tucdn.wpon.cn/api-girl/index.php?wpon=json')
            url = 'https://' + eval(resp.text).get("mp4")[4:]
            url = url.split('\\')
            url = '/'.join(url)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61'
            }
            'https://tucdn.wpon.cn//api-girl//videos//83.mp4'
            resp = requests.get(url, headers=headers)
            with open('../../1.mp4', 'wb') as f:
                f.write(resp.content)
                print('视频保存完成')


# if __name__ == '__main__':
#     joker = Joker()
#     # joker.findPhonePlace(15383312439)
#     joker.createProgressBar(100,1)
#     # joker.sendMessage(15383312439, 'hello')
#     # joker.quickAnswer(0.5)
#     # joker.freeApi(mode=3)
#     # print(joker.__doc__)
