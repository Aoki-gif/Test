import win32com.client


TO_ADDRS = 'tsctestuser8@gmail.com'
FROM_ADDRS = 'aoki@kk-tsc.com'

outlook = win32com.client.Dispatch('Outlook.Application')
mymail = outlook.CreateItem(0)


sign = '''
テスト　署名　テスト
Outlok
'''


mymail.BodyFromat = 1
mymail.To = TO_ADDRS
mymail.Subject = 'テスト'
mymail.body = '''
各位

お疲れ様です。
テスト送信です。
''' + '\n' + sign

mymail.send()

