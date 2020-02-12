from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.Conf import ConfigYaml
import smtplib


class SendEmail:

    def __init__(self, smtpserver, username, password, rece, title, content=None, file=None):
        self.smtpserver = smtpserver
        self.username = username
        self.password = password
        self.rece = rece
        self.title = title
        self.content = content
        self.file = file

    # 发送邮件方法
    def send_mail(self):
        msg = MIMEMultipart()
        # 初始化邮件信息
        msg.attach(MIMEText(self.content, _charset="utf8"))
        msg["Subject"] = self.title
        msg["From"] = self.username
        msg["To"] = self.rece

        # 判断是否有附件
        if self.file:
            # MIMEText读取文件
            att = MIMEText(open(self.file).read())
            # 设置内容类型
            att["Content-Type"] = "application/octet-stream"
            # 设置附件头
            att["Content-Disposition"] = 'attachment;filename="%s"' % self.file
            # 将内容附加到邮件主体中
            msg.attach(att)
        # 登录邮件服务器
        self.smtp = smtplib.SMTP(self.smtpserver, port=25)
        self.smtp.login(self.username, self.password)
        # 发送邮件
        self.smtp.sendmail(self.username, self.rece, msg.as_string())


if __name__ == '__main__':
    email_info = ConfigYaml().get_email_info()
    smtpserver = email_info["smtpserver"]
    username = email_info["username"]
    password = email_info["password"]
    rece = email_info["receiver"]
    email = SendEmail(smtpserver, username, password, rece, "测试")
    email.send_mail()








