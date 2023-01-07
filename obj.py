# 存一些类用
import os
import threading
import time
import websockets
import json
import asyncio
import uuid
import traceback
import re


class logger:
    file = './log/' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.log'
    log = f'Logged from {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}' + '\n'
    level = 'info'

    def __init__(self, file=None, level='info'):
        if not os.path.isdir('./log'):
            os.mkdir('./log')
        if file:
            self.file = file
        self.level = level

    def __del__(self):
        f = open(self.file, 'w', encoding='utf-8')
        f.write(self.log)
        f.close()

    def info(self, t):
        self.log = self.log + f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] [INFO]: ' + t + '\n'
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] [INFO]: ' + t)

    def warn(self, t):
        self.log = self.log + f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] [WARN]: ' + t + '\n'
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] [INFO]: ' + t)

    def fatal(self, t):
        self.log = self.log + f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] [FATAL]: ' + t + '\n'
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] [INFO]: ' + t)

    def debug(self, t):
        if self.level == 'info':
            return
        self.log = self.log + f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] [DEBUG]: ' + t + '\n'
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] [INFO]: ' + t)


class group_info:
    id = 100001
    name = 'Group'
    memo = 'Memo'
    create_time = '1672502400'
    level = '1'
    member_count = '1'
    max_member_count = '200'

    def __init__(self,
                 id=100001,
                 name='Group',
                 memo='Memo',
                 create_time='1672502400',
                 level='1',
                 member_count='1',
                 max_member_count='200'
                 ):
        self.id = id
        self.name = name
        self.memo = memo
        self.create_time = create_time
        self.level = level
        self.member_count = member_count
        self.max_member_count = max_member_count


class friend_info:
    id = 10001
    mame = 'name'
    remark = 'remark'

    def __init__(self,
                 id=10001,
                 name='name',
                 remark='remark'
                 ):
        self.id = id
        self.name = name
        self.remark = remark


class sender:
    id = 10001
    nickname = 'nickname'
    sex = 'unknown'
    age = 105
    card = 'card'
    area = 'China'
    level = '0'
    role = 'member'
    title = 'title'

    def __init__(self,
                 user_id=10001,
                 nickname='nickname',
                 sex='unknown',
                 age=105,
                 card='card',
                 area='China',
                 level='0',
                 role='member',
                 title='title'
                 ):
        self.user_id = user_id
        self.nickname = nickname
        self.sex = sex
        self.age = age
        self.card = card
        self.area = area
        self.level = level
        self.role = role
        self.title = title


class Message:
    send_time = '1672502400'
    self_id = 10001
    group_id = 100001
    message_type = 'private'
    sub_type = 'friend'
    message_id = 1
    user_id = 10001
    message = 'message'
    raw_message = 'message'
    font = 0
    temp_source = 0

    def __init__(self,
                 send_time='1672502400',
                 self_id=10001,
                 group_id=100001,
                 message_type='private',
                 sub_type='friend',
                 message_id=1,
                 user_id=10001,
                 message='message',
                 raw_message='message',
                 font=0,
                 temp_source=0,
                 sender=None,
                 reply=None
                 ):
        self.sender = sender
        self.send_time = send_time
        self.self_id = self_id
        self.group_id = group_id
        self.message_type = message_type
        self.sub_type = sub_type
        self.message_id = message_id
        self.user_id = user_id
        self.message = message
        self.raw_message = raw_message
        self.font = font
        self.temp_source = temp_source
        self._reply = reply

    def reply(self, message):
        if self.message_type == 'private':
            return self._reply(self.user_id, message)
        else:
            return self._reply(self.group_id, message)


