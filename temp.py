"""
search the value of `signin` you can see this api as the picture shown.
it sets cookie. so you need to request this api before submitting a request to login api via `requests.session()`
authorize api的状态是302重定向，向这个地址发送请求,requests会自动处理，返回重定向之后的页面(login get)。
注意，此时的login是get请求，仅用于获取login的前端页面，还没有输入密码

输入密码后，api是login的post请求，`signin`来源于上一个login的response

heres an example:
```python
import requests

def authorize():
    cookies = {...}
    headers = {...}
    params = {...}
    response = session.get('https://secure.costargroup.com/connect/authorize', params=params, cookies=cookies, headers=headers)
    print(response.text) # here you can see the login page source, extract signin from it
    return response.text

if __name__ == '__main__':
    session = requests.session()
    resp = authorize()


```

如果输入的是正确的账号密码，页面应该会跳转，并返回登陆成功后的页面源代码。之后用这个session向你的目标api发送请求即可。

i dont have an account so dont know if it can work. Feel free to tell me if you have any other question :)


"""



from lxml import etree
import requests

cookies = {
    'SignInMessage.027a745704a84294571a274b303008ba': 'yaEqCjXbbcZY_Fb6GmGJAEaRBn0FZhlzz7bRmJ2rgzJaJVhKOSPPM8-hkiEm_Kgqo__Fpf0aLPl8mGSPwKgI1mlIG-iHo5peC5SdiDKgVydRrF-MD8p3MciIdRWDLOgBgdeSYjDUOVDRJfzaqCUbaEHDvVbUnqrlp23yWd7d702cIgpdh3JwOk6_FbEotFSScbcqnxF04apNhOjgZYk3N5KcVsrjpae2SltP92ORCLOfz_fhQOLQYrpyQwcAtlXNbTsEmpravU3V7gdxnw79FhD4yIaDmR3nAkuncqm0zpBGtE5WK9R58X2vHy-2e-ej-UEe44BnsvlKzLVxT_T3SYafz19uGi-3XKYbjymBIBmez1QkESh-pktM5gVdqkblKvqCW4xASSHbmBocRFt-_Ie05dFU47uepMAUULgwpjKz4wzs9IoMJesCoOMxtSqgjNDymJ9Grp4WKAKVrPHEDeA7lVFxlcLYrCgEjrjCjacxeKL5sCBmj9C-2la6lYEwJI0W9AMKVOyULhlVOV9KJXL7u8_HLCJeqNYZyEtKePYfJZfJWY7BLBzlXaZUfZIcZmEQbqENeogom72a6ILm-reZe7Zt98SlEH-xPWiwZIXYwQjSuhzesVMmFrkQuXVIWzZopyXO06hNPo0L9m9tKw',
    'idsrv.xsrf': '6eroodEwH-IayQeB1KCsbSOwmyNMTDl9auCRvV1pg6VLVA1TI2i_n3mGJwmU8JC3aLcpNaCJJNedrEEmzipeKNQg7m0Dq5j4MXrYBwpn0Hk',
    'ak_bmsc': '59D5CF5F9C2F38934F7DAA093CB80958~000000000000000000000000000000~YAAQJdgjF5ctcsiWAQAA0d5b6BunBhasMqnhJKn4Bz5ZvXiCFL9xbD5yh/jZyO84vXlsN9TbVjMF77hr1IwOzIj4DxIsqAA/x0maT0hR1goaqjUdgF1GZhRJmng3g3r5HVtveuNx5sXlBMfk9vPC8GNHrR1Sm4xxJJWYopEKFdaWgEiGR0x+F1igDppKPY2k68fkD1tw7vatdpVkojjfR4qolFImA2g0HKI3NVPqS7/PLk1tnoZAZPBCZ25t35KQZvQjSPDzTvkvB97HQvWBLeGD6dpjplSyLNXgP1uwYvs2UfkgDGeWT3BDtKGY4Dizn8Wem93NVnEXsLPUv7WAtaI5nKspRjUHcjDrGMiSpJtnvCilrzIoe+JmM5s/j/KZwGiHEG9E28p8hPG5DKHI',
    '__ssid': '30394ef0e1ccf101fcce8521f278498',
    'SignInMessage.77cf101785aa288926c78c091160493e': '2AKu6ZOaUmbtm1ZuibOHuMJEc7-euskSp8mA4knpMF_-bt8stBMmkQ2VY-Tcu_uH5sAgheY1z7lRSVqDi_kpDIs1iMVfAhY3FKYX0nt73zy5y9T7P4BdtvtPWytll3rhyulWmM0arZV8WktaqJfR0LhYqQ4w4bJCcOmiQkqXhn9YLSDVTFyL_Zfw4xzOxJ2d9sW8H0apowCQIWqLIM4fkpb32m8_sQr8IxX5JcYIbyqLLEC0qGJt4d2fzLb3zadCy2Dy91SdNpUkv1Z8F3vx9kd47kgQ5nG59BydUcRu3WQRuEhq2xp1P9qX_OJ93cC5wTA4Cd8DDjYul-repsPDUCuRvbMTWwNkzpNt0yKzmlWi-tXcI3nXPskfiJxxQrpt3dHWR91S0lfbREuK6vaZseR9dn2glmYaNkL3BhUROi72hciPgKgJsbV7bBOq0H_wPISqgdMhdVNFRQ8_k4Y81kCfn1iDePqu29Pt2lWELg16tJf10imWEDUs7e3vplY6NZdBiNaVzY2FlQNJK7oyiBQzWmvZhujflIgnrUgybfYlUsx3Kh70Bc4HoDO3DES-QjdzFuf82C9Sp4BqJPoB_nKNEniavA7c1LaRMlAALv3Pnsz-9IB10a4xWcrqpTFS_YDlUPlbMgFexQaQS_Enpw',
    'SignInMessage.c53596f7169cb651bdb130bda13f40ef': 'kgcj__ZaOa50eU7tM5YOd5EOCSxV_JWrtADjB5BGyJ3VlmKpAbT2uPD-sxaXm9OMx7k9Slg6pfsQoNsZ5hRy85YMs3wtsqHZfdHg031hl-D8XutmrEh9NBSvF1NvUT8-6IHIZp9qTMZlafvdIhhuoAGV7CV0rMy5NGs5RYYn9xMzjQEzf4eg-KUUbkNte3nkBSPyerNzeUsIcmnyHSSk-RwQpo4ldrdoObiFcbPM0YZcLVvaQJPLR5Bk5XEuRZHr4Ike2SlvzajVpod8oZgi0d9HSCwWXVt9PvMOqdZVEQMDkwW_ct9hEbF4IPTiRPl4GbPhIl4CNp7ypc3XHU51lDF_f_5tykRsOENx1-i0xKjaso62BwPACs32fiqg4R4l8Q5hGZV3NfzaYJ8lZJlPrA02piMrPysscaN0QQ_2d8SwhT4VBozov6MX49ydxvKgxWucMu_HKpO8lpnREvE81FS1jIi-lgD7a32JiZz5pOOlLxYeHfDgPmFjZVxh7Pk2n4v67Ff9zwnkYKJeck8ivhhDBZByBm2wZ3J8Guc3aHCSIch4vPLyAonTlC855GbZKtUbByhYZ0dSStA1iw8ZUEUz0fVYPcxJSv7QRLVqvyEz_zWOh2uPWYzyeLsvMG1UyksbhepmMRyH6vK8FpCwuQ',
    'centralauthn.pending': 'R2GANuhsEC9mDYlj32UC8IwqLShEd4d9z3lTHFtOQdTc36BHAEYAAVL9QTyksJKMXAo1fACqyVeHPgw-gECL0YYm4Qco0sPYgU-RW_dWWpUzs01U1BhKn68xC8TsjIT-buuZuUMyxr0AmfYuGYBn2hOwW_RnERLyta1SX-ReSMi20BvuWbj0lkfIB5kRhbVX9eXFC3TnOxVDFWbVlsIqqmrg6L90njVga6QWGtGr2QN8gQj9lt5naxPLwTejBuUKVy6aMnnr5i7OiJCZaqOmd9IaQ6_OarVn1gznaER9lDE',
    'pc': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImxTTHVmSWJfSUtRX29KLXVlcnR5MnBOS3o3QSIsInR5cCI6IkpXVCJ9.eyJ0aWQiOiI2ZTNlOGQzMGQ0ZWQ0ZDc3YWMxYjUxNGM3ZTk0ZGVlOCIsIm4iOiJlOTliMjE0ZjU5YjY0ZWU5OTI3MTgzZjQ4MTMwNzY5YSIsImV4cCI6MTgxMDcyNzE1MCwiaXNzIjoiaHR0cHM6Ly9zZWN1cmUuY29zdGFyZ3JvdXAuY29tIiwiYXVkIjoicGMifQ.THg17WfsTRk99UQYswwAEzDCF3qps2tXE1sgt_iJk5N0eqosc-lnlkK6yeY4bEbb-K6HY1mOIH1iNUD03ezagotdfRE0drW2En5M4ljx7jp498G7usdyJDMLWSPLO303nCOodEYZ4DQHFlGfAqdzcYbuArVaLFkK85vc6WoWvYuneIsOK0chFGge8Fk91-qC__KdwRSTwx8Rvn6R6bjpWtnp8c-pLnsoN7rJhb7wCG48DWga3xhCEBk6FsDdsvY9eIzNZAehoL5-i9JrgGvmjeUm7WLO_eXclrNNqzyoHolOHBJMxAn4gLhOSktwssLMuDvSUx3Fp5qPHnvqvAVsxQ',
    'bm_sv': 'ACC28EAE2897C8246561BF031DE30726~YAAQJdgjF2pEcsiWAQAAg0pd6BvXo+vRO5jvzPkaKZUxeE9ZVzhRQL9/LMs5RRkGTAzVDpbS42E1kVsCFM2lTH1tnpRHs2xFW+XQwRW6wZU6LuwLc5zAWBGI/bA+XMDdtYLr1a62GAOu28i7+RCKfSkFx/ErEuD6ST1983sXJ/jTugndJM56VC4FyUb+pu0Z56o/uuSO2XIPmjl8mtwcK2zc2qgKkj93Qqi4KD6J+FJIb47717EGnrDY3FvOJElV168cVmk=~1',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,en-CN;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://secure.costargroup.com',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://secure.costargroup.com/login?signin=77cf101785aa288926c78c091160493e',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    # 'cookie': 'SignInMessage.027a745704a84294571a274b303008ba=yaEqCjXbbcZY_Fb6GmGJAEaRBn0FZhlzz7bRmJ2rgzJaJVhKOSPPM8-hkiEm_Kgqo__Fpf0aLPl8mGSPwKgI1mlIG-iHo5peC5SdiDKgVydRrF-MD8p3MciIdRWDLOgBgdeSYjDUOVDRJfzaqCUbaEHDvVbUnqrlp23yWd7d702cIgpdh3JwOk6_FbEotFSScbcqnxF04apNhOjgZYk3N5KcVsrjpae2SltP92ORCLOfz_fhQOLQYrpyQwcAtlXNbTsEmpravU3V7gdxnw79FhD4yIaDmR3nAkuncqm0zpBGtE5WK9R58X2vHy-2e-ej-UEe44BnsvlKzLVxT_T3SYafz19uGi-3XKYbjymBIBmez1QkESh-pktM5gVdqkblKvqCW4xASSHbmBocRFt-_Ie05dFU47uepMAUULgwpjKz4wzs9IoMJesCoOMxtSqgjNDymJ9Grp4WKAKVrPHEDeA7lVFxlcLYrCgEjrjCjacxeKL5sCBmj9C-2la6lYEwJI0W9AMKVOyULhlVOV9KJXL7u8_HLCJeqNYZyEtKePYfJZfJWY7BLBzlXaZUfZIcZmEQbqENeogom72a6ILm-reZe7Zt98SlEH-xPWiwZIXYwQjSuhzesVMmFrkQuXVIWzZopyXO06hNPo0L9m9tKw; idsrv.xsrf=6eroodEwH-IayQeB1KCsbSOwmyNMTDl9auCRvV1pg6VLVA1TI2i_n3mGJwmU8JC3aLcpNaCJJNedrEEmzipeKNQg7m0Dq5j4MXrYBwpn0Hk; ak_bmsc=59D5CF5F9C2F38934F7DAA093CB80958~000000000000000000000000000000~YAAQJdgjF5ctcsiWAQAA0d5b6BunBhasMqnhJKn4Bz5ZvXiCFL9xbD5yh/jZyO84vXlsN9TbVjMF77hr1IwOzIj4DxIsqAA/x0maT0hR1goaqjUdgF1GZhRJmng3g3r5HVtveuNx5sXlBMfk9vPC8GNHrR1Sm4xxJJWYopEKFdaWgEiGR0x+F1igDppKPY2k68fkD1tw7vatdpVkojjfR4qolFImA2g0HKI3NVPqS7/PLk1tnoZAZPBCZ25t35KQZvQjSPDzTvkvB97HQvWBLeGD6dpjplSyLNXgP1uwYvs2UfkgDGeWT3BDtKGY4Dizn8Wem93NVnEXsLPUv7WAtaI5nKspRjUHcjDrGMiSpJtnvCilrzIoe+JmM5s/j/KZwGiHEG9E28p8hPG5DKHI; __ssid=30394ef0e1ccf101fcce8521f278498; SignInMessage.77cf101785aa288926c78c091160493e=2AKu6ZOaUmbtm1ZuibOHuMJEc7-euskSp8mA4knpMF_-bt8stBMmkQ2VY-Tcu_uH5sAgheY1z7lRSVqDi_kpDIs1iMVfAhY3FKYX0nt73zy5y9T7P4BdtvtPWytll3rhyulWmM0arZV8WktaqJfR0LhYqQ4w4bJCcOmiQkqXhn9YLSDVTFyL_Zfw4xzOxJ2d9sW8H0apowCQIWqLIM4fkpb32m8_sQr8IxX5JcYIbyqLLEC0qGJt4d2fzLb3zadCy2Dy91SdNpUkv1Z8F3vx9kd47kgQ5nG59BydUcRu3WQRuEhq2xp1P9qX_OJ93cC5wTA4Cd8DDjYul-repsPDUCuRvbMTWwNkzpNt0yKzmlWi-tXcI3nXPskfiJxxQrpt3dHWR91S0lfbREuK6vaZseR9dn2glmYaNkL3BhUROi72hciPgKgJsbV7bBOq0H_wPISqgdMhdVNFRQ8_k4Y81kCfn1iDePqu29Pt2lWELg16tJf10imWEDUs7e3vplY6NZdBiNaVzY2FlQNJK7oyiBQzWmvZhujflIgnrUgybfYlUsx3Kh70Bc4HoDO3DES-QjdzFuf82C9Sp4BqJPoB_nKNEniavA7c1LaRMlAALv3Pnsz-9IB10a4xWcrqpTFS_YDlUPlbMgFexQaQS_Enpw; SignInMessage.c53596f7169cb651bdb130bda13f40ef=kgcj__ZaOa50eU7tM5YOd5EOCSxV_JWrtADjB5BGyJ3VlmKpAbT2uPD-sxaXm9OMx7k9Slg6pfsQoNsZ5hRy85YMs3wtsqHZfdHg031hl-D8XutmrEh9NBSvF1NvUT8-6IHIZp9qTMZlafvdIhhuoAGV7CV0rMy5NGs5RYYn9xMzjQEzf4eg-KUUbkNte3nkBSPyerNzeUsIcmnyHSSk-RwQpo4ldrdoObiFcbPM0YZcLVvaQJPLR5Bk5XEuRZHr4Ike2SlvzajVpod8oZgi0d9HSCwWXVt9PvMOqdZVEQMDkwW_ct9hEbF4IPTiRPl4GbPhIl4CNp7ypc3XHU51lDF_f_5tykRsOENx1-i0xKjaso62BwPACs32fiqg4R4l8Q5hGZV3NfzaYJ8lZJlPrA02piMrPysscaN0QQ_2d8SwhT4VBozov6MX49ydxvKgxWucMu_HKpO8lpnREvE81FS1jIi-lgD7a32JiZz5pOOlLxYeHfDgPmFjZVxh7Pk2n4v67Ff9zwnkYKJeck8ivhhDBZByBm2wZ3J8Guc3aHCSIch4vPLyAonTlC855GbZKtUbByhYZ0dSStA1iw8ZUEUz0fVYPcxJSv7QRLVqvyEz_zWOh2uPWYzyeLsvMG1UyksbhepmMRyH6vK8FpCwuQ; centralauthn.pending=R2GANuhsEC9mDYlj32UC8IwqLShEd4d9z3lTHFtOQdTc36BHAEYAAVL9QTyksJKMXAo1fACqyVeHPgw-gECL0YYm4Qco0sPYgU-RW_dWWpUzs01U1BhKn68xC8TsjIT-buuZuUMyxr0AmfYuGYBn2hOwW_RnERLyta1SX-ReSMi20BvuWbj0lkfIB5kRhbVX9eXFC3TnOxVDFWbVlsIqqmrg6L90njVga6QWGtGr2QN8gQj9lt5naxPLwTejBuUKVy6aMnnr5i7OiJCZaqOmd9IaQ6_OarVn1gznaER9lDE; pc=eyJhbGciOiJSUzI1NiIsImtpZCI6ImxTTHVmSWJfSUtRX29KLXVlcnR5MnBOS3o3QSIsInR5cCI6IkpXVCJ9.eyJ0aWQiOiI2ZTNlOGQzMGQ0ZWQ0ZDc3YWMxYjUxNGM3ZTk0ZGVlOCIsIm4iOiJlOTliMjE0ZjU5YjY0ZWU5OTI3MTgzZjQ4MTMwNzY5YSIsImV4cCI6MTgxMDcyNzE1MCwiaXNzIjoiaHR0cHM6Ly9zZWN1cmUuY29zdGFyZ3JvdXAuY29tIiwiYXVkIjoicGMifQ.THg17WfsTRk99UQYswwAEzDCF3qps2tXE1sgt_iJk5N0eqosc-lnlkK6yeY4bEbb-K6HY1mOIH1iNUD03ezagotdfRE0drW2En5M4ljx7jp498G7usdyJDMLWSPLO303nCOodEYZ4DQHFlGfAqdzcYbuArVaLFkK85vc6WoWvYuneIsOK0chFGge8Fk91-qC__KdwRSTwx8Rvn6R6bjpWtnp8c-pLnsoN7rJhb7wCG48DWga3xhCEBk6FsDdsvY9eIzNZAehoL5-i9JrgGvmjeUm7WLO_eXclrNNqzyoHolOHBJMxAn4gLhOSktwssLMuDvSUx3Fp5qPHnvqvAVsxQ; bm_sv=ACC28EAE2897C8246561BF031DE30726~YAAQJdgjF2pEcsiWAQAAg0pd6BvXo+vRO5jvzPkaKZUxeE9ZVzhRQL9/LMs5RRkGTAzVDpbS42E1kVsCFM2lTH1tnpRHs2xFW+XQwRW6wZU6LuwLc5zAWBGI/bA+XMDdtYLr1a62GAOu28i7+RCKfSkFx/ErEuD6ST1983sXJ/jTugndJM56VC4FyUb+pu0Z56o/uuSO2XIPmjl8mtwcK2zc2qgKkj93Qqi4KD6J+FJIb47717EGnrDY3FvOJElV168cVmk=~1',
}

