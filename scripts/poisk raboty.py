class Job:
    def __init__(self, profession):
        self.profession = profession
        self.vacancies = []

    def post_vacancy(self, company, salary, min_exp):
        vacancy = {"company": company, "salary": salary, "min_exp": min_exp}
        self.vacancies.append(vacancy)

    def close_vacancy(self, company):
        self.vacancies = [v for v in self.vacancies if v["company"] != company]

    def update_salary(self, company, new_salary):
        for vacancy in self.vacancies:
            if vacancy["company"] == company:
                vacancy["salary"] = new_salary

    def update_exp(self, company, new_exp):
        for vacancy in self.vacancies:
            if vacancy["company"] == company:
                vacancy["min_exp"] = new_exp

    def show_vacancies(self):
        print(f"{self.profession}:")
        if not self.vacancies:
            print("Пока нет вакансий на данную профессию")
        else:
            for vacancy in self.vacancies:
                print(
                    f'"{vacancy["company"]}": зарплата {vacancy["salary"]} тыс, требуемый опыт {vacancy["min_exp"]}')

    def find_best_vacancy(self, exp, profession, min_salary):
        if profession != self.profession:
            print(f"Кажется, вы ищете вакансии в разделе {self.profession}. Выберите другой раздел.")
            return

        best_vacancy = None
        for vacancy in self.vacancies:
            if vacancy["min_exp"] <= exp and vacancy["salary"] >= min_salary:
                if best_vacancy is None or vacancy["salary"] > best_vacancy["salary"]:
                    best_vacancy = vacancy

        if best_vacancy:
            print(
                f"Наилучшая вакансия для вас в компании {best_vacancy['company']} с зарплатой {best_vacancy['salary']} тыс.")
            self.close_vacancy(best_vacancy["company"])
        else:
            print("Простите, для вас не нашлось вакансий.")

# Примеры использования
loyer = Job('loyer')
loyer.show_vacancies()
loyer.post_vacancy('Хорошие юристы', 300, 15)
loyer.show_vacancies()

# Далее продолжайте вызывать методы на объекте loyer без создания новых экземпляров.
loyer.post_vacancy('Делу время', 100, 5)
loyer.post_vacancy('BTS', 176, 0)
loyer.show_vacancies()
loyer.find_best_vacancy(10, 'doctor', 200)
loyer.find_best_vacancy(6, 'loyer', 100)
loyer.update_salary('Делу время', 150)
loyer.show_vacancies()
