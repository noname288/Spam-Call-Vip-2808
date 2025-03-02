
import requests
import time
import random
import os
from concurrent.futures import ThreadPoolExecutor

class SpamAPI:
    def __init__(self):
        self.api_endpoints = {
            "call_1": "https://api.example.com/call",
            "call_2": "https://api.example2.com/call",
            "sms_1": "https://api.example.com/sms",
            "sms_2": "https://api.example2.com/sms"
        }
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (X11; Linux x86_64; rv:78.0)"
        ]
        
    def format_phone(self, phone):
        """Chuẩn hóa số điện thoại"""
        phone = str(phone).strip()
        if phone.startswith("+84"):
            return phone
        elif phone.startswith("84"):
            return "+" + phone
        elif phone.startswith("0"):
            return "+84" + phone[1:]
        return "+84" + phone
    
    def call_api(self, phone_number, num_calls=1):
        """API gọi điện thoại"""
        formatted_phone = self.format_phone(phone_number)
        success_count = 0
        
        for _ in range(num_calls):
            # Lựa chọn ngẫu nhiên API endpoint
            api_endpoint = random.choice([self.api_endpoints["call_1"], self.api_endpoints["call_2"]])
            user_agent = random.choice(self.user_agents)
            
            headers = {
                'User-Agent': user_agent,
                'Content-Type': 'application/json'
            }
            
            payload = {
                'phone_number': formatted_phone,
                'service_type': 'verification',
                'timestamp': int(time.time())
            }
            
            try:
                # Mô phỏng gọi API (trong thực tế sẽ gửi request thật)
                # response = requests.post(api_endpoint, json=payload, headers=headers)
                print(f"[CALL] Đã gọi đến {formatted_phone} qua API {api_endpoint}")
                success_count += 1
                time.sleep(1)  # Đợi 1 giây giữa các cuộc gọi
            except Exception as e:
                print(f"[ERROR] Lỗi khi gọi điện: {str(e)}")
        
        return success_count
    
    def sms_api(self, phone_number, num_sms=1):
        """API gửi tin nhắn SMS"""
        formatted_phone = self.format_phone(phone_number)
        success_count = 0
        
        for _ in range(num_sms):
            # Lựa chọn ngẫu nhiên API endpoint
            api_endpoint = random.choice([self.api_endpoints["sms_1"], self.api_endpoints["sms_2"]])
            user_agent = random.choice(self.user_agents)
            
            headers = {
                'User-Agent': user_agent,
                'Content-Type': 'application/json'
            }
            
            payload = {
                'phone_number': formatted_phone,
                'message': 'Mã xác thực của bạn là: ' + str(random.randint(1000, 9999)),
                'timestamp': int(time.time())
            }
            
            try:
                # Mô phỏng gửi API (trong thực tế sẽ gửi request thật)
                # response = requests.post(api_endpoint, json=payload, headers=headers)
                print(f"[SMS] Đã gửi SMS đến {formatted_phone} qua API {api_endpoint}")
                success_count += 1
                time.sleep(1)  # Đợi 1 giây giữa các SMS
            except Exception as e:
                print(f"[ERROR] Lỗi khi gửi SMS: {str(e)}")
        
        return success_count
    
    def multi_service_attack(self, phone_number, num_calls=5, num_sms=5):
        """Tấn công đa dịch vụ (gọi điện + SMS)"""
        with ThreadPoolExecutor(max_workers=2) as executor:
            call_future = executor.submit(self.call_api, phone_number, num_calls)
            sms_future = executor.submit(self.sms_api, phone_number, num_sms)
            
            call_results = call_future.result()
            sms_results = sms_future.result()
            
        return {
            "calls_sent": call_results,
            "sms_sent": sms_results
        }

def main():
    # Lấy số điện thoại từ người dùng
    print("=== HỆ THỐNG SPAM CALL/SMS ===")
    phone_input = input("Nhập số điện thoại cần spam: ")
    
    try:
        num_calls = int(input("Số lượng cuộc gọi (mặc định 5): ") or "5")
        num_sms = int(input("Số lượng SMS (mặc định 5): ") or "5")
    except ValueError:
        print("Số lượng không hợp lệ, sử dụng giá trị mặc định")
        num_calls = 5
        num_sms = 5
    
    api = SpamAPI()
    print(f"\nĐang bắt đầu tấn công số {phone_input}...")
    
    results = api.multi_service_attack(phone_input, num_calls, num_sms)
    
    print("\n=== KẾT QUẢ ===")
    print(f"Đã gửi thành công {results['calls_sent']}/{num_calls} cuộc gọi")
    print(f"Đã gửi thành công {results['sms_sent']}/{num_sms} tin nhắn SMS")

if __name__ == "__main__":
    main()
