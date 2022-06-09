from pyfcm import FCMNotification

API_KEY = "AAAAqB2QRB0:APA91bHO0EqAVZiDN7bqlzgLDe_15z0IqghN-OgFS3UH3DnSxiax5h_70ohg02VJccHLYQ2nWaXrtN3B2M01Lyxp1dmz8fwAqpbKcUuWQjHouXH_4yusHc-kLIDGfbIF_EdP3TNTRAWM"
push_service = FCMNotification(api_key=API_KEY)

def sendNotification(topic, title, body, img_url):
    try:
        push_service.notify_topic_subscribers(
            topic_name=topic,
            message_body=body,
            message_title=title,
            extra_notification_kwargs={
                "image": img_url
            }
        )
    except Exception as e:
        print(e)