class Notice:
    js = {}  # 原始json
    send_time = 1672502400  # 操作时间戳
    group_id = 100001  # 统一来源群ID
    self_id = 10001  # 统一机器人ID
    notice_type = 'None'
    sub_type = 'None'
    operator_id = 10002  # 统一操作者ID
    user_id = 10001  # 统一被操作者ID
    message_id = 0  # 撤回消息ID
    # file = file()             # file对象
    duration = 1
    sender_id = 10002  # 原则上与operator_id一致
    target_id = 10001  # 原则上与user_id一致
    honor_type = 'talkative'  # 荣誉称号，龙王之类的
    title = 'Title'  # 群头衔
    card_old = 'card_old'  # 原群名片
    card_new = 'card_new'  # 新群名片
    # client = Device()     # 客户端信息
    online = True
    comment = 'comment'  # 验证消息
    flag = 'flag'  # 请求 flag, 在调用处理请求的 API 时需要传入

    def __init__(self,
                 js,
                 send_time=1672502400,
                 group_id=100001,
                 self_id=10001,
                 notice_type='None',
                 sub_type='None',
                 operator_id=10002,
                 user_id=10001,
                 message_id=0,
                 duration=1,
                 sender_id=10002,
                 target_id=10001,
                 honor_type='talkative',
                 title='Title',
                 card_old='card_old',
                 card_new='card_new',
                 online=True,
                 comment='comment',
                 flag='flag'
                 ):
        self.js = js
        self.send_time = send_time
        self.group_id = group_id
        self.self_id = self_id
        self.notice_type = notice_type
        self.sub_type = sub_type
        self.operator_id = operator_id
        self.user_id = user_id
        self.message_id = message_id
        if sub_type == 'group_upload':
            self.file = file(id=js['file']['id'], name=js['file']['name'], size=js['file']['size'],
                             busid=js['file']['busid'])
        if sub_type == 'offline_file':
            self.file = file(id=js['file']['id'], name=js['file']['name'], size=js['file']['size'],
                             url=js['file']['url'])
        self.duration = duration
        self.sender_id = sender_id
        self.target_id = target_id
        self.honor_type = honor_type
        self.title = title
        self.card_old = card_old
        self.card_new = card_new
        if sub_type == 'client_status':
            self.client = Device(appid=js['client'], device_kind=js['client']['device_kind'],
                                 device_name=js['client']['device_name'])
            self.online = online
        self.comment = comment
        self.flag = flag


class Device:
    app_id = 1001
    device_name = 'device_name'  # 设备名称
    device_kind = 'device_kind'  # 类型

    def __init__(self, appid=1001, device_name='device_name', device_kind='device_kine'):
        self.app_id = appid
        self.device_kind = device_kind
        self.device_name = device_name


class file:
    id = 'FileID'
    name = 'File'
    size = 1
    busid = 1
    url = 'http://File.Url'

    def __init__(self,
                 id='FileID',
                 name='File',
                 size=1,
                 busid=1,
                 url='http://File.Url'
                 ):
        self.id = id
        self.name = name
        self.size = size
        self.busid = busid
        self.url = url


class Request:
    user_id = 10001
    group_id = 100001
    sub_type = 'unknown'
    comment = 'comment'
    flag = 'flag'
    n_type = 'friend'

    def __init__(self,
                 user_id=10001,
                 group_id=100001,
                 sub_type='unknown',
                 comment='comment',
                 flag='flag',
                 reply=None,
                 n_type='friend'
                 ):
        self.user_id = user_id
        self.group_id = group_id
        self.sub_type = sub_type
        self.comment = comment
        self.flag = flag
        self._reply = reply
        self.n_type = n_type

    def reply(self, approve: bool, remark="", reason=""):
        """
        快速处理request
        :param remark: 如果是好友申请，在同意时可以备注好友
        :param reason: 如果拒绝群申请，这里为拒绝原因，默认空
        :param approve: 是否通过/允许
        :return:
        """
        if self.n_type == 'friend':
            self._reply(self.flag, approve, remark=remark)
        elif self.n_type == 'group':
            self._reply(self.flag, self.sub_type, approve, reason=reason)


