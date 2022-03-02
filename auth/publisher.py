from aio_pika import connect, Message
import json
from .crud import get_password_hash

async def publisher(message,subject,url):
    '''This function is used to publish message to rabbitmq.

            Parameters:
                message: A Dictionary,
                        contains message to be published.
                subject: A String,
                         subject of message.
                url: A String,
                     url of message will received by user.

            Returns:
                None
    '''
    # Perform connection
    connection = await connect(
        "amqp://user:example@192.168.63.26"
    )

    message['subject']=subject
    message['url']='http://192.168.96.250:8000'+url
    print(json.dumps(message).encode('utf-8'))

    # connection = await connect(
    #     "amqp://guest:guest@localhost"
    # )
   
    # Creating a channel
    channel = await connection.channel()


    # Sending the message
    await channel.default_exchange.publish(
        Message(json.dumps(message).encode('utf-8'),headers={'APIKey':get_password_hash('admin')}),
        routing_key="email"
    )


    print('User Authentication info sent.')

    await connection.close()


