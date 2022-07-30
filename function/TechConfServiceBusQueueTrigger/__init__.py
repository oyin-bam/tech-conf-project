from lib2to3.pytree import Base
import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from . import config

def main(msg: func.ServiceBusMessage):

    print(msg)

    notification_id = int(msg.get_body().decode('utf-8'))
    

    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    conn = psycopg2.connect(user=config.BaseConfig.POSTGRES_USER,
                                  password=config.BaseConfig.POSTGRES_PW,
                                  host=config.BaseConfig.POSTGRES_URL,
                                  port=config.BaseConfig.POSTGRES_PORT,
                                  database=config.BaseConfig.POSTGRES_DB)
    try:
       
        cur = conn.cursor()

        notificationQuery = "SELECT subject, message FROM notification WHERE id={}".format(notification_id)

        cur.execute(notificationQuery)
        notifications = cur.fetchone()
        print(notifications)


        cur.execute("SELECT first_name, last_name, email FROM attendee")
        attendees = cur.fetchall()

        for attendee in attendees:
            personalized_message = notifications[1] + " " + attendee[0] + " " + attendee[1]
            email = attendee[2]

            send_email(email, notifications[0], personalized_message)
        

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        updatedStatus = "notified {no_of_attendees} attendees".format(no_of_attendees=len(attendees))
        updatedCompletedDate = datetime.utcnow()

        updateQuery = """ UPDATE notification
                SET status = %s, completed_date = %s
                WHERE id=%s"""

        cur.execute(updateQuery, (updatedStatus,updatedCompletedDate,notification_id))
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Failed to connect to the database, error")
        print(error)
        logging.error(error)
    finally:
        if (conn):
            # TODO: Close connection
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")


## Logic test --- [without running azure function]
# def test(notification_id):

#     logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

#     # TODO: Get connection to database
#     conn = psycopg2.connect(user=BaseConfig.POSTGRES_USER,
#                                   password=BaseConfig.POSTGRES_PW,
#                                   host=BaseConfig.POSTGRES_URL,
#                                   port=BaseConfig.POSTGRES_PORT,
#                                   database=BaseConfig.POSTGRES_DB)
#     try:
       
#         cur = conn.cursor()

#         cur.execute("SELECT subject, message FROM notification where id={id}".format(id=notification_id))
#         notifications = cur.fetchone()
#         print(notifications)


#         cur.execute("SELECT first_name, last_name, email FROM attendee")
#         attendees = cur.fetchall()

#         for attendee in attendees:
#             personalized_message = notifications[1] + " " + attendee[0] + " " + attendee[1]
#             email = attendee[2]

#             send_email(email, notifications[0], personalized_message)
        

#         # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
#         updatedStatus = "notified {no_of_attendees} attendees".format(no_of_attendees=len(attendees))
#         updatedCompletedDate = datetime.now()

#         updateQuery = """ UPDATE notification
#                 SET status = %s
#                 WHERE completed_date = %s"""

#         cur.execute(updateQuery, (updatedStatus, updatedCompletedDate, notification_id))
#         conn.commit()

#     except (Exception, psycopg2.DatabaseError) as error:
#         print("Failed to connect to the database, error")
#         logging.error(error)
#     finally:
#         if (conn):
#             # TODO: Close connection
#             cur.close()
#             conn.close()
#             print("PostgreSQL connection is closed")



def send_email(email, subject, message):
    print(email, subject, message)
    """ send email to attendees """
    sg = SendGridAPIClient(api_key=config.BaseConfig.SENDGRID_API_KEY)
    from_email = Email('harjacober@gmail.com')
    to_email = To(email)
    subject = subject
    content = Content("text/plain", message)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)