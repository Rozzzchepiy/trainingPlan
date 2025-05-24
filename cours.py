import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Програма")
        self.geometry("1000x600")
        
        self.calculated_max = None
        
        style = ttk.Style()
        style.configure("Gray.TFrame", borderwidth=1, relief="solid")

        # Налаштування стилю для Notebook (зсув кнопок вниз)
        style.configure("TNotebook", padding=[0, 20, 0, 20])
        style.configure("TNotebook.Tab", padding=[5, 0, 5, 0])  # Додатковий padding для кожної вкладки
        
        # Створення вкладок
        notebook = ttk.Notebook(self)
        notebook.pack()

        # Вкладка 1
        max_tab = MaxCalculate(notebook, self)
        notebook.add(max_tab, text="Розрахунок максимуму")

        # Вкладка 2
        plan_tab = PlanTrainings(notebook, self)
        notebook.add(plan_tab, text="Планування тренувань")



class MaxCalculate(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, style="Gray.TFrame", width=950, height=550)  # Фіксовані розміри
        self.pack_propagate(False)
        self.app = app
        
        
        # Заголовок
        title_label = tk.Label(self, text="Введіть дані про вашу вправу", font=("Arial", 14, "bold"))
        title_label.pack(pady=(20, 0))
        
        # Основний фрейм
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=20, padx=50, fill="x")
        
        # Поле "Вага (кг)"
        weight_frame = ttk.Frame(main_frame)
        weight_frame.pack(fill="x", pady=(0, 15))
        
        weight_label = tk.Label(weight_frame, text="Вага (кг):", font=("Arial", 11))
        weight_label.pack(anchor="w")
        
        self.weight_entry = tk.Spinbox(weight_frame, from_=0, to=500, increment=1, font=("Arial", 11), wrap=True, relief="solid", bd=1)
        self.weight_entry.pack(fill="x", pady=(5, 0))
        
        # Повторення 
        reps_frame = ttk.Frame(main_frame)
        reps_frame.pack(fill="x", pady=(0, 15))
        
        reps_label = tk.Label(reps_frame, text="Кількість повторень:", font=("Arial", 11))
        reps_label.pack(anchor="w")
        
        self.reps_entry = tk.Spinbox(reps_frame, from_=0, to=36, increment=1, font=("Arial", 11), wrap=True, relief="solid", bd=1)
        self.reps_entry.pack(fill="x", pady=(5, 0))
        
        # Формула розрахунку
        formula_frame = ttk.Frame(main_frame)
        formula_frame.pack(fill="x", pady=(0, 30))
        
        formula_label = tk.Label(formula_frame, text="Формула розрахунку:", 
                                font=("Arial", 11))
        formula_label.pack(anchor="w")
        
        # Комбобокс для вибору формули
        self.formula_var = tk.StringVar(value="O'Conner")
        self.formula_combobox = ttk.Combobox(formula_frame, 
                                           textvariable=self.formula_var,
                                           values=["O'Conner", "Brzycki", "Epley", "Lander"],
                                           state="readonly",
                                           font=("Arial", 11),
                                           )
        self.formula_combobox.pack(fill="x", pady=(5, 0))
        
        # Розрахунок
        self.calculate_button = tk.Button(main_frame, text="Розрахувати максимум", font=("Arial", 11), 
                                        relief="solid",
                                        bd=1,
                                        cursor="hand2",
                                        command=self.calculate_max)
        self.calculate_button.pack(pady=(10, 0))
        
        # Результат
        self.result_frame = ttk.Frame(main_frame)
        self.result_frame.pack(fill="x", pady=(20, 0))
        
        self.result_label = tk.Label(self.result_frame, text="", 
                                   font=("Arial", 12, "bold"))
        self.result_label.pack()
    
    def calculate_max(self):
        """Розрахунок максимуму за обраною формулою"""
        try:
            weight = float(self.weight_entry.get())
            reps = int(self.reps_entry.get())
            formula = self.formula_var.get()
            
            if weight <= 0 or reps <= 0:
                raise ValueError("Значення мають бути більше нуля")
            
            # Формули розрахунку 1RM (One Rep Max)
            if formula == "O'Conner":
                max_weight = weight * (1 + 0.025 * reps)
            elif formula == "Brzycki":
                max_weight = weight * (36 / (37 - reps))
            elif formula == "Epley":
                max_weight = weight * (1 + reps / 30)
            elif formula == "Lander":
                max_weight = (100 * weight) / (101.3 - 2.67123 * reps)
            else:
                max_weight = weight * (1 + 0.025 * reps)  # За замовчуванням O'Conner
                
            self.app.calculated_max = max_weight
            self.result_label.config(text=f"Ваш максимум: {max_weight:.1f} кг", fg="green")
            
        except ValueError as e:
            if "could not convert string to float" in str(e) or "invalid literal" in str(e):
                self.result_label.config(text="Помилка: Введіть коректні числові значення", fg="red")
            else:
                self.result_label.config(text=f"Помилка: {str(e)}", fg="red")
        except Exception as e:
            self.result_label.config(text="Помилка розрахунку", fg="red")        
        
        
        
