import smtplib
import LoadEnv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# 配置SMTP服务器和邮箱账户
smtp_server = LoadEnv.load_env().get('smtp_server')  # 你的SMTP服务器地址
smtp_port = LoadEnv.load_env().get('smtp_port')  # SMTP服务器端口
sender_email = LoadEnv.load_env().get('sender_email')  # 发件人邮箱地址
sender_password = LoadEnv.load_env().get('sender_password')  # 授权码


# 附件（如果需要）
# attachment_path = 'path_to_attachment_file.pdf'
# with open(attachment_path, 'rb') as attachment:
#     attachment_part = MIMEApplication(attachment.read(), Name='attachment.pdf')
# attachment_part['Content-Disposition'] = f'attachment; filename="{attachment_path}"'
# msg.attach(attachment_part)

def sendMail(recipient_email, message_text):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = '签到脚本结果通知'
    msg.attach(MIMEText(message_text, 'plain'))
    # 连接到SMTP服务器并发送邮件
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 使用TLS加密连接
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print('邮件发送成功')
    except Exception as e:
        print('邮件发送失败:', str(e))


# 调试一下
if __name__ == '__main__':
    sendMail('1231231231@qq.com', "小程序签到成功！")
