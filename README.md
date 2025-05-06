CareHub
CareHub is a Python console-based medical appointment system. It includes two apps: one for users to book and manage appointments, and one for admins to review and update appointment statuses. All data is handled through a connected database.

Features
User App:

Create and manage medical appointments.

View appointment statuses (approved, denied, skipped).

Email notifications for appointment status updates.

Admin App:

Review and approve or deny appointment requests.

Send status updates to users.

View user appointment details.

Requirements
Python 3.6 or higher.

A MySQL-compatible database for storing user and appointment data.

Installation
Clone the repository:
git clone https://github.com/your-username/CareHub.git
cd CareHub

Install dependencies (you may use a virtual environment):
pip install -r requirements.txt

Set up the database by running the provided SQL scripts (adjust for your specific database configuration).
Run create_tables.py to have the required tables for the program to run.

Update the send_email.py file with your email settings (SMTP server, email, and password) for sending email notifications.

Usage

Run the user or admin application:

For User app:
python App_user.py

For Admin app
python App_admin.py

1) Admin must enter the information for specialities, doctors and doctors schedule to appintments are available for the user to take.

2) User can follow ths on-screen prompts to manage appointments.

3) Admin review and acepts/rejects appointments requests.
