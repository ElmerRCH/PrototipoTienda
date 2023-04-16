import smtplib

from_addr = 'renehiguera15@gmail.com'
to = 'renehiguera2018@gmail.com'
message = 'This is a test Email from python'

# Reemplaza estos valores con tus credenciales de Google Mail
username = 'renehiguera15@gmail.com'
password = 'accorzuwpwvhqhlp'
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username, password)
server.sendmail(from_addr, to, message)
server.quit()