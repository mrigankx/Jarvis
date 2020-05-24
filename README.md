Install these python libraries:
tkinter
mysql
pyowm
pyttsx3
requests
speech_recognition
vlc
wikipedia
youtube_dl
bs4
selenium
nltk

Create a Database with name="jarvis_data" and include 3 tables:
  Table               Columns
`credentials` :      `cred_id`
                    `username`
                    `password`
                    `master_pass`
                    
`email_auth`  :     `auth_id`
                    `cred_id`
                    `email`
                    `epass`

`email_list`  :     `sl_no`
                    `shortname`
                    `email_id`
