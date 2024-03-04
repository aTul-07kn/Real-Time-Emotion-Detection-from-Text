# First let's get jinja2
from jinja2 import Template
import os
import random
# We will need smtplib to connect to our smtp email server
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# contains emails of the customer executives along with their working logs 
executive_details=["teja.czechsolutions@gmail.com","anand.czechsolutions@gmail.com","walter.czechsolutions@gmail.com"]

def send_email(name, receiver_email, emotion):

    # Get the absolute path to the directory of this script
    script_directory = os.path.dirname(os.path.realpath(__file__))
    
    if emotion=="joy":
        # Construct the path to the joy email template within the Emailmodule folder
        template_path = os.path.join(script_directory, "email_templates", "joy_template.html")
        subject="Acknowledging Your Satisfaction and Elevating Your Positive Experience"

    elif emotion=='sadness' or emotion=='anger' or emotion=='fear':
        cust_care_email=random.choice(executive_details)
        # Construct the path to the unhappy email template within the Emailmodule folder
        template_path = os.path.join(script_directory, "email_templates", "unhappy_template.html")
        template_path_care = os.path.join(script_directory, "email_templates", "customercare_template.html")
        subject="Your Feedback Respected-Aiming for Swift Resolution" # subject for CUSTOMER
        subject_care=f"Emergency!! {name} need assistance" # subject for CUSTOMER CARE

        # Read the Jinja2 email template for CUSTOMER CARE
        with open(template_path_care, "r") as file:
            template_str_care = file.read()
        jinja_template_care = Template(template_str_care)

    # Read the Jinja2 email template for CUSTOMER
    with open(template_path, "r") as file:
        template_str = file.read()
    jinja_template = Template(template_str)

    # Define email server and credentials
    smtp_server = "smtp.gmail.com" #change smtp.server.com to smtp.gmail.com

    smtp_port = 587
    sender_email = "cezchsolutions@gmail.com"

    # generate the password by going to 2-step verification and create a new password for different apps as google has removed the access for third party websites like SMTP server
    sender_password = "fiot nkgv ummv fgco"

    # Set up email server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Create email content using Jinja2 template
    if emotion=='sadness' or emotion=='ager' or emotion=='fear':
        # --------------------------------------SENDING MAIL TO CUSTOMER--------------------------------------------------
        email_data = {
            "greeting": f"Hello {name}!",
            "sender_name": "Czech Unified Solutions"
        }

        email_content = jinja_template.render(email_data) # render CUSTOMER UNHAPPY TEMPLATE

        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email  #customer mail
        msg["Subject"] = subject

        # Attach the HTML content to the email
        msg.attach(MIMEText(email_content, "html"))

        # Print and send the email to customer
        print(f"Sent email to CUSTOMER {receiver_email}")
        server.sendmail(sender_email, receiver_email, msg.as_string())

        # Close the server connection for customer
        # server.quit()        

        # ---------------------------------SENDING MAIL TO CUSTOMER CARE----------------------------------------
        email_data = {
            "greeting": f"Hello Assistance Ace!",
            "sender_name": "Czech Unified Solutions",
            "customer_name": name,
            "customer_email": receiver_email #this is the CUSTOMER MAIL that the customer executive needs to contact
        }
        email_content = jinja_template_care.render(email_data) # render CUSTOMER CARE TEMPLATE

        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = cust_care_email  #customer care mail
        msg["Subject"] = subject_care

        # Attach the HTML content to the email
        msg.attach(MIMEText(email_content, "html"))

        # Print and send the email to customer care
        print(f"Sent email to CUSTOMER EXECUTIVE {cust_care_email}")
        server.sendmail(sender_email, cust_care_email, msg.as_string())

        # Close the server connection
        server.quit()

    else:
        # SENDING MAIL TO CUSTOMER ONLY
        email_data = {
            "greeting": f"Hello {name}!",
            "sender_name": "Czech Unified Solutions"
        }

        email_content = jinja_template.render(email_data)
        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        # Attach the HTML content to the email
        msg.attach(MIMEText(email_content, "html"))

        # Print and send the email
        print(f"Sent email to {receiver_email}")
        server.sendmail(sender_email, receiver_email, msg.as_string())

        # Close the server connection
        server.quit()        

if __name__=="__main__":
    # sample
    name='Atul Kumar Nayak'
    receiver_email="atulnayak7869@gmail.com"
    emotion="sadness"
    send_email(name,receiver_email,emotion)