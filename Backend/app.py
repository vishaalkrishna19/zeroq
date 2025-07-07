def send_user_credentials_email(user_email, user_name, password):
    try:
        # Read email template
        with open('emails/user_created.txt', 'r') as f:
            email_content = f.read()
        # Replace placeholders
        email_content = email_content.replace('{name}', user_name)
        email_content = email_content.replace('{email}', user_email)
        email_content = email_content.replace('{password}', password)
        # Extract subject and body
        lines = email_content.split('\n')
        subject = lines[0].replace('Subject: ', '')
        body = '\n'.join(lines[2:])  # Skip subject and empty line
        # Send email using configured admin email
        send_email(ADMIN_EMAIL, user_email, subject, body)
    except Exception as e:
        print(f"Failed to send user credentials email to {user_email}: {str(e)}")
        return False
    return True
#Hello this is a test line

print("hello")








