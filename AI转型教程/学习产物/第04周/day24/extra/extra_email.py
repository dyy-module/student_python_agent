import re

def is_valid_email(addr):
    email_re = r'[0-9a-zA-Z]+(\.?[0-9a-zA-Z]+)@[0-9a-zA-Z]+\.com'
    return re.match(email_re,addr)

# 测试:
assert is_valid_email('someone@gmail.com')
assert is_valid_email('bill.gates@microsoft.com')
assert not is_valid_email('bob#example.com')
assert not is_valid_email('mr-bob@example.com')
print('ok')
