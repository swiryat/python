class Job:
    def __init__(self, profession):
        self.profession = profession
        self.vacancies = []


    def show_vacancies(self):
        if not self.vacancies:
            print("Пока нет вакансий на данную профессию")
        else:
            for vacancy in self.vacancies:
                print(f"{vacancy['company']}: зарплата {vacancy['salary']}тыс,+
                требуемый опыт {vacancy['experience']}")


    def post_vacancy(self, company, salary, experience):
        self.vacancies.append({"company": company, "salary": salary, "experience": experience})


    def find_best_vacancy(self, exp, profession, min_salary):
        if profession != self.profession:
            print(f"Кажется, вы ищете вакансии {profession}+
            в разделе {self.profession}. Выберите другой раздел.")
            return

        best_vacancy = None
        for vacancy in self.vacancies:
            if vacancy["experience"] <= exp and vacancy["salary"] >= min_salary:
                if best_vacancy is None or vacancy["salary"] >+
                best_vacancy["salary"]:
                    best_vacancy = vacancy

        if best_vacancy is not None:
            print(f"Наилучшая вакансия для вас в компании+
            {best_vacancy['company']} с+
            зарплатой {best_vacancy['salary']} тыс.")
            self.vacancies.remove(best_vacancy)
        else:
            print("Простите, для вас не нашлось вакансий.")


    def update_salary(self, company, new_salary):
        for vacancy in self.vacancies:
            if vacancy["company"] == company:
                vacancy["salary"] = new_salary
                break
