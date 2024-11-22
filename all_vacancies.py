import requests


def get_all_vacancies(url, params=None, headers=None):
    page_response = requests.get(url, headers=headers, params=params)
    page_response.raise_for_status()
    all_vacancies = page_response.json()
    return all_vacancies