import smtplib 
from email.message import EmailMessage 

email_subject = "Email test from Python" 
sender_email_address = "renehiguera15@gmail.com" 
receiver_email_address = "renehiguera13@gmail.com" 
email_smtp = "smtp.gmail.com" 
email_password = "fortnite125" 

message = EmailMessage() 
message['Subject'] = email_subject 
message['From'] = sender_email_address 
message['To'] = receiver_email_address 

message.set_content("Hello from Python!") 

server = smtplib.SMTP(email_smtp, '587') 

server.ehlo() 

server.starttls() 
server.login(sender_email_address, email_password) 

server.send_message(message) 

server.quit()