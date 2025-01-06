class Logger:
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

    @classmethod
    def init(cls):
        log_dir = os.path.dirname(cls.log_file_path)
        # 로그 디렉토리가 존재하지 않으면 생성
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    @classmethod
    def log_conversation(cls, chatbot_type, user_message, bot_response, user_ip):
        # """
        # 대화 내용을 로그 파일에 기록합니다.
        
        # :param chatbot_type: 챗봇 유형 (A 또는 B)
        # :param user_message: 사용자가 보낸 메시지
        # :param bot_response: 챗봇의 응답
        # :param user_ip: 사용자의 IP 주소
        # """
        masked_ip = mask_ip(user_ip)  # IP 주소 마스킹
        
        log_entry = f"[{datetime.utcnow().isoformat()}] IP: {masked_ip} | Chatbot: {chatbot_type}\n"
        log_entry += f"User: {user_message}\nBot: {bot_response}\n\n"
        
        try:
            with open(cls.log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(log_entry)
        except Exception as e:
            print(f"Error logging conversation: {e}")
    @staticmethod
    def mask_ip(ip_address):
        # """
        # IP 주소를 마스킹하여 앞 2자리와 뒤 3자리만 표시합니다.
        # 예: '192.168.1.10' -> '19*****010'
        
        # :param ip_address: 원본 IP 주소 문자열
        # :return: 마스킹된 IP 주소 문자열
        # """
        if not ip_address or len(ip_address) < 5:
            return 'Unknown'
        
        # IP 주소에서 숫자와 점(.)만 추출
        clean_ip = re.sub(r'[^0-9.]', '', ip_address)
        
        # 길이에 따라 마스킹 처리
        if len(clean_ip) <= 5:
            return clean_ip  # 너무 짧으면 그대로 반환
        else:
            return f"{clean_ip[:2]}{'*' * (len(clean_ip) - 5)}{clean_ip[-3:]}"
        