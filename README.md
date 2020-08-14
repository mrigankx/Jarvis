# About Covia
Covia is a virtual personal assistant(Virtual assistants are typically cloud-based programs that require internet-connected devices and/or applications to work. Three such applications are Siri on Apple devices, Cortana on Microsoft Devices and Google Assistant on Android devices.) for a pc user with a login feature and permission sets. It can do the basic stuffs that a user do on their day to day life; like,
1) Opening the browser and search something and then close the browser.
2) Reading the news headlines
3) Reading the information about any topics from Wikipedia.
4) Opening file explorer.
5) Time and weather information.
6) Email to a specific person.
7) Play music.
) It can lock, sign out, restart and shutdown the pc.
etc.

## Built with
* [Python](https://python.com)
* [Selenium](https://www.selenium.dev/)
* Web Scraping
* [Speech Recognition](https://pypi.org/project/SpeechRecognition/)
* [MySQL](https://www.mysql.com/)
## Setup for running this project
1) Create a Database in MySQL with name="jarvis_data".
2) Include 4 tables: credentials, email_auth, email_list, permissions.
3) for every table, there are some columns mentioned below,
 * credentials : cred_id, username, password, master_pass.
 * email_auth : auth_id, cred_id, email, epass.
 * email_list : sl_no, shortname, email_id.
 * permissions : cred_id, email_access, internet_access, master_access.
#### Definitions of columns: 
1) **cred_id**: This is the primary key of credentials table.(Type: Auto number).
2) **username**: In this columns the usernames who will use covia are stored.(Type: TEXT), ex: user501, user502 etc.
3) **password**: This column will hold the passwords for the users.(Type: TEXT).
4) **master_pass**: This is the master key for the software, without this a user cannot reset his password.(Type: TEXT).
5) **auth_id**: This is the primary key for email_auth table.(Type: Auto Number).
6) **email**: This contains the email adddress of covia, by which the email automation will be done.
7) **epass**: This will contain the password for the email address of the email.
8) **sl_no**: This is the primary key for email_list table.(Type: Auto Number).
9) **shortname**: This will contain the email recepient's name.
10) **email_id**: In this, the recepient's email address will be stored.
11) **email_access**: This field will contain the information that if a user has the permission to send email or not.
12) **internet_access**: This field will contain the information that if a user has the permission to use internet or not.
13) **master_access**: If this field is set to TRUE, then that user will have both email and internet access and that user will become master user.



## How to run this project
1) Clone the Repository.
2) Switch to master branch.
3) To run the project, enter and run
```bash
pip install -r requirements.txt
python index_main.py
```

