from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import smtplib
import functions
from email.mime.multipart import MIMEMultipart

from email.mime.application import MIMEApplication


import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 
 


master=Tk()
master.title("Topsis Information Form")
f1=''
def browse():
    global f1
    f1=filedialog.askopenfilename(initialdir="/",title="Select a File",filetype=(("CSV Files","*.csv"),))
    #filename is saved in f1

    
      
def sent():
    global weight
    global impact
    global receiver_address
    print(f1)
    weight=temp_weight.get()
    impact=temp_impact.get()
    receiver_address =temp_email.get()
    functions.topsis(f1,weight,impact,"102003427-result4.csv")
    mail_content ='hello'
#The mail addresses and password
    sender_address = 'okpython03@gmail.com'
    sender_pass = 'ownmihsqpwiifqfv'
    
    
    #print(receiver_address)
#Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Topsis Solution'
#The subject line
#The body and the attachments for the mail
    filenameq = '102003427-result.csv' # TODO: replace your attachment filepath/name
    with open(filenameq, 'rb') as fp:
           attachment = MIMEApplication(fp.read())
           attachment.add_header('Content-Disposition', 'attachment', filename=filenameq)
           message.attach(attachment)
 #encode the attachment
# #add payload header with filename
    
#Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
  



mytitle=Label(master,text="Topsis Information Form",font=('Calibri',20)).grid(row=0,sticky=N)
n1=Label(master,text="File Name",font=('Calibri',15)).grid(row=1,sticky=W,padx=5)
n1=Label(master,text="Weights",font=('Calibri',15)).grid(row=2,sticky=W,padx=5)
n1=Label(master,text="Impacts",font=('Calibri',15)).grid(row=3,sticky=W,padx=5)
n1=Label(master,text="EmailId",font=('Calibri',15)).grid(row=4,sticky=W,padx=5)
n1=Label(master,text="",font=('Calibri',15)).grid(row=4,sticky=S,padx=5)

temp_file=StringVar()
temp_weight=StringVar()
temp_impact=StringVar()
temp_email=StringVar()

fileEntry=Entry(master,textvariable=temp_file)
fileEntry.grid(row=1,column=0,padx=5)

weightEntry=Entry(master,textvariable=temp_weight)
weightEntry.grid(row=2,column=0,padx=5)
impactEntry=Entry(master,textvariable=temp_impact)
impactEntry.grid(row=3,column=0)

emailEntry=Entry(master,textvariable=temp_email)
emailEntry.grid(row=4,column=0)


Button(master,text="Browse a File",command=browse).grid(row=1,column=1,pady=0,padx=0)

Button(master,text="Submit",command=sent).grid(row=5,sticky=S,pady=15,padx=5)


master.mainloop()