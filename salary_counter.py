import os
from dotenv import load_dotenv
from terminaltables import DoubleTable
from create_table import create_table_rub_salary
from all_vacancies import get_all_vacancies


def predict_rub_salary_from_hh(language):
    url = 'https://api.hh.ru/vacancies'
    page = 0
    area = 1
    average_salary = 0
    vacancies_found = 0
    vacancies_processed = 0


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
                    average_salary += money
                    vacancies_processed += 1

        # hh_pages = all_vacancies['pages']                   
        page += 1
    if average_salary:
        average_salary = average_salary / vacancies_processed

    rub_salary_from_hh = language, vacancies_found, vacancies_processed, int(average_salary)
    return rub_salary_from_hh


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
                average_salary += payment
                vacancies_processed += 1
        page += 1

        if average_salary:
            average_salary = average_salary / vacancies_processed

        rub_salary_from_sj = language, vacancies_found, vacancies_processed, int(average_salary)
        
        return rub_salary_from_sj

 
if __name__ == '__main__':
    load_dotenv()
    superjob_key = os.environ['SUPERJOB_KEY']

    table_header = [
    ('Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата')
    ]

    languages = ['Python', 'C#', 'C++', 'Java', 'JS', '1С']

    for language in languages:
        sj_pages = 5
        hh_pages = 5

        rub_salary_from_sj = [predict_rub_salary_from_superjob(language)]


        


    # print(salary_from_superjob)
    # print(salary_from_hh)

    # table_salaies_hh = create_table_rub_salary(salary_from_hh, 'HeadHunter Moscow')
    # table_salaies_sj = create_table_rub_salary(salary_from_superjob, 'SuperJob Moscow')



    # print(table_salaies_hh.table)
    # print()

    # print(table_salaies_sj.table)
    # print()




    

