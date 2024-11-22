import requests
import pprint


def get_rub_salary(vacansies_name):
    url = 'https://api.hh.ru/vacancies'
    payload = {"text": f"{vacansies_name}", 'area': '1',}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    rub_salary = response.json()
    return rub_salary


def get_vacansies_statistic(vacancies_found, vacancies_processed, average_salary):
    vacansies_statistic = {
    'vacancies_found':vacancies_found, 
    'vacancies_processed':vacancies_processed,
    'average_salary': average_salary}
    return vacansies_statistic


# def get_average_salary(all_vacancies):


if __name__ == '__main__':
    predict_rub_salary = {}
    page = 0
    pages = 10
    url = 'https://api.hh.ru/vacancies'
    vacansies_name = ['Java', 'Python', 'Ruby', ]

    for vacansy in vacansies_name:
        vacancies_processed = 0
        vacancies_found = 0
        average_salary = []
        found_vacansy_name = []

        while page < pages:
            page_response = requests.get(url, params={'page': page,"text": f"{vacansy}", 'area': '1'})
            page_response.raise_for_status()
            all_vacancies = page_response.json()
            all_vacancies = all_vacancies['items']
            for salary in all_vacancies:
                programmer_salary = salary['salary']
                vacansy_name = salary['name']
                if vacansy in vacansy_name:
                    found_vacansy_name.append(vacansy_name)
                    if not programmer_salary:
                        continue
                    for money in programmer_salary.keys():
                        if money != 'from':
                            continue
                        if not programmer_salary[money]:
                            continue
                        rounded_programmer_salary = programmer_salary[money] * 1.2
                        average_salary.append(rounded_programmer_salary)
            vacancies_processed += (len(average_salary))
            vacancies_found += (len(found_vacansy_name))
        if average_salary:
            average_salary = sum(average_salary) / len(average_salary)
            average_salary = round(average_salary)
            pages = all_vacancies['pages']
            page += 1

        vacansies_statistic = get_vacansies_statistic(vacancies_found, vacancies_processed, average_salary)
        predict_rub_salary[f'{vacansy}'] = vacansies_statistic
        page = 0

    pprint.pprint(predict_rub_salary)
       
       

