import os
from dotenv import load_dotenv
from terminaltables import DoubleTable
from average_salary_how_int import get_average_salary_how_int
from create_table import create_table_rub_salary
from all_vacancies import get_all_vacancies


def predict_rub_salary_from_hh(language, vacancies_found, vacancies_processed, average_salary, hh_pages):
    url = 'https://api.hh.ru/vacancies'
    page = 0
    area = 1
    while page < hh_pages:
        params = {'page': page,"text": f"{language}", 'area': area}
        all_vacancies = get_all_vacancies(url, params)
        all_vacancies_programmers = all_vacancies['items']

        for vacancy_programmer in all_vacancies_programmers:
            if not vacancy_programmer['salary']:
                continue
            vacancies_found += 1
            salaries = vacancy_programmer['salary']
            for salary in salaries:
                if salary == 'from' and salaries[salary]:
                    money = salaries[salary] * 0.8
                    average_salary.append(int(money))
                    vacancies_processed += 1

        # hh_pages = all_vacancies['pages']                   
        page += 1
    
    rub_salary_from_hh = language, vacancies_found, vacancies_processed, average_salary
    return rub_salary_from_hh


def predict_rub_salary_from_superjob(language, vacancies_found, vacancies_processed, average_salary, superjob_key, sj_pages, count=100):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    page = 0
    t = 4
    catalogues = 48
    while page < sj_pages:
        headers = {'X-Api-App-Id': superjob_key}
        params = {'page': page, 'count': count, 'keyword': f'{language}', 't': t, 'catalogues': catalogues}

        all_vacansies = get_all_vacancies(url, params, headers)
        all_vacancies_programmers = all_vacansies['objects']

        for vacancy_programmer in all_vacancies_programmers:
            vacancies_found += 1
            payment_from = vacancy_programmer['payment_from']   
            if payment_from:
                payment = payment_from * 0.8
                average_salary.append(int(payment))
                vacancies_processed += 1
        page += 1

    rub_salary_from_superjob = language, vacancies_found, vacancies_processed, average_salary
    return rub_salary_from_superjob
 

if __name__ == '__main__':
    load_dotenv()
    superjob_key = os.environ['SUPERJOB_KEY']

    salaries_sj = []
    salaries_hh = []

    languages = ['Python', 'C#', 'C++', 'Java', 'JS', '1С']
    for language in languages:
        page = 0
        sj_pages = 5
        hh_pages = 5
        average_salary = []
        vacancies_found = 0
        vacancies_processed = 0

        salary_predictions_from_superjob = predict_rub_salary_from_superjob(language, vacancies_found, vacancies_processed, average_salary, superjob_key, sj_pages)
        salaries_sj.append(salary_predictions_from_superjob)

        salary_predictions_from_hh = predict_rub_salary_from_hh(language, vacancies_found, vacancies_processed, average_salary, hh_pages)
        salaries_hh.append(salary_predictions_from_hh)

    table_salaies_sj = create_table_rub_salary(salaries_sj, 'SuperJob Moscow')
    table_salaies_hh = create_table_rub_salary(salaries_hh, 'HeadHunter Moscow')

    print(table_salaies_sj.table)
    print()
    print(table_salaies_hh.table)
    print()

    

