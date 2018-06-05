import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def write_email(content, title, attachment=None):
    msg = MIMEMultipart()       #创建带有附件的邮件对象
    text = MIMEText(content, _charset="utf-8")     #创建正文内容对象
    msg["Subject"] = title                  #邮件标题
    msg.attach(text)                          #正文添加到邮件包中

    if attachment:
        with open(attachment, "rb") as file:
            attachPart = MIMEApplication(file.read())    #创建附件对象
        attachPart.add_header("content-disposition", "attachment", filename=attachment)   #附件命名
        msg.attach(attachPart)        #附件添加到邮件包中
    return msg

def send_email(sender, key, receiver, msg):
    msg["From"] = sender           #添加发件人IP信息到邮件包
    msg["To"] = receiver           #添加收件人IP信息到邮件包

    smtp = smtplib.SMTP_SSL()       #创建邮件服务器对象
    smtp.connect("smtp.163.com", 465)    #链接163邮件服务器
    smtp.login(sender, key)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()      #断开服务器
    print("邮件发送成功!")

if __name__ == "__main__":
    sender = input("登录, 请输入邮箱地址: ")
    key = input("请输入授权码: ")
    receiver = input("请输入收件人地址: ")
    title = input("请输入邮件标题: ")
    content = input("请输入邮件正文内容: ")
    attachment = input("请上传附件: ")
    msg = write_email(content, title, attachment)
    send_email(sender, key, receiver, msg)