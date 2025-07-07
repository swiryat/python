import requests

api_key = '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'

def generate_text(prompt):
    url = 'https://api.openai.com/v1/engines/gpt-3.5-turbo/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    data = {
        'prompt': prompt,
        'max_tokens': 50,  # Максимальное количество токенов в ответе
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['text']
    else:
        return 'Ошибка при запросе к GPT API'

if __name__ == '__main__':
    prompt = 'Напишите текст о '
    response_text = generate_text(prompt)
    print(response_text)
