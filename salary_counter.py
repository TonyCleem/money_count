import os
from dotenv import load_dotenv
from terminaltables import DoubleTable
from create_table import create_table_rub_salary
from all_vacancies import get_all_vacancies
from find_salary import get_salary


def predict_rub_salary_from_hh(language):
    url = 'https://api.hh.ru/vacancies'
    page = 0
    pages = 1
    area = 1
    average_salary = 0
    vacancies_found = 0
    vacancies_processed = 0

    while page < pages:
        params = {'page': page,"text": f"{language}", 'area': area}
        all_vacancies = get_all_vacancies(url, params)
        all_vacancies_programmers = all_vacancies['items']

        for vacancy_programmer in all_vacancies_programmers:
            if not vacancy_programmer['salary']:
                continue
            vacancies_found += 1
            salaries = vacancy_programmer['salary']
            discovered_salary = get_salary(salaries['from'], salaries['to'])
            if not discovered_salary:
                continue
            average_salary += discovered_salary
            vacancies_processed += 1

        pages = all_vacancies['pages']                   
        page += 1

    if average_salary:
        average_salary = average_salary / vacancies_processed
        rub_salary_from_hh = vacancies_found, vacancies_processed, int(average_salary)
        return rub_salary_from_hh
    return None


def predict_rub_salary_from_superjob(language):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    page = 0
    t = 4
    count = 100
    catalogues = 48
    average_salary = 0
    vacancies_found = 0
    vacancies_processed = 0
    pages = 5

    while page < pages:
        headers = {'X-Api-App-Id': superjob_key}
        params = {'page': page, 'count': count, 'keyword': f'{language}', 't': t, 'catalogues': catalogues}
        all_vacansies = get_all_vacancies(url, params, headers)
        all_vacancies_programmers = all_vacansies['objects']

        for vacancy_programmer in all_vacancies_programmers:
            vacancies_found += 1
            discovered_salary = get_salary(vacancy_programmer['payment_from'], vacancy_programmer['payment_to'])
            if not discovered_salary:
                continue
            average_salary += discovered_salary
            vacancies_processed += 1
        page += 1

    if average_salary:
        average_salary = average_salary / vacancies_processed
        rub_salary_from_sj = vacancies_found, vacancies_processed, int(average_salary)
        return rub_salary_from_sj
    return None

        
if __name__ == '__main__':
    load_dotenv()
    superjob_key = os.environ['SUPERJOB_KEY']

    languages = ['Python', 'C#', 'C++', 'Java', 'JS', '1С']

    salaries_sj = []
    salaries_hh = []

    for language in languages:
        rub_salary_from_sj = predict_rub_salary_from_superjob(language)
        rub_salary_from_hh = predict_rub_salary_from_hh(language)
        
        if rub_salary_from_sj:
            rub_salary_from_sj = [f'{language}', *rub_salary_from_sj]
            salaries_sj.append(rub_salary_from_sj)

        if rub_salary_from_hh:
            rub_salary_from_hh = [f'{language}', *rub_salary_from_hh]
            salaries_hh.append(rub_salary_from_hh)

    table_salaries_hh = create_table_rub_salary(salaries_hh, 'HeadHunter Moscow')
    table_salaries_sj = create_table_rub_salary(salaries_sj, 'SuperJob Moscow')

    print(table_salaies_hh.table)
    print()
    print(table_salaies_sj.table)
    print()


 

    





    

