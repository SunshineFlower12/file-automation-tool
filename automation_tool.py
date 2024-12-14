import os
import shutil
import smtplib
from email.message import EmailMessage
import http.client
from html.parser import HTMLParser
import time
import datetime
import re
import logging

# Set up logging
logging.basicConfig(filename='automation_tool.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def display_menu():
    """Displays a menu for users to choose automation tasks."""
    print("\nWelcome to the Automation Tool!")
    print("1. Web Scraping")
    print("2. File Management")
    print("3. Send Email")
    print("4. Schedule Tasks")
    print("5. Exit")
    choice = input("Enter your choice (1-5): ")
    return choice

def validate_email(email):
    """Validates the email format."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        print(f"Invalid email format: {email}")
        logging.error(f"Invalid email format: {email}")
        return False
    return True

def validate_url(url):
    """Validates the URL format."""
    url_regex = r'^(https?://)?[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(url_regex, url):
        print(f"Invalid URL format: {url}")
        logging.error(f"Invalid URL format: {url}")
        return False
    return True

def validate_directory(path):
    """Checks if a directory exists and is valid."""
    if not os.path.exists(path):
        print(f"Directory does not exist: {path}")
        logging.error(f"Directory does not exist: {path}")
        return False
    if not os.path.isdir(path):
        print(f"Invalid directory: {path}")
        logging.error(f"Invalid directory: {path}")
        return False
    return True

def web_scraping_automation():
    """Interactive web scraping with user inputs."""
    url = input("Enter the URL to scrape (e.g., www.example.com): ")
    if not validate_url(url):
        return
    output_file = input("Enter the output file name (e.g., output.html): ")
    
    # Extract the domain name and path for http.client
    domain = url.split("/")[2] if "://" in url else url.split("/")[0]
    path = '/' + '/'.join(url.split("/")[3:])
    
    try:
        # Create a connection and request the page
        conn = http.client.HTTPConnection(domain)
        conn.request("GET", path)
        response = conn.getresponse()
        
        if response.status == 200:
            content = response.read().decode('utf-8')
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Web scraping completed. Content saved to {output_file}")
            logging.info(f"Web scraping completed. Content saved to {output_file}")
        else:
            print(f"Error: Received status code {response.status}")
            logging.error(f"Error: Received status code {response.status}")
        conn.close()
    except Exception as e:
        print(f"Error during web scraping: {e}")
        logging.error(f"Error during web scraping: {e}")

def file_management_automation():
    """Interactive file management with user inputs."""
    source_dir = input("Enter the source directory: ")
    if not validate_directory(source_dir):
        return
    dest_dir = input("Enter the destination directory: ")
    if not validate_directory(dest_dir):
        return
    
    try:
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        for file_name in os.listdir(source_dir):
            full_file_name = os.path.join(source_dir, file_name)
            if os.path.isfile(full_file_name):
                shutil.move(full_file_name, dest_dir)

        print(f"Files moved from {source_dir} to {dest_dir}")
        logging.info(f"Files moved from {source_dir} to {dest_dir}")
    except Exception as e:
        print(f"Error during file management: {e}")
        logging.error(f"Error during file management: {e}")

def email_automation():
    """Interactive email sending with user inputs."""
    sender_email = input("Enter your email address: ")
    if not validate_email(sender_email):
        return
    receiver_email = input("Enter the recipient's email address: ")
    if not validate_email(receiver_email):
        return
    subject = input("Enter the email subject: ")
    body = input("Enter the email body: ")
    smtp_server = input("Enter the SMTP server (e.g., smtp.gmail.com): ")
    smtp_port = int(input("Enter the SMTP port (e.g., 587): "))
    login = input("Enter your email login: ")
    password = input("Enter your email password: ")
    attachment = input("Enter the file to attach (or leave blank for no attachment): ")

    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        if attachment:
            with open(attachment, 'rb') as attachment_file:
                file_data = attachment_file.read()
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=os.path.basename(attachment))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(login, password)
        server.send_message(msg)
        server.quit()

        print("Email sent successfully.")
        logging.info(f"Email sent successfully to {receiver_email}.")
    except Exception as e:
        print(f"Error during email automation: {e}")
        logging.error(f"Error during email automation: {e}")

def schedule_automation():
    """Interactive scheduling of tasks with user inputs."""
    print("\nScheduling tasks...")

    print("\n1. Web Scraping Task")
    print("2. File Management Task")
    task_choice = input("Choose a task to schedule (1-2): ")

    if task_choice == '1':
        url = input("Enter the URL to scrape: ")
        if not validate_url(url):
            return
        output_file = input("Enter the output file name: ")
        time_to_run = input("Enter the time to run the task (e.g., 10:00): ")

        while True:
            current_time = datetime.datetime.now().strftime("%H:%M")
            if current_time == time_to_run:
                print(f"Running web scraping task at {current_time}...")
                web_scraping_automation()
                break
            time.sleep(60)  # Check every minute

    elif task_choice == '2':
        source_dir = input("Enter the source directory: ")
        if not validate_directory(source_dir):
            return
        dest_dir = input("Enter the destination directory: ")
        if not validate_directory(dest_dir):
            return
        time_to_run = input("Enter the time to run the task (e.g., 11:00): ")

        while True:
            current_time = datetime.datetime.now().strftime("%H:%M")
            if current_time == time_to_run:
                print(f"Running file management task at {current_time}...")
                file_management_automation()
                break
            time.sleep(60)  # Check every minute

def main():
    while True:
        choice = display_menu()

        if choice == '1':
            web_scraping_automation()
        elif choice == '2':
            file_management_automation()
        elif choice == '3':
            email_automation()
        elif choice == '4':
            schedule_automation()
        elif choice == '5':
            print("Exiting the Automation Tool. Goodbye!")
            logging.info("Exiting the Automation Tool. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
