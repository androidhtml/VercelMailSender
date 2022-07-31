import smtplib as ml
from http.server import BaseHTTPRequestHandler
from os import environ
from json import dumps,loads
from re import compile
from email.mime.text import MIMEText
from email.header import Header
from urllib.parse import unquote
from email.utils import formataddr
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin',"*")
            self.send_header('Content-type','application/json')
            self.end_headers();
            passwd = compile(r'passwd=([^?&=]*)').findall(self.path);
            to = compile(r'to=([^?&=]*)').findall(self.path);
            if len(passwd)==0:
                self.wfile.write(dumps({
                        "code": 0,
                        "msg": "请输入密码"
                }).encode());
                return;
            elif passwd[0]=='' or passwd[0] != environ['passwd']:
                self.wfile.write(dumps({
                        "code": 0,
                        "msg": "密码错误"
                    }).encode(encoding='utf-8'));
                return;
            msg = compile(r'msg=([^?&=]*)').findall(self.path);
            if len(msg)==0:
                    self.wfile.write(dumps({
                        "code": 0,
                        "msg": "未指定消息"
                    }).encode(encoding='utf-8'));
                    return;
            content =  MIMEText(unquote(msg[0]),'plain','utf-8')
            content['From']=formataddr(["网站通知小助手",environ["SMTP_USER"]])
            content['To']=formataddr([environ["MASTER_NAME"],to]);
            content['Subject']=Header("有新通知辣!");
            smtpobj = ml.SMTP_SSL(environ["SMTP_SERVER"],465)
            smtpobj.login(environ["SMTP_USER"],environ["SMTP_PASS"]);
            mail = content
            smtpobj.send_message(from_addr=environ["SMTP_USER"], to_addrs=environ["RECIEVER"],msg=mail)
            self.wfile.write(dumps({
                        "code": 200,
                        "msg": "成功"
                    }).encode(encoding='utf-8'));
            return;
        except Exception as e:
            print(e);
            self.wfile.write(dumps({
                "code": 500,
                "msg": "配置错误，请在服务端查看错误日志"
            }).encode(encoding='utf-8'))
        finally:
            return;