def authorize():
    global session
    cookies = {
        'pc': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImxTTHVmSWJfSUtRX29KLXVlcnR5MnBOS3o3QSIsInR5cCI6IkpXVCJ9.eyJ0aWQiOiIwNWJiNjZkNDI5NWU0NTEzODYyMDY1MDRlN2U0OGFjNSIsIm4iOiI5NjAwYjIzZDA4ODk0ODM4YmMxYzZjNjUzNmEwY2M2YSIsImV4cCI6MTgxMDcyNzg4MSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmUuY29zdGFyZ3JvdXAuY29tIiwiYXVkIjoicGMifQ.kNtYXT_mzu-azgtFaTINL0eUsK5bxL0eQv--u-avv_HIhS0s6Ppju3WYSayfpbNG1P0R6hoDuSjo1toYExskysVMwowbZUihX7CXpyOu4D3RLQSzDVmzDYXuxKmNR1UB8jEj2A00epmD9LMrFemg-pncAr5uVsfPXFrnozAwMUxrKCgFlX6zMnsoYQ_xXrunZ3dHnnQeSK_Xfg6e7r0dd7pM7McnMWJMMPU0KWTlGHT9cH9E_CG4KP4JqgpSRXDzWT8V8ON5n8JDyKNhljsep5NdpPrvif9y-_HdYvt3S638xsM0V_XoaebYw3hDNyDexYrrxmAV4uCKf0NX1xbEUA',
        'bm_mi': '5CB3090C6822FF051D6829597A32AD8E~YAAQJdgjFxr+csiWAQAArYlo6BsX2sJprUu0MWc3CG66crVr647Whn0y/lV06Lo9C8XepL30vW5p/Nd7QDdUAbuqoPaBIxD9yZUVNjE1TLaKvFp632BNVMIX5D3l0LR6jNNMWAMWigoIm6J6TXWoaCZez7JVT0vFWYb9E3sX38bxj4SiKF4DQcyc0jeyyHRR42CVG2Ikh+pzhxHZ4PGrTZXEdDsg532eVyW7w99rgYla0L6NQHyf0ajwy9ryaQe46RQ1DVB2yitTEHBMBnPLyZSnUGpyLt78oz5C5aDuUy4askW+BmPoVpVEKA8dPmeB~1',
        '_gcl_au': '1.1.1647554421.1747655890',
        '_ga': 'GA1.1.1078223496.1747655890',
        'ak_bmsc': '7E6F9B19C20FA02CEF6295BE8ED4E590~000000000000000000000000000000~YAAQJdgjF57+csiWAQAAk5Fo6Buq+kRDWClXJZdFvzTrT34tQD9gE7FzSzykEw5XPtZQDIlTeW0exSSF+2iCkwMi4EzOKd/doWJjB1QwjF+METSVFREJ+vi105fLYHcMOoF8BfPZpuBrAbtCC0VeeBc0YV+JXicjxZgJB1EcY7Ujzq4KwRNuhYvFD9BA3sd6rSQA3lG/qz+rXWgOSzsxElKNaDunjzaGAsvN9ZIzd4PM0UFz0f0QDWuVARJAReDih2eMZlpTXa+aSHoG17uDS+SUWAstF0HJQyOvrhqUqrw3PLM+eSImPTzJOsDN77S2mRpZ8qEnokNxTR6Quk7K2xFmu4QtlNm3lpTrytbDLwEYXr4hDpRwIFmRJi8pcUWpH3iu/Mk2sysAF69p7c61BpYmPG14iXQcg5HuSw9XHaUIceNmMZ14Gt7OatqezwOEqZGk7gcEBCfZfwIkCZtYOhslKMDfY19nNNZ74vsDH6wN',
        '_fbp': 'fb.1.1747655891008.318224823318290821',
        'bm_sv': '7FF31353A079F1CC9B0D6C90BB869869~YAAQJdgjF/4Dc8iWAQAAEPJo6BuW5RDJiY1LRxWkZobSuQlQSoJ3G7ho+YpZRavAhbOcc7HTO1bHsES/b3jYewVCdib/sYBb1ulfIIBKKRem0uqenVdMJaQBrvY2QJtZNC9dsxT4W80wko2/t/fAGvADiKBZr0UVT5zLDVahjQxFg6alc29lwegO6GWT8YTznPqfnCZC63rqE042KPqcGyZitSfj6tJcp/xJ9FEop+XNgBslqHIty3KK5ZjjucPIMRVUbPw=~1',
        'cto_bundle': '2ysjQV9QZ3clMkI4bWIlMkJFa2ZvMml1b21yV2NFYmNTbVBWVVEzRHhPTmxKQ01YdXp1bmwwZ29adFdxbEgwTHdoR3UwSiUyRmpWMWxjVmNKdXZpU2N6cnlQVThzbXF4bEdHZExMVXNNd1VRMWhvWFlCcHYzJTJCMWxwVTVTV3JVYjhGTENWc2NMVlNa',
        '_ga_C9F0BWS8KH': 'GS2.1.s1747655890$o1$g1$t1747655945$j0$l0$h0',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://www.costar.com/',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    }

    params = {
        'client_id': 'costar',
        'nonce': '7e746f9b-9ca8-467a-25d1-71e3fb9ba889',
        'response_type': 'code',
        'response_mode': 'form_post',
        'scope': 'openid profile email address phone offline_access product_user session',
        'redirect_uri': 'https://product.costar.com/home/auth-callback',
        'acr_values': '',
        'locale': 'en-US',
    }

    response = session.get('https://secure.costargroup.com/connect/authorize', params=params, cookies=cookies, headers=headers)
    # print(response.headers)
    return response.text
    

def extract(resp):
    tree = etree.HTML(resp)
    signinform = tree.xpath('//form[@id="signinform"]/@action')[0]
    print(signinform) # /login?signin=11.......d736d93e8c1b15ee

    xsrf_token = tree.xpath('//input[@name="idsrv.xsrf"]/@value')[0]
    print(xsrf_token)

    return signinform, xsrf_token
    

if __name__ == '__main__':
    session = requests.session()
    resp = authorize()
    signinform, xsrf_token = extract(resp)
    # params = {
    #     'signin': '77cf101785aa288926c78c091160493e',
    # }

    data = {
        'idsrv.xsrf': xsrf_token,
        'sessionId': '',
        'username': '123456',
        'password': '111',
    }
    url = 'https://secure.costargroup.com' + signinform
    print(url)
    response = session.post(url, data=data)
    print(response.headers)