from firebase_admin import messaging
import traceback
import json
from auth_login.models import MyUser
from django.conf import settings
from auth_login.models import Notification
from order_cart.models import ProductOrder,ServiceOrder

class NotificationsHelper:
    
    # Method to send messages to FCM
    @classmethod
    def __sendMessage(cls, msg: messaging.Message):
        try:
            
            response = messaging.send(message=msg, dry_run=False)
          
        except Exception as exc:
          
            print(traceback.format_exc())

    # Method to create a message with localized data
    @classmethod
    def __localizedMsg(cls, title: str, body: str, titleArgs: list[str] = [], bodyArgs: list[str] = [], data: dict = {}):
        # Create message payload with both data and notification
        msg = messaging.Message(
            data={
                **data,
                'title': title,
                'titleArgs': json.dumps(titleArgs),
                'body': body,
                'bodyArgs': json.dumps(bodyArgs),
                'localized': str(True)
            },
            android=messaging.AndroidConfig(
                notification=messaging.AndroidNotification(
                    title_loc_key=title,
                    title_loc_args=titleArgs,
                    body_loc_key=body,
                    body_loc_args=bodyArgs
                )
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        alert=messaging.ApsAlert(
                            title_loc_key=title,
                            title_loc_args=titleArgs,
                            loc_key=body,
                            loc_args=bodyArgs
                        )
                    )
                )
            ),
            notification=messaging.Notification(
                title=title,
                body=body
            )
        )
        return msg
    #send not localized notification to topic
    #! this function currently for test, don't use it in the dashboard for now :) 
    @classmethod
    def sendBroadcast(cls,title,body,topic):
        data={
            'type':"BROADCAST",
            'localized':str(False)

        }
        msg=messaging.Message(

                    notification=messaging.Notification(
                        title=title,
                        body=body,

                    ),
                    topic=topic,
                    data=data,
                    )
        cls.__sendMessage(msg)

    @classmethod
    def sendProductOrderUpdates(cls,update:str,order:ProductOrder,target:MyUser):
          data={
            'type':"Product_Updates",
            "order-id":str(order.id),
            'update':update
        }
          bodyArgs=[str(order.id)]
          msg=cls.__localizedMsg( title=update+'_TITLE',
                                body=update+'_BODY',
                                bodyArgs=bodyArgs,
                                data=data,
                                )
          if target.fcm_token:
            msg.token=target.fcm_token
            cls.__sendMessage(msg)
            Notification.objects.create(
                                    title=update+'_TITLE',
                                    body=update+'_BODY',
                                    bodyArgs=bodyArgs,
                                    localized=True,
                                    user=target,
                                    )
            
    @classmethod
    def sendServiceOrderUpdates(cls,update:str,order:ServiceOrder,target:MyUser):
          data={
            'type':"Service_Updates",
            "order-id":str(order.id),
            'update':update
        }
          bodyArgs=[str(order.id)]
          msg=cls.__localizedMsg( title=update+'_TITLE',
                                body=update+'_BODY',
                                bodyArgs=bodyArgs,
                                data=data,
                                )
          if target.fcm_token:
            msg.token=target.fcmToken
            cls.__sendMessage(msg)
            Notification.objects.create(
                                    title=update+'_TITLE',
                                    body=update+'_BODY',
                                    bodyArgs=bodyArgs,
                                    localized=True,
                                    user=target,
                                    )


    @classmethod
    def sendMessage(cls,title:str,update:str,target:MyUser):
        data={
            'type':title,
            'update':update
        }
        
        bodyArgs=[]
        msg=cls.__localizedMsg( title=title+'_TITLE',
                                body=update+'_BODY',
                                bodyArgs=bodyArgs,
                                data=data,
                                )
        
        if target.fcm_token:
            msg.token=target.fcm_token
            cls.__sendMessage(msg)
            Notification.objects.create(
                                    title=update+'_TITLE',
                                    body=update+'_BODY',
                                    bodyArgs=bodyArgs,
                                    localized=True,
                                    user=target,
                                    )
    
class OrdersUpdates:
    PROVIDER_ACCEPTED_PRODUCT_ORDER='PROVIDER_ACCEPTED_PRODUCT_ORDER'
    PROVIDER_ACCEPTED_SERVICE_ORDER='PROVIDER_ACCEPTED_SERVICE_ORDER'
    PROVIDER_REJECTED_PRODUCT_ORDER='PROVIDER_REJECTED_PRODUCT_ORDER'
    PROVIDER_REJECTED_SERVICE_ORDER='PROVIDER_REJECTED_SERVICE_ORDER'
    CLIENT_CANCEL_PRODUCT_ORDER='CLIENT_CANCEL_PRODUCT_ORDER'
    CLIENT_CANCEL_SERVICE_ORDER='CLIENT_CANCEL_SERVICE_ORDER'
    NEW_PORODUCT_ORDER='NEW_PORODUCT_ORDER' 
    NEW_SERVICE_ORDER='NEW_SERVICE_ORDER' 
    PRODUCT_COMPLATED='PRODUCT_COMPLATED'
    SERVICE_COMPLATED='SERVICE_COMPLATED'
    
