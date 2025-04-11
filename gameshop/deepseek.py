import requests
import logging


class DeepSeekAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }

        # Настройка логирования
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def generate_answer(self, question: str) -> str:
        """
        Генерирует ответ через DeepSeek API
        """
        payload = {
            "model": "deepseek-ai/DeepSeek-R1",
            "messages": [
                {
                    "role": "system",
                    "content": "Russian Sanecka Bot 3000 "
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }

        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()

            data = response.json()

            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content'].strip()

            return "⚠ Не удалось получить ответ"

        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            return "🔑 Ошибка доступа"

        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            return "⚠ Ошибка обработки"