class reg:
    reg_list = {
        'apps': [
            # {'re': '(.*)', 'func': <function func at 0x0000000000000000>}
        ],
        'notice': [
            # {'func': <function func at 0x0000000000000000>}
        ],
        'noticeApps': [
            # {'type': 'poke', 'func': <function func at 0x0000000000000000>}
        ],
        'request': [
            # {'func': <function func at 0x0000000000000000>}
        ],
        'Apps': [
            # Bot 启动成功后在多线程调用
            # <function func at 0x0000000000000000>
        ],
        'msgApp': [
            # <function func at 0x0000000000000000>
        ]
    }

    def register(self, func_tri):
        def wapper(func):
            def _wapper(*args, **kwargs):
                return func(*args, **kwargs)  # 实际上不会被调用，运行不到这一步

            self.reg_list['apps'].append({'re': func_tri, 'func': func})
            return _wapper

        return wapper

    def registerNotice(self, func):
        def wapper(*args, **kwargs):
            return func(*args, **kwargs)  # 实际上不会被调用，运行不到这一步

        self.reg_list['notice'].append({'func': func})
        return wapper

    def registerNoticeApp(self, notice_type):
        def wapper(func):
            def _wapper(*args, **kwargs):
                return func(*args, **kwargs)  # 实际上不会被调用，运行不到这一步

            self.reg_list['noticeApps'].append({'type': notice_type, 'func': func})
            return _wapper

        return wapper

    def registerRequest(self, func):
        def wapper(*args, **kwargs):
            return func(*args, **kwargs)  # 实际上不会被调用，运行不到这一步

        self.reg_list['request'].append({'func': func})
        return wapper

    def registerRequestApp(self, notice_type):
        def wapper(func):
            def _wapper(*args, **kwargs):
                return func(*args, **kwargs)  # 实际上不会被调用，运行不到这一步

            self.reg_list['requestApps'].append({'type': notice_type, 'func': func})
            return _wapper

        return wapper

    def registerMessage(self, func):
        self.reg_list['msgApp'].append(func)

    def registerEvent(self, func):
        self.reg_list['Apps'].append(func)