class PlanTrainings(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, style="Gray.TFrame") 
        self.pack_propagate(False)
        self.app = app
        
        # Заголовок
        title_label = tk.Label(self, text="Налаштування плану тренувань", font=("Arial", 14, "bold"))
        title_label.pack(pady=(20, 0))
        
        # Основний фрейм
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=20, padx=50, fill="x")
        
        # поточний 1RM
        weight_frame = ttk.Frame(main_frame)
        weight_frame.pack(fill="x", pady=(0, 15))
        
        weight_label = tk.Label(weight_frame, text="Поточний максимум 1RM (кг):", font=("Arial", 11))
        weight_label.pack(anchor="w")
        
        self.weight_entry = tk.Spinbox(weight_frame, from_=0, to=500, increment=1, font=("Arial", 11), wrap=True, relief="solid", bd=1)
        self.weight_entry.pack(fill="x", pady=(5, 0))
        
        
        # Ціль 
        reps_frame = ttk.Frame(main_frame)
        reps_frame.pack(fill="x", pady=(0, 15))
        
        reps_label = tk.Label(reps_frame, text="Цільовий максимум 1RM (кг):", font=("Arial", 11))
        reps_label.pack(anchor="w")
        
        self.reps_entry = tk.Spinbox(reps_frame, from_=0, to=500, increment=1, font=("Arial", 11), wrap=True, relief="solid", bd=1)
        self.reps_entry.pack(fill="x", pady=(5, 0))

        # Дата початку тренувань
        data_frame = ttk.Frame(main_frame)
        data_frame.pack(fill="x", pady=(0, 15))
        
        data_label = ttk.Label(data_frame, text="Старт плану", font=("Arial", 11))
        data_label.pack(anchor="w")
        
        self.date_entry = ttk.Entry(data_frame, font=("Arial", 11))
        self.date_entry.pack(fill="x", pady=(5, 0))
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))


        self.day_vars = []
        days_frame = ttk.Frame(main_frame)
        days_frame.pack(fill="x", pady=(5, 0))
        
        
        days_label = tk.Label(days_frame, text="Оберіть дні ваших тренувань:", font=("Arial", 11))
        days_label.pack(anchor="w")
        
       
        # Чекбокси для вибору днів тренувань
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
        for i, day in enumerate(days):
            var = tk.IntVar()
            cb = ttk.Checkbutton(days_frame, text=day, variable=var)
            cb.pack(side="left", padx=5, pady=5)
            self.day_vars.append((var, i)) 
        
        button_frame = tk.Frame(main_frame)  
        button_frame.pack(pady=(10, 0))
        
        # використання 1RM
        self.calculate_button = tk.Button(button_frame, text="Використати розрахованний 1RM", font=("Arial", 11), 
                                        relief="solid",
                                        bd=1,
                                        cursor="hand2",
                                        command=self.use_calculated_max)
        self.calculate_button.pack(side="left", padx=5)
        
        # Розрахунок
        self.calculate_button = tk.Button(button_frame, text="Згенерувати план", font=("Arial", 11), 
                                        relief="solid",
                                        bd=1,
                                        cursor="hand2")
        self.calculate_button.pack(side="left")
        
    def use_calculated_max(self):
        """Вставка розрахованого максимуму у поле"""
        if self.app.calculated_max is not None:
            self.weight_entry.delete(0, tk.END)
            self.weight_entry.insert(0, str(round(self.app.calculated_max, 1)))
        else:
            tk.messagebox.showwarning("Увага", "Спочатку розрахуйте максимум на вкладці 'Розрахунок максимуму'")
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
