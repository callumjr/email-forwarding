import imaplib, smtplib, email, pprint, config

def check_criteria(keywords, body):
    for word in keywords:
        if word in body.lower():
            return True
    
    return False

imap_host = config.IMAP_HOST
smtp_host = config.SMTP_HOST
smtp_port = config.SMTP_PORT
user_email = config.USER_EMAIL
user_pass = config.USER_PASS
send_adress = config.SEND_ADDRESS

keywords = ['po', 'order']

imap = imaplib.IMAP4_SSL(imap_host)

imap.login(user_email, user_pass)

imap.select('Inbox')

tmp, data = imap.search(None, 'NEW')
for num in data[0].split():
    tmp, data = imap.fetch(num, '(RFC822)')

    message = email.message_from_bytes(data[0][1])

    for part in message.walk():
        if part.get_content_type() == "text/plain":
            content_string = part.get_payload()
            # print(content_string)
            
            if check_criteria(keywords, content_string):
                message.replace_header("From", user_email)
                message.replace_header("To", send_adress)
                
                print('message contains keyword')
                smtp = smtplib.SMTP(smtp_host, smtp_port)
                smtp.starttls()
                smtp.login(user_email, user_pass)
                smtp.sendmail(user_email, send_adress, message.as_string())
                smtp.quit()
                print('message sent')

            else:
                print("message does not contain keyword")
imap.close()

# create email list
# if not on email list check for keywords 

# print('Message: {0}\n'.format(num))
    # print(f"From: {message.get('From')}")
    # print(f"To: {message.get('To')}")
    # print(f"BCC: {message.get('BCC')}")
    # print(f"Date: {message.get('Date')}")
    # print(f"Subject: {message.get('Subject')}")

    # print(f"Content:")