class BotWebsocket:
    ws_url = 'ws://127.0.0.1:6700'
    bot = {
        'id': 10001,
        'name': 'Bot',
    }
    msg = {}
    logger = logger()
    recv_api = {}
    group_list = {}
    friend_list = {}
    reg = reg()

    def __init__(self, url, ):
        self.ws_url = url

    def _run(self):
        try:
            self.loop = asyncio.get_event_loop()
            t = self.loop.create_task(self._runWebsocket())
            self.loop.run_until_complete(t)
            # self.loop.run_forever()
        except KeyboardInterrupt as kb:
            self.logger.info('Shutting Down!')
            self.logger.__del__()

    def stop(self):
        self.loop.stop()

    async def _runWebsocket(self):
        while True:
            async with websockets.connect(self.ws_url) as self.ws:
                threading.Thread(target=self._Bot_init).start()
                while True:
                    try:
                        res = await self.ws.recv()
                        threading.Thread(target=self._jsonParse, args=(res,)).start()  # 多线程防止堵塞
                    except (Exception, BaseException) as e:
                        print(traceback.format_exc())
                        time.sleep(5)

    async def _sendWebsocket(self, data):
        await self.ws.send(data)

    def _Bot_init(self):
        def get_group_list():  # get_group_list
            id = f'{uuid.uuid1()}'
            data = {'action': 'get_group_list', 'params': {}, 'echo': id}
            ret = self._send_data(data, id)
            gl = ret['data']
            for i in gl:
                gi = group_info(
                    id=i['group_id'],
                    name=i['group_name'],
                    create_time=i['group_create_time'],
                    level=i['group_level'],
                    member_count=i['member_count'],
                    max_member_count=i['max_member_count']
                )
                self.group_list[i['group_id']] = gi
            self.logger.info(f'获取到群列表，共 {len(self.group_list)} 个。')

        def get_friend_list():
            id = f'{uuid.uuid1()}'
            data = {'action': 'get_friend_list', 'params': {}, 'echo': id}
            ret = self._send_data(data, id)
            fl = ret['data']
            for i in fl:
                fi = friend_info(
                    id=i['user_id'],
                    name=i['nickname'],
                    remark=i['remark']
                )
                self.friend_list[i['user_id']] = fi
            self.logger.info(f'获取到好友列表，共 {len(self.friend_list)} 个。')

        def get_gocq_ver():
            id = f'{uuid.uuid1()}'
            data = {'action': 'get_version_info', 'params': {}, 'echo': id}
            ret = self._send_data(data, id)
            self.logger.info('当前使用GO-CQHTTP版本：' + ret['data']['app_version'])

        self.logger.info('Bot.py开始初始化期间功能可能不完整。')
        get_gocq_ver()
        get_group_list()
        get_friend_list()

        # 以下是初始化代码
        self.logger.info('Bot.py初始化完成。')

        # 启动线程App
        err = []
        i = None
        try:
            for i in self.reg.reg_list['Apps']:
                threading.Thread(target=i).start()
        except Exception as e:
            err.append({'func': i, 'error': traceback.format_exc(), 'except': e})
        if len(err) > 0:
            print(f"在启动子程序时，共有{len(self.reg.reg_list['Apps'])}个子程序，启动失败{len(err)}个。")
            for i in err:
                print(f"在启动子程序{i['func']}时发生错误，错误类型：{i['except']}。")
                print(i['error'])
        else:
            print(f"在启动子程序时，共有{len(self.reg.reg_list['Apps'])}个子程序，已全部启动成功。")

    def _jsonParse(self, t):
        # 事件分拣
        try:
            js = json.loads(t)
            if 'echo' in js:
                # 回声，API响应数据
                self._ret_api(js['echo'], js)
                return
            post_type = js['post_type']
            self.bot[id] = int(js['self_id'])
            if post_type == 'message':  # 消息事件
                self._message(js)
            if post_type == 'request':
                self._request(js)
            if post_type == 'notice':
                self._notice(js)
            if post_type == 'meta_event':
                self._meta(js)
        except (Exception, BaseException) as e:
            print(traceback.format_exc())
            time.sleep(5)

    def _ret_api(self, echo, js):
        # print(js)
        self.recv_api[echo] = {'recv': True, 'data': js['data']}

    def _message(self, js: dict):
        msg_type = js['message_type']
        if msg_type == 'private':
            self.logger.info(
                f'收到好友 {js["sender"]["nickname"]}({js["sender"]["user_id"]}) 的消息： {js["message"]} ({js["message_id"]})')
            _sender = sender(
                user_id=js["sender"]["user_id"],
                nickname=js["sender"]['nickname'],
                sex=js["sender"]['sex'],
                age=js["sender"]['age'],
                # card=js["sender"]['card'],
                # area=js["sender"]['area'],
                # level=js["sender"]['level'],
                # role=js["sender"]['role'],
                # title=js["sender"]['title']
            )
            message = Message(
                send_time=js['time'],
                self_id=js['self_id'],
                message_type=js['message_type'],
                sub_type=js['sub_type'],
                message_id=js['message_id'],
                user_id=js['user_id'],
                message=js['message'],
                raw_message=js['raw_message'],
                font=js['font'],
                sender=_sender,
                reply=self._send_private_msg
            )
            self.msg[js['message_id']] = message

            for i in self.reg.reg_list['msgApp']:
                i(message)

            for i in self.reg.reg_list['apps']:
                if re.match(i['re'], js["message"]):
                    i['func'](message)
        if msg_type == 'group':
            self.logger.info(
                f'收到群 {self.group_list[js["group_id"]].name}({js["group_id"]}) 内 {js["sender"]["nickname"]}({js["sender"]["user_id"]}) 的消息： {js["message"]} ({js["message_id"]})')
            _sender = sender(
                user_id=js["sender"]["user_id"],
                nickname=js["sender"]['nickname'],
                sex=js["sender"]['sex'],
                age=js["sender"]['age'],
                card=js["sender"]['card'],
                area=js["sender"]['area'],
                level=js["sender"]['level'],
                role=js["sender"]['role'],
                title=js["sender"]['title']
            )
            message = Message(
                send_time=js['time'],
                self_id=js['self_id'],
                group_id=js["group_id"],
                message_type=js['message_type'],
                sub_type=js['sub_type'],
                message_id=js['message_id'],
                user_id=js['user_id'],
                message=js['message'],
                raw_message=js['raw_message'],
                font=js['font'],
                sender=_sender,
                reply=self._send_group_msg
            )
            self.msg[js['message_id']] = message

            for i in self.reg.reg_list['msgApp']:
                i(message)

            for i in self.reg.reg_list['apps']:
                if re.match(i['re'], js["message"]):
                    i['func'](message)

    def _notice(self, js: dict):
        if js['notice_type'] == 'friend_recall':
            # 私聊消息撤回
            self.logger.info(
                f'好友 {js["user_id"]} 撤回了消息：{self.msg[js["message_id"]].message} ({js["message_id"]})')
        if js['notice_type'] == 'group_recall':
            # 群聊消息撤回
            self.logger.info(
                f'{js["user_id"]} 在群 {self.group_list[js["group_id"]].name}({js["group_id"]}) 撤回了消息：'
                f'{self.msg[js["message_id"]].message} ({js["message_id"]})')
        if js['notice_type'] == 'group_increase':
            # 群成员增加
            if js['sub_type'] == 'approve':
                self.logger.info(f'管理员 {js["operator_id"]} 已同意 {js["user_id"]} 加入群 '
                                 f'{self.group_list[js["group_id"]].name}({js["group_id"]})')
            elif js['sub_type'] == 'invite':
                self.logger.info(f'管理员 {js["operator_id"]} 邀请 {js["user_id"]} 加入群 '
                                 f'{self.group_list[js["group_id"]].name}({js["group_id"]})')
        if js['notice_type'] == 'group_decrease':
            # 群成员减少
            if js['sub_type'] == 'leave':
                self.logger.info(f'成员 {js["user_id"]} 离开群 '
                                 f'{self.group_list[js["group_id"]].name}({js["group_id"]})')
            if js['sub_type'] == 'kick':
                self.logger.info(f'管理员 {js["operator_id"]} 将 {js["user_id"]} 踢出群 '
                                 f'{self.group_list[js["group_id"]].name}({js["group_id"]})')
            if js['sub_type'] == 'kick_me':
                self.logger.warn(f'管理员 {js["operator_id"]} 将 自己{js["user_id"]} 踢出群 '
                                 f'{self.group_list[js["group_id"]].name}({js["group_id"]})')
        if js['notice_type'] == 'group_admin':
            # 群管理变动
            if js['sub_type'] == 'set':
                self.logger.info(f'{js["user_id"]} 成为群 '
                                 f'{self.group_list[js["group_id"]].name}({js["group_id"]}) 的管理员')
            if js['sub_type'] == 'unset':
                self.logger.info(f'{js["user_id"]} 被取消群 '
                                 f'{self.group_list[js["group_id"]].name}({js["group_id"]}) 的管理员')
        if js['notice_type'] == 'group_upload':
            # 群文件上传
            self.logger.info(f'{js["user_id"]} 在群 {self.group_list[js["group_id"]].name}({js["group_id"]}) 上传文件 '
                             f'file={js["file"]}')
        if js['notice_type'] == 'group_ban':
            # 群禁言
            if js["user_id"] == 0:
                self.logger.info(f'群 {self.group_list[js["group_id"]].name}({js["group_id"]}) 开启全群禁言 '
                                 f'，操作人{js["operator_id"]} ({js["duration"]})')
            else:
                self.logger.info(
                    f'{js["user_id"]} 在群 {self.group_list[js["group_id"]].name}({js["group_id"]}) 被禁言 '
                    f'{js["duration"]}秒，操作人{js["operator_id"]}')
        if js['notice_type'] == 'friend_add	':
            # 好友已添加
            self.logger.info(f'{js["user_id"]} 已添加为好友。')
        if js['notice_type'] == 'poke':
            # 戳一戳（群内&好友）
            if len(js) == 8:  # 好友
                self.logger.info(f'{js["user_id"]} 戳了戳自己({js["target_id"]})')
            else:
                self.logger.info(
                    f'{js["user_id"]} 在群 {self.group_list[js["group_id"]].name}({js["group_id"]}) 戳了戳 '
                    f'{js["target_id"]}')
        if js['notice_type'] == 'lucky_king':
            # 群红包运气王提示
            self.logger.info(f'{js["user_id"]} 在群 {self.group_list[js["group_id"]].name}({js["group_id"]}) 发送的红包'
                             f'的运气王为 {js["target_id"]}')
        if js['notice_type'] == 'honor':
            # 群成员荣誉变更提示
            if js['honor_type'] == 'talkative':
                self.logger.info(f'{js["user_id"]} 在群 {self.group_list[js["group_id"]].name}({js["group_id"]}) 成为'
                                 f'龙王')
            if js['honor_type'] == 'performer':
                self.logger.info(f'{js["user_id"]} 在群 {self.group_list[js["group_id"]].name}({js["group_id"]}) 获得'
                                 f'群聊之火')
            if js['honor_type'] == 'emotion':
                self.logger.info(f'{js["user_id"]} 在群 {self.group_list[js["group_id"]].name}({js["group_id"]}) 获得'
                                 f'快乐源泉')
        if js['notice_type'] == 'title':
            # 群成员头衔变更
            self.logger.info(f'{js["user_id"]} 在群 {self.group_list[js["group_id"]].name}({js["group_id"]}) 获得头衔'
                             f'{js["title"]}')
        if js['notice_type'] == 'group_card':
            # 群成员名片更新
            self.logger.info(f'{js["user_id"]} 在群 {self.group_list[js["group_id"]].name}({js["group_id"]}) 更新群名片'
                             f'从 {js["card"]}')
        if js['notice_type'] == 'offline_file':
            # 接收到离线文件
            self.logger.info(f'{js["user_id"]} 在群 {self.group_list[js["group_id"]].name}({js["group_id"]}) 上传文件 '
                             f'url={js["url"]}')
        if js['notice_type'] == 'client_status':
            # 其他客户端在线状态变更
            if js['online']:
                self.logger.info(f'账号在{js["device_name"]}({js["device_kind"]}) 上登陆。')
            else:
                self.logger.info(f'账号在{js["device_name"]}({js["device_kind"]}) 上登陆。')
        if js['notice_type'] == 'essence':
            # 精华消息变更
            if js["sub_type"] == 'add':
                self.logger.info(
                    f'{js["operator_id"]} 在群 {self.group_list[js["group_id"]].name}({js["group_id"]}) 设置'
                    f'精华消息= {js["message_id"]}')
            else:
                self.logger.info(
                    f'{js["operator_id"]} 在群 {self.group_list[js["group_id"]].name}({js["group_id"]}) 取消'
                    f'精华消息= {js["message_id"]}')

        if len(self.reg.reg_list['notice']) > 0:
            for i in self.reg.reg_list['notice']:
                i['func'](js)
        if len(self.reg.reg_list['noticeApps']) > 0:
            for i in self.reg.reg_list['noticeApps']:
                if js['notice_type'] == i['type']:
                    i['func'](js)

    def _request(self, js: dict):
        if js['request_type'] == 'friend':
            request = Request(
                user_id=js['user_id'],
                comment=js['comment'],
                flag=js['flag'],
                reply=self._set_friend_add_request,
                n_type='friend')
            for i in self.reg.reg_list['request']:
                i['func'](request)
            self.logger.info(f'{js["user_id"]} 想添加您为好友。')
        if js['request_type'] == 'group':
            request = Request(
                group_id=js['group_id'],
                sub_type=js['sub_type'],
                user_id=js['user_id'],
                comment=js['comment'],
                flag=js['flag'],
                reply=self._set_group_add_request,
                n_type='group')
            if js['sub_type'] == 'add':
                self.logger.info(f'{js["user_id"]} 想加入群 {self.group_list[js["group_id"]].name}({js["group_id"]})。')
            elif js['sub_type'] == 'invite':
                self.logger.info(
                    f'{js["user_id"]} 想邀请自己加入群 {self.group_list[js["group_id"]].name}({js["group_id"]})。')
            for i in self.reg.reg_list['request']:
                i['func'](request)

    def _meta(self, js: dict):
        self.logger.debug(f'收到meta：{js}')

    def _send_data(self, data, id):
        # 发包，取响应数据
        asyncio.run(self._sendWebsocket(json.dumps(data)))
        while True:
            if id in self.recv_api:
                ret = self.recv_api[id]
                del self.recv_api[id]
                return ret
            time.sleep(0.001)

    def _send_data_no_ret(self, data):
        # 发包，没有响应
        asyncio.run(self._sendWebsocket(json.dumps(data)))

    def send_data(self, data: dict):
        # 发包，取响应数据
        id = f'{uuid.uuid1()}'
        if "echo" in data:
            id = data["echo"]
        else:
            data["echo"] = id
        return self._send_data(data, id)
        # asyncio.run(self._sendWebsocket(json.dumps(data)))
        # while True:
        #     if id in self.recv_api:
        #         ret = self.recv_api[id]
        #         del self.recv_api[id]
        #         return ret
        #     time.sleep(0.01)

    def _send_group_msg(self, group_id, message):
        id = f'{uuid.uuid1()}'
        sdata = {'action': 'send_group_msg', 'params': {'group_id': int(group_id), 'message': message}, 'echo': id}
        return self._send_data(sdata, id)

    def _send_private_msg(self, user_id, message):
        id = f'{uuid.uuid1()}'
        sdata = {'action': 'send_private_msg', 'params': {'user_id': int(user_id), 'message': message}, 'echo': id}
        return self._send_data(sdata, id)

    def _set_friend_add_request(self, flag, approve=True, remark=""):
        sdata = {'action': 'set_friend_add_request',
                 'params': {'flag': flag, 'approve': approve, 'remark': remark}}
        self._send_data_no_ret(sdata)

    def _set_group_add_request(self, flag, sub_type, approve=True, reason=""):
        sdata = {'action': 'set_group_add_request',
                 'params': {'flag': flag, 'sub_type': sub_type, 'approve': approve, 'reason': reason}}
        self._send_data_no_ret(sdata)