from skygear.transmitter.encoding import deserialize_record
from skygear.action import push_users
from skygear.container import SkygearContainer
from skygear.options import options as skyoptions
from skygear.utils.context import current_user_id
from chat.decorators import *

@after_message_sent
def after_message_sent_hook(message, conversation, participants):
    container = SkygearContainer(api_key=skyoptions.masterkey,
                                 user_id=current_user_id())
    message = deserialize_record(message)
    conversation = deserialize_record(conversation)
    participants = [deserialize_record(p) for p in participants]
    other_user_ids = [p.id.key for p in participants if p != current_user_id()]
    current_user = [p for p in participants if p.id.key == current_user_id()][0]
    content = ''
    if 'body' in message:
        content = current_user['username'] + ": " + message['body']
    else:
        content = current_user['username'] + " sent you a file."
    notification = {'gcm': {
                       'notification': {
                           'title': conversation['title'],
                           'body': content
                       }
                    },
                    'apns': {
                        'aps': {
                            'alert': {
                                'title': conversation['title'],
                                'body': content
                            },
                            'from': 'skygear',
                            'operation': 'notification'
                        }
                    }
                   }
    push_users(container, other_user_ids, notification)
