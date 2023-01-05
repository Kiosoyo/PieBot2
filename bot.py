import obj
from obj import BotWebsocket


class bot(BotWebsocket):

    def __init__(self, ws_url):
        super().__init__(ws_url)

    def run(self):
        self._run()

    def send_group_msg(self, group_id, message):
        sdata = {'action': 'send_group_msg', 'params': {'group_id': int(group_id), 'message': message}}
        return self.send_data(sdata)

    def send_private_msg(self, user_id, message):
        sdata = {'action': 'send_private_msg', 'params': {'user_id': int(user_id), 'message': message}}
        return self.send_data(sdata)

    def send_msg(self, user_id: int = None, group_id: int = None, message_type: str = None, message=None):
        if not message_type:
            if group_id: message_type = 'group'
            if user_id: message_type = 'private'
            if not group_id and not user_id: return None
        if message_type == 'group':
            return self.send_group_msg(group_id, message)
        else:
            return self.send_private_msg(user_id, message)

    def delete_msg(self, message_id):
        sdata = {'action': 'delete_msg', 'params': {'message_id': int(message_id)}}
        return self.send_data(sdata)

    def mark_msg_as_read(self, message_id):
        sdata = {'action': 'mark_msg_as_read', 'params': {'message_id': int(message_id)}}
        return self.send_data(sdata)

    def set_group_kick(self, group_id, user_id, reject_add_request=False):
        sdata = {'action': 'set_group_kick', 'params': {'group_id': int(group_id), 'user_id': int(user_id),
                                                        'reject_add_request': reject_add_request}}
        return self.send_data(sdata)

    def set_group_ban(self, group_id, user_id, duration):
        sdata = {'action': 'set_group_ban',
                 'params': {'group_id': int(group_id), 'user_id': int(user_id), 'duration': duration}}
        return self.send_data(sdata)

    def get_group_info(self, group_id) -> obj.group_info:
        return self.group_list[int(group_id)]

    def get_friend_info(self, user_id) -> obj.friend_info:
        return self.friend_list[int(user_id)]

    def set_group_whole_ban(self, group_id, enable):
        sdata = {'action': 'set_group_whole_ban',
                 'params': {'group_id': int(group_id), 'enable': enable}}
        self._send_data_no_ret(sdata)

    def set_group_admin(self, group_id, user_id, enable):
        sdata = {'action': 'set_group_admin',
                 'params': {'group_id': int(group_id), 'user_id': user_id, 'enable': enable}}
        self._send_data_no_ret(sdata)

    def set_group_card(self, group_id, user_id, card):
        sdata = {'action': 'set_group_card',
                 'params': {'group_id': int(group_id), 'user_id': user_id, 'card': card}}
        self._send_data_no_ret(sdata)

    def set_group_name(self, group_id, group_name):
        sdata = {'action': 'set_group_card',
                 'params': {'group_id': int(group_id), 'group_name': group_name}}
        self._send_data_no_ret(sdata)

    def set_group_leave(self, group_id, is_dismiss=False):
        sdata = {'action': 'set_group_leave',
                 'params': {'group_id': int(group_id), 'is_dismiss': is_dismiss}}
        self._send_data_no_ret(sdata)

    def set_group_special_title(self, group_id, user_id, special_title):
        sdata = {'action': 'set_group_special_title',
                 'params': {'group_id': int(group_id), 'user_id': user_id, 'special_title': special_title}}
        self._send_data_no_ret(sdata)

    def send_group_sign(self, group_id):
        sdata = {'action': 'send_group_sign',
                 'params': {'group_id': int(group_id)}}
        self._send_data_no_ret(sdata)

    def set_friend_add_request(self, flag, approve=True, remark=""):
        sdata = {'action': 'set_friend_add_request',
                 'params': {'flag': flag, 'approve': approve, 'remark': remark}}
        self._send_data_no_ret(sdata)

    def set_group_add_request(self, flag, sub_type, approve=True, reason=""):
        sdata = {'action': 'set_group_add_request',
                 'params': {'flag': flag, 'sub_type': sub_type, 'approve': approve, 'reason': reason}}
        self._send_data_no_ret(sdata)

    def download_file(self, file_url, thread_count=1, headers=None):
        if headers is None:
            headers = []
        sdata = {'action': 'download_file',
                 'params': {'file_url': file_url, 'thread_count': thread_count, 'headers': headers}}
        return self.send_data(sdata)
