import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from tkinter import messagebox
import csv

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
        style.configure("TNotebook.Tab", padding=[5, 0, 5, 0]) 
        
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
        super().__init__(parent, style="Gray.TFrame", width=950, height=550) 
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
            
            if formula == "O'Conner":
                max_weight = weight * (1 + 0.025 * reps)
            elif formula == "Brzycki":
                max_weight = weight * (36 / (37 - reps))
            elif formula == "Epley":
                max_weight = weight * (1 + reps / 30)
            elif formula == "Lander":
                max_weight = (100 * weight) / (101.3 - 2.67123 * reps)
            else:
                max_weight = weight * (1 + 0.025 * reps)  # O'Conner
                
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
        super().__init__(parent, style="Gray.TFrame", width=950, height=550)  
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
        target = ttk.Frame(main_frame)
        target.pack(fill="x", pady=(0, 15))
        
        target_label = tk.Label(target, text="Цільовий максимум 1RM (кг):", font=("Arial", 11))
        target_label.pack(anchor="w")
        
        self.target_entry = tk.Spinbox(target, from_=0, to=500, increment=5, font=("Arial", 11), wrap=True, relief="solid", bd=1)
        self.target_entry.pack(fill="x", pady=(5, 0))

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
                                        cursor="hand2",
                                        command=self.generate_workout_plan)
        self.calculate_button.pack(side="left")
        
        
    
        
    def use_calculated_max(self):
        """Вставка розрахованого максимуму у поле"""
        if self.app.calculated_max is not None:
            self.weight_entry.delete(0, tk.END)
            self.weight_entry.insert(0, str(round(self.app.calculated_max, 1)))
        else:
            tk.messagebox.showwarning("Увага", "Спочатку розрахуйте максимум на вкладці 'Розрахунок максимуму'")
            
    def round_to_standard_weight(self, weight):
        """Округлення ваги до стандартних блисків (2.5 кг)"""
        return round(weight / 2.5) * 2.5
            
    def generate_workout_plan(self):
        """Генерація плану тренувань на основі введених даних"""
        try:
            current_max = float(self.weight_entry.get())
            target_max = float(self.target_entry.get())
            start_date = datetime.strptime(self.date_entry.get(), "%Y-%m-%d")
            selected_days = [i for var, i in self.day_vars if var.get() == 1]
            
            if not selected_days:
                raise ValueError("Оберіть хоча б один день для тренувань")
            if current_max <= 0 or target_max <= 0:
                raise ValueError("Максимум має бути більше нуля")
            if current_max >= target_max:
                raise ValueError("Поточний максимум має бути меншим за цільовий")
            
            # Генерація плану тренувань
            base_weight = self.round_to_standard_weight(current_max * 0.8)
            plan = []
            cycle_number = 1
            training_number = 1
            
            while base_weight < target_max * 0.8 + 2.5:
                plan.append({
                    "Цикл": cycle_number,
                    "Тренування": training_number,
                    "Вага": base_weight,
                    "Підходи": "4",
                    "Повторення": "8"
                })
                training_number += 1
                
                plan.append({
                    "Цикл": cycle_number,
                    "Тренування": training_number,
                    "Вага": base_weight + 2.5,
                    "Підходи": "5",
                    "Повторення": "6"
                })
                training_number += 1
                
                plan.append({
                    "Цикл": cycle_number,
                    "Тренування": training_number,
                    "Вага": base_weight + 5,
                    "Підходи": "6",
                    "Повторення": "4"
                })
                training_number += 1
                
                plan.append({
                    "Цикл": cycle_number,
                    "Тренування": training_number,
                    "Вага": base_weight + 7.5,
                    "Підходи": "6",
                    "Повторення": "2"
                })
                training_number += 1
                
                base_weight += 2.5
                cycle_number += 1
            
            if len(plan) % 4 != 0:
                remaining_trainings = 4 - (len(plan) % 4)
                for i in range(remaining_trainings):
                    if i == 0:
                        plan.append({
                            "Цикл": cycle_number,
                            "Тренування": training_number,
                            "Вага": base_weight,
                            "Підходи": "4",
                            "Повторення": "8"
                        })
                    elif i == 1:
                        plan.append({
                            "Цикл": cycle_number,
                            "Тренування": training_number,
                            "Підходи": "5",
                            "Повторення": "6"
                        })
                    elif i == 2:
                        plan.append({
                            "Цикл": cycle_number,
                            "Тренування": training_number,
                            "Вага": base_weight + 5,
                            "Підходи": "6",
                            "Повторення": "4"
                        })
                    else:
                        plan.append({
                            "Цикл": cycle_number,
                            "Тренування": training_number,
                            "Вага": base_weight + 7.5,
                            "Підходи": "6",
                            "Повторення": "2"
                        })
                    training_number += 1
            
            current_date = start_date
            
            # Знаходимо перший вибраний день, який є після початкової дати або в той самий день
            while True:
                if current_date.weekday() in selected_days:
                    break
                current_date += timedelta(days=1)
            
            # Додаємо дати до плану
            for item in plan:
                item["Дата"] = current_date.strftime("%Y-%m-%d")
                
                # Знаходимо наступний вибраний день
                while True:
                    current_date += timedelta(days=1)
                    if current_date.weekday() in selected_days:
                        break
            
            # Відображення плану 
            self.show_workout_plan(plan)
            
        except ValueError as e:
            messagebox.showerror("Помилка", f"Невірні дані: {str(e)}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Сталася помилка: {str(e)}")
    
    def show_workout_plan(self, plan):
        plan_window = tk.Toplevel(self)
        plan_window.title("План тренувань")
        plan_window.geometry("1000x700")
        plan_window.configure(bg="#f0f0f0")
        
        window_width = 1050
        window_height = 700
        screen_width = plan_window.winfo_screenwidth()
        screen_height = plan_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        plan_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        style = ttk.Style()
        style.configure("Treeview", 
                    font=("Arial", 10), 
                    rowheight=25)
        style.configure("Treeview.Heading", 
                    font=("Arial", 11, "bold"),
                    foreground="black")
    
        title_frame = tk.Frame(plan_window)
        title_frame.pack(pady=(10, 15))
        
        title_label = tk.Label(title_frame, 
                            text="Ваш персональний план тренувань", 
                            font=("Arial", 16, "bold"))
        title_label.pack()
        
        container = tk.Frame(plan_window)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Створення Treeview
        columns = ("Цикл", "Тренування", "Дата", "Вага (кг)", "Підходи", "Повторення")
        tree = ttk.Treeview(container, columns=columns, show="headings")
        
        # Налаштування стовпців
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        
        # Спеціальні налаштування для тренування та Дата
        tree.column("Дата", width=180)
        tree.column("Тренування", width=200)
        
        for item in plan:
            tree.insert("", "end", values=(
                item["Цикл"],
                item["Тренування"],
                item["Дата"],
                item["Вага"],
                item["Підходи"],
                item["Повторення"]
            ))
        
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Налаштування розтягування
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        button_frame = tk.Frame(plan_window)
        button_frame.pack(pady=(10, 15))
        
        button_style = {"font": ("Arial", 11), 
                    "bg": "#4CAF50", 
                    "fg": "white",
                    "activebackground": "#45a049",
                    "activeforeground": "white",
                    "borderwidth": 1,
                    "relief": "raised",
                    "padx": 15,
                    "pady": 5}
        
        export_button = tk.Button(button_frame, 
                                text="Експорт у CSV", 
                                command=lambda: self.export_to_csv(plan),
                                **button_style)
        export_button.pack(side="left", padx=10)
        
        close_button = tk.Button(button_frame, 
                            text="Закрити", 
                            command=plan_window.destroy,
                            **{**button_style, "bg": "#f44336", "activebackground": "#d32f2f"})
        close_button.pack(side="left", padx=10)
        
        # Додаткові налаштування Treeview
        tree.tag_configure('oddrow', background="#f9f9f9")
        tree.tag_configure('evenrow', background="#ffffff")
        
        # Додавання альтернативного кольору рядків
        for i, item in enumerate(tree.get_children()):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree.item(item, tags=(tag,))

    def export_to_csv(self, plan):
        """Експорт плану тренувань у CSV файл"""
        try:
            file_path = tk.filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV файли", "*.csv"), ("Текстові файли", "*.txt"), ("Усі файли", "*.*")],
                title="Зберегти план тренувань як...",
                initialfile="Мій_план_тренувань.csv"
            )
            
            if not file_path:
                return
                
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['Цикл', 'Тренування', 'Дата', 'Вага (кг)', 'Підходи', 'Повторення']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
                
                writer.writeheader()
                
                for training in plan:
                    writer.writerow({
                        'Цикл': training['Цикл'],
                        'Тренування': training['Тренування'],
                        'Дата': training['Дата'],
                        'Вага (кг)': training['Вага'],
                        'Підходи': training['Підходи'],
                        'Повторення': training['Повторення']
                    })
                    
            success_window = tk.Toplevel(self)
            success_window.title("Експорт завершено")
            success_window.geometry("400x150")
            success_window.configure(bg="#f0f0f0")
            
            # Центрування вікна повідомлення
            x = self.winfo_x() + (self.winfo_width() - 400) // 2
            y = self.winfo_y() + (self.winfo_height() - 150) // 2
            success_window.geometry(f"400x150+{x}+{y}")
            
            tk.Label(success_window, 
                    text="План успішно експортовано!", 
                    font=("Arial", 12, "bold"),
                    bg="#f0f0f0").pack(pady=(20, 10))
            
            file_label = tk.Label(success_window, 
                                text=f"Файл: {file_path}", 
                                font=("Arial", 10),
                                bg="#f0f0f0",
                                wraplength=380)
            file_label.pack(pady=(0, 15))
            
            tk.Button(success_window, 
                    text="OK", 
                    command=success_window.destroy,
                    font=("Arial", 10),
                    bg="#4CAF50",
                    fg="white",
                    width=10).pack()
            
        except Exception as e:
            messagebox.showerror("Помилка", 
                            f"Не вдалося зберегти файл:\n{str(e)}",
                            parent=self)
            
if __name__ == "__main__":
    app = App()
    app.mainloop()
