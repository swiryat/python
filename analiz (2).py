import ast
import os
import sys
import traceback
import pandas as pd
from collections import defaultdict
from radon.complexity import cc_visit
import matplotlib.pyplot as plt
import logging
import tkinter as tk
from tkinter import filedialog
import chardet

# Настройка логирования
logging.basicConfig(filename='analysis.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self, language):
        self.analysis_results = []
        self.language = language
        self.potential_prints = []
        self.function_definitions = []
        self.imported_libraries = set()
        self.dangerous_functions = ["eval", "exec"]
        self.other_dangerous_functions = ["input", "open", "os.system", "pickle.loads"]
        self.visited_functions = set()
        self.file_dependencies = defaultdict(set)
        self.analyzed_files = set()
        self.current_file = ""

    def analyze_code_file(self, file_path):
        self.analyze_code_from_file(file_path)
        self.analyze_file_dependencies(file_path)

    def analyze_code_directory(self, dir_path):
        for root, _, files in os.walk(dir_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if file_name.endswith(".py"):
                    self.analyze_code_file(file_path)

    def analyze_code_from_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as file:
                code_content = file.read()
                self.current_file = file_path
                self.analyze_code(code_content)
        except Exception as e:
            self.handle_analysis_error(file_path, e)

    def analyze_file_dependencies(self, file_path):
        try:
            with open(file_path, "rb") as file:
                raw_content = file.read()
                result = chardet.detect(raw_content)
                detected_encoding = result['encoding']
                code_content = raw_content.decode(detected_encoding, errors="replace")
                self.current_file = file_path
                self.analyze_code(code_content)
        except Exception as e:
            self.handle_analysis_error(file_path, e)

    def handle_analysis_error(self, file_path, error):
        error_message = f"Произошла ошибка при анализе файла {file_path}: {error}"
        print(error_message)
        logging.error(error_message)
        traceback.print_exc()
        lines = code_content.split("\n")
        line_number = traceback.extract_tb(error.__traceback__)[-1].lineno
        start_line = max(0, line_number - 3)
        end_line = min(len(lines), line_number + 2)
        context = "\n".join(lines[start_line:end_line])
        logging.error("Контекст ошибки:")
        logging.error(context)

    def analyze_project_structure(self, root_path):
        for root, _, files in os.walk(root_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if file_name.endswith(".py") and file_path not in self.analyzed_files:
                    self.analyze_file_dependencies(file_path)

    def analyze_project_memory_usage(self, root_path):
        for file_path in self.analyzed_files:
            self.analyze_code_from_file(file_path)

    def analyze_dynamic_generated_code(self):
        for file_path in self.analyzed_files:
            self.analyze_code_from_file(file_path)

    def generate_visualization(self, output_file):
        df = pd.DataFrame(self.analysis_results, columns=["File", "Line", "Message"])
        df.to_csv(output_file, index=False)

    def visit_Import(self, node):
        for module in node.names:
            self.imported_libraries.add(module.name)

    def visit_ImportFrom(self, node):
        for module in node.names:
            full_module_name = f"{node.module}.{module.name}"
            self.imported_libraries.add(full_module_name)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            function_name = node.func.id
            if function_name == "print":
                self.potential_prints.append((self.current_file, node.lineno, node.col_offset))
            if function_name in self.dangerous_functions:
                self.analysis_results.append((self.current_file, node.lineno, f"Потенциально опасная функция '{function_name}' вызвана"))
            elif function_name in self.other_dangerous_functions:
                self.analysis_results.append((self.current_file, node.lineno, f"Использование функции '{function_name}' может быть опасным"))

    def visit_FunctionDef(self, node):
        self.function_definitions.append((self.current_file, node.name, node.lineno, node.col_offset))
        self.visited_functions.add(node.name)

    def analyze_code(self, code):
        tree = ast.parse(code)
        self.visit(tree)
        self.analyze_function_calls(tree)
        self.analyze_function_complexity(tree)

    def analyze_function_calls(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                function_name = node.func.id
                if function_name in self.visited_functions:
                    if function_name == "print":
                        arguments = [ast.unparse(arg) for arg in node.args]
                        context = f"Вызов функции '{function_name}' с аргументами: {', '.join(arguments)}"
                        self.analysis_results.append((self.current_file, node.lineno, context))
                    else:
                        self.analysis_results.append((self.current_file, node.lineno, f"Вызов функции '{function_name}' находится внутри другой функции"))

    def analyze_function_complexity(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = cc_visit(node)
                self.analysis_results.append((self.current_file, node.lineno, f"Сложность функции '{node.name}': {complexity}"))

    def analyze_code_complexity(self, code, filename):
        tree = ast.parse(code)
        complexity = cc_visit(tree)
        self.analysis_results.append((filename, 0, f"Сложность кода: {complexity}"))

    def generate_complexity_plot(self, output_file):
        df = pd.DataFrame(self.analysis_results, columns=["File", "Line", "Message"])
        df["Complexity"] = df["Message"].str.extract(r"Сложность кода: (\d+)").astype(float)
        complexity_by_file = df[df["Message"].str.startswith("Сложность кода:")].groupby("File")["Complexity"].mean()
        plt.figure(figsize=(10, 6))
        complexity_by_file.plot(kind="bar", color="skyblue")
        plt.xlabel("Файл")
        plt.ylabel("Средняя сложность кода")
        plt.title("Сложность кода в разных файлах")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_file)
        print("Сохранен график:", output_file)
        plt.close()
        logging.info(f"Сохранен график в файл: {output_file}")

def main():
    logging.basicConfig(filename='analysis.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    if len(sys.argv) < 2:
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if not path:
            print("Отменено.")
            return
    else:
        path = sys.argv[1]

    result_file_path = "analysis_results.csv"
    language = "python"
    
    if os.path.exists(path):
        print(f"Начат анализ пути: {path}")
        logging.info(f"Начат анализ пути: {path}")
        analyzer = CodeAnalyzer(language)
        
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as file:
            code_content = file.read()
        print(f"Анализ файла: {path}")
        logging.info(f"Анализ файла: {path}")
        analyzer.analyze_code_file(path)
        analyzer.analyze_code_complexity(code_content, path)

    if os.path.isdir(path):
        print(f"Анализ директории: {path}")
        logging.info(f"Анализ директории: {path}")
        analyzer.analyze_code_directory(path)
        analyzer.analyze_project_structure(path)
        analyzer.analyze_project_memory_usage(path)
        analyzer.analyze_dynamic_generated_code()
        analyzer.generate_visualization(result_file_path)
            
        output_file = "complexity_plot.png"
        analyzer.generate_complexity_plot(os.path.join(os.getcwd(), output_file))
        print(f"Сгенерирован график сложности: {output_file}")
        logging.info(f"Сгенерирован график сложности: {output_file}")
            
        output_file = "graf.png"
        analyzer.generate_complexity_plot(os.path.join(os.getcwd(), output_file))
        print(f"Сгенерирован график: {output_file}")
        logging.info(f"Сгенерирован график: {output_file}")
    else:
        print("Файл или директория не найдены.")
        logging.error("Файл или директория не найдены.")

if __name__ == "__main__":
    main()
