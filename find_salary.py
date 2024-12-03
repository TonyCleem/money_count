def get_salary(salary_from, salary_to):
	if not salary_from and not salary_to:
		return None
	if salary_from and salary_to:
		return salary_from + salary_to / 2
	if not salary_from:
		return salary_to * 0.8
	if not salary_to:
		return salary_from * 1.2
	

