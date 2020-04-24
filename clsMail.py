# Class
#　メール機能
#　1.CreateInfo：情報作成
#　2.SendMail：送信
import base64
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import ssl


class clsMail:
    FROM_ADDRS = ''
    TO_ADDRS = ''
    MY_PASSWORD = ''
    BODY = 'お客様が到着しました。'
    HOST = ''
    NEGO_INFO = ('', '')  # (通信方式、ポート番号)
    MSG = MIMEText(BODY)

    def __init__(self):
        self.FROM_ADDRS = ''
        self.TO_ADDRS = ''
        self.MY_PASSWORD = ''
        self.BODY = ''
        self.HOST = ''
        self.NEGO_INFO = ('',0)
        self.MSG = MIMEText(self.BODY)


    # 設定
    # 引数：お客様名　会社名、Char情報、送信元、送信先、cc、bcc、件名、ホスト名、通信情報、ポート名
    # 戻値：msg (本文)
    def CreateInfo(self, Gstname, CmpyName, cinfo, fromA, toA, passW, cc, bcc, subject, host, nego, port):
 
         # ＜本文作成＞　下記、本文イメージ
        #　
        #　会社名
        #　お客様名　様が受付に到着しました。
        #
        self.BODY = CmpyName + '\r\n' + Gstname + '様が受付に到着しました。'

        # その他、設定
        self.FROM_ADDRS  = fromA
        self.TO_ADDRS    = toA
        self.MY_PASSWORD = passW
        self.HOST = host
        self.NEGO_INFO = (nego, port)

        # MIME　Message作成
        if cinfo == "utf-8":
            self.MSG = MIMEText(self.BODY)
        elif cinfo == "iso-2022-jp":
            self.MSG = MIMEText(base64.b64encode(self.BODY.encode(cinfo, "ignore")), "plain", cinfo)

        self.MSG["Subject"] = subject
        self.MSG["From"] = fromA
        self.MSG["To"] = toA
        if cc is not None :
            self.MSG["Cc"] = cc
        if bcc is not None :
            self.MSG["Bcc"] = bcc        
        self.MSG["Date"] = formatdate(None,True)

    # 送信
    def SendMail(self):
        try:
            print("メール送信中")
            # SMTPクライアントインスタンス作成
            if self.NEGO_INFO[0] == "no-encrypt":
                stmpclient = smtplib.SMTP(self.HOST, self.NEGO_INFO[1], timeout=10)
            elif self.NEGO_INFO[0] == "starttls":
                stmpclient = smtplib.SMTP(self.HOST, self.NEGO_INFO[1], timeout=10)
                stmpclient.ehlo()
                stmpclient.starttls()
                stmpclient.ehlo()
            elif self.NEGO_INFO[0] == "ssl":
                context = ssl.create_default_context()
                stmpclient = smtplib.SMTP_SSL(self.HOST, self.NEGO_INFO[1], timeout=10)
            stmpclient.set_debuglevel(2) # サーバ通信Debug出力

            #   サーバーログイン
            stmpclient.login(self.FROM_ADDRS, self.MY_PASSWORD)

            # メール送信
            stmpclient.send_message(self.MSG)
            stmpclient.quit()
        except Exception as e:
            print("Except: " + str(e)) #エラー出力
        else:
            print("メール送信完了しました。".fromat(self.TO_ADDRS))


if __name__ == '__main__':
    Mail = clsMail()
    Mail.CreateInfo( 'あおき', '青木会社', "utf-8", "tsctestuser8@gmail.com", "aoki@kktsc.onmicrosoft.com", 'tsc201509AI', '', '', 'クラステスト送信', "smtp.gmail.com", "ssl", 465)
    #Mail.CreateInfo( 'あおき', '青木会社', "iso-2022-jp", "tsctestuser8@gmail.com", "aoki@kktsc.onmicrosoft.com", 'tsc201509AI', '', '', 'クラステスト送信', "smtp.gmail.com", "starttls", 587)
    #Mail.CreateInfo( 'あおき', '青木会社', "iso-2022-jp", "zene2729@yahoo.co.jp", "aoki@kktsc.onmicrosoft.com", 'zene2728', '', '', 'クラステスト送信', "smtp.mail.yahoo.co.jp", "no-encrypt", 587)
    Mail.SendMail()