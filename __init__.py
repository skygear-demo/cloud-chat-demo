from skygear.transmitter.encoding import deserialize_record
from chat.hooks import *
from skygear.container import SkygearContainer
from skygear.options import options as skyoptions
from skygear.utils.context import current_context, current_user_id

def _get_container():
    return SkygearContainer(api_key=skyoptions.masterkey,
                            user_id=current_user_id())


def __send_to_user(user_ids, title, message):
    container = _get_container()
    n = {'gcm': {'notification': {'title': title, 'body': message}}}
    payload = {'user_ids': user_ids, 'notification': n}
    print(container.send_action('push:user', payload))


@after_message_sent
def after_message_sent_hook(message, conversation, participants):
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
    __send_to_user(other_user_ids, conversation['title'], content)
