import os
import json
import tkinter as tk
from datetime import datetime
import random
from tkinter import messagebox
import customtkinter as ctk

# Theme and color settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Colors
MAIN_BG = "#150050"          # Main background
WINDOW_BG = "#000000"        # Window background
ACCENT = "#3F0071"           # Neon purple elements
TEXT_COLOR = "#E0B3FF"       # Light purple text
GLOW = "#8A2BE2"             # Soft glowing accent
WATER_COLOR = "#87CEEB"      # Sky blue for water
GLASS_OUTLINE = "#A9A9A9"    # Gray for glass outline

USER_FILE = "users.json"
USER_DATA_FILE = "user_data.json"
os.makedirs("data", exist_ok=True)

class FitnessApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Main window
        self.title("Fitness Trainer")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(fg_color=MAIN_BG)

        self.user_data = None
        self.water_intake = tk.DoubleVar(value=0.0)
        self.water_goal = 2.0
        self.total_calories = tk.DoubleVar(value=0.0)
        self.steps = tk.DoubleVar(value=0.0)
        self.goals = []
        self.weight_text = tk.StringVar(value="Введите вес во вкладке 'Weight'")

        # Start with login screen
        self.show_login_screen()

    # ---------------------------- Utility methods ----------------------------
    def save_user(self, username, password):
        data = {}
        file_path = os.path.join("data", USER_FILE)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
        data[username] = {"password": password}
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def verify_user(self, username, password):
        file_path = os.path.join("data", USER_FILE)
        if not os.path.exists(file_path):
            return False
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                return False
        return username in users and users[username]["password"] == password

    def _save_user_data(self):
        data = {
            "username": self.user_data["username"] if self.user_data else "Guest",
            "water_intake": self.water_intake.get(),
            "total_calories": self.total_calories.get(),
            "steps": self.steps.get(),
            "goals": self.goals
        }
        with open(os.path.join("data", USER_DATA_FILE), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def _load_user_data(self):
        try:
            with open(os.path.join("data", USER_DATA_FILE), "r", encoding="utf-8") as f:
                data = json.load(f)
                self.water_intake.set(data.get("water_intake", 0.0))
                self.total_calories.set(data.get("total_calories", 0.0))
                self.steps.set(data.get("steps", 0.0))
                self.goals = data.get("goals", [])
                return data
        except FileNotFoundError:
            return {"username": "Guest", "settings": {}}

    # ---------------------------- Login screen ----------------------------
    def show_login_screen(self):
        self.clear_window()

        frame = ctk.CTkFrame(self, fg_color=WINDOW_BG, corner_radius=15, border_width=2, border_color=GLOW)
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.5)

        title = ctk.CTkLabel(frame, text="Вход", text_color=TEXT_COLOR, font=("Segoe UI", 28, "bold"))
        title.pack(pady=20)

        username_entry = ctk.CTkEntry(frame, placeholder_text="Имя пользователя", fg_color=MAIN_BG, border_color=ACCENT)
        username_entry.pack(pady=10, padx=40, fill="x")

        password_entry = ctk.CTkEntry(frame, placeholder_text="Пароль", show="•", fg_color=MAIN_BG, border_color=ACCENT)
        password_entry.pack(pady=10, padx=40, fill="x")

        def login():
            u = username_entry.get().strip()
            p = password_entry.get().strip()
            if self.verify_user(u, p):
                self.user_data = {"username": u}
                self._load_user_data()
                self._build_main_ui()
            else:
                messagebox.showerror("Ошибка", "Неверное имя или пароль")

        login_btn = ctk.CTkButton(frame, text="Войти", fg_color=ACCENT, hover_color=GLOW, command=login)
        login_btn.pack(pady=15)

        reg_btn = ctk.CTkButton(frame, text="Регистрация", fg_color="#222222", command=self.show_register_screen)
        reg_btn.pack(pady=10)

    # ---------------------------- Register screen ----------------------------
    def show_register_screen(self):
        self.clear_window()

        frame = ctk.CTkFrame(self, fg_color=WINDOW_BG, corner_radius=15, border_width=2, border_color=GLOW)
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.6)

        title = ctk.CTkLabel(frame, text="Регистрация", text_color=TEXT_COLOR, font=("Segoe UI", 28, "bold"))
        title.pack(pady=20)

        username_entry = ctk.CTkEntry(frame, placeholder_text="Имя пользователя", fg_color=MAIN_BG, border_color=ACCENT)
        username_entry.pack(pady=10, padx=40, fill="x")

        password_entry = ctk.CTkEntry(frame, placeholder_text="Пароль", show="•", fg_color=MAIN_BG, border_color=ACCENT)
        password_entry.pack(pady=10, padx=40, fill="x")

        confirm_entry = ctk.CTkEntry(frame, placeholder_text="Подтверждение пароля", show="•", fg_color=MAIN_BG, border_color=ACCENT)
        confirm_entry.pack(pady=10, padx=40, fill="x")

        def register():
            u = username_entry.get().strip()
            p = password_entry.get().strip()
            c = confirm_entry.get().strip()
            if not u or not p:
                messagebox.showwarning("Ошибка", "Заполните все поля")
                return
            if p != c:
                messagebox.showerror("Ошибка", "Пароли не совпадают")
                return
            self.save_user(u, p)
            messagebox.showinfo("Успешно", "Регистрация завершена!")
            self.show_login_screen()

        reg_btn = ctk.CTkButton(frame, text="Зарегистрироваться", fg_color=ACCENT, hover_color=GLOW, command=register)
        reg_btn.pack(pady=20)

        back_btn = ctk.CTkButton(frame, text="Назад", fg_color="#222222", command=self.show_login_screen)
        back_btn.pack()

    # ---------------------------- Clear window ----------------------------
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    # ---------------------------- Main UI ----------------------------
    def _build_main_ui(self):
        self.clear_window()

        # Header
        header = ctk.CTkFrame(self, fg_color=ACCENT, corner_radius=12, border_width=2, border_color=GLOW)
        header.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.1)

        user_label = ctk.CTkLabel(header, text=f"Welcome, {self.user_data['username']}!", text_color=TEXT_COLOR, font=("Segoe UI", 22, "bold"))
        user_label.pack(pady=10, side="left", padx=20)

        current_date = ctk.CTkLabel(header, text=datetime.now().strftime("%d.%m.%Y"), text_color=TEXT_COLOR, font=("Segoe UI", 18))
        current_date.pack(pady=10, side="right", padx=20)

        # Main tab area
        tabview = ctk.CTkTabview(self, fg_color=WINDOW_BG, segmented_button_fg_color=ACCENT,
                                 segmented_button_selected_color=GLOW, segmented_button_unselected_color="#2A004F", corner_radius=15)
        tabview.place(relx=0.02, rely=0.15, relwidth=0.96, relheight=0.8)

        # Add tabs
        panel_tab = tabview.add("Dashboard")
        calories_tab = tabview.add("Calories")
        water_tab = tabview.add("Water")
        weight_tab = tabview.add("Weight")
        health_tab = tabview.add("Health")
        meditation_tab = tabview.add("Meditation")
        sleep_tab = tabview.add("Sleep")
        goals_tab = tabview.add("Goals")

        # Fill tabs
        self._build_panel_tab(panel_tab)
        self._build_calories_tab(calories_tab)
        self._build_water_tab(water_tab)
        self._build_weight_tab(weight_tab)
        self._build_health_tab(health_tab)
        self._build_meditation_tab(meditation_tab)
        self._build_sleep_tab(sleep_tab)
        self._build_goals_tab(goals_tab)

        # Exit button
        exit_btn = ctk.CTkButton(self, text="Выход", fg_color="#222222", text_color="white",
                                 hover_color="#550099", command=self.show_login_screen)
        exit_btn.place(relx=0.9, rely=0.94, relwidth=0.08, relheight=0.05)

    # ---------------------------- Dashboard ----------------------------
    def _build_panel_tab(self, frame):
        frame.configure(fg_color=MAIN_BG)
        title = ctk.CTkLabel(frame, text="Общая панель", font=("Segoe UI", 26, "bold"), text_color=TEXT_COLOR)
        title.pack(pady=15)

        blocks_frame = ctk.CTkFrame(frame, fg_color=WINDOW_BG, corner_radius=15, border_width=2, border_color=GLOW)
        blocks_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Calories block
        calories_block = ctk.CTkFrame(blocks_frame, fg_color=WINDOW_BG, corner_radius=10, border_width=2, border_color=GLOW)
        calories_block.pack(pady=5, padx=10, fill="x")
        ctk.CTkLabel(calories_block, text="🍎 Калории", font=("Segoe UI", 20, "bold"), text_color=GLOW).pack(pady=5)
        ctk.CTkLabel(calories_block, textvariable=self.total_calories, font=("Segoe UI", 18), text_color=TEXT_COLOR).pack()
        ctk.CTkLabel(calories_block, text="Сегодня вы потребили столько калорий.", font=("Segoe UI", 14), text_color="#CFA0FF").pack(pady=5)

        # Water block
        water_block = ctk.CTkFrame(blocks_frame, fg_color=WINDOW_BG, corner_radius=10, border_width=2, border_color=GLOW)
        water_block.pack(pady=5, padx=10, fill="x")
        ctk.CTkLabel(water_block, text="💧 Вода", font=("Segoe UI", 20, "bold"), text_color=GLOW).pack(pady=5)
        water_text = tk.StringVar(value=f"{self.water_intake.get():.2f} / {self.water_goal:.1f} л")
        ctk.CTkLabel(water_block, textvariable=water_text, font=("Segoe UI", 18), text_color=TEXT_COLOR).pack()
        ctk.CTkLabel(water_block, text="Гидратация важна для энергии и здоровья.", font=("Segoe UI", 14), text_color="#CFA0FF").pack(pady=5)

        # Weight block
        weight_block = ctk.CTkFrame(blocks_frame, fg_color=WINDOW_BG, corner_radius=10, border_width=2, border_color=GLOW)
        weight_block.pack(pady=5, padx=10, fill="x")
        ctk.CTkLabel(weight_block, text="⚖️ Вес", font=("Segoe UI", 20, "bold"), text_color=GLOW).pack(pady=5)
        ctk.CTkLabel(weight_block, textvariable=self.weight_text, font=("Segoe UI", 18), text_color=TEXT_COLOR).pack()
        ctk.CTkLabel(weight_block, text="Регулярный контроль помогает достигать целей.", font=("Segoe UI", 14), text_color="#CFA0FF").pack(pady=5)

        # Steps block
        steps_block = ctk.CTkFrame(blocks_frame, fg_color=WINDOW_BG, corner_radius=10, border_width=2, border_color=GLOW)
        steps_block.pack(pady=5, padx=10, fill="x")
        ctk.CTkLabel(steps_block, text="👟 Шаги", font=("Segoe UI", 20, "bold"), text_color=GLOW).pack(pady=5)
        ctk.CTkLabel(steps_block, textvariable=self.steps, font=("Segoe UI", 18), text_color=TEXT_COLOR).pack()
        ctk.CTkLabel(steps_block, text="Активность улучшает самочувствие.", font=("Segoe UI", 14), text_color="#CFA0FF").pack(pady=5)

        # Goals block
        goals_block = ctk.CTkFrame(blocks_frame, fg_color=WINDOW_BG, corner_radius=10, border_width=2, border_color=GLOW)
        goals_block.pack(pady=5, padx=10, fill="x")
        ctk.CTkLabel(goals_block, text="🎯 Цели", font=("Segoe UI", 20, "bold"), text_color=GLOW).pack(pady=5)
        goals_text = tk.StringVar(value=f"Активных целей: {len(self.goals)}")
        ctk.CTkLabel(goals_block, textvariable=goals_text, font=("Segoe UI", 18), text_color=TEXT_COLOR).pack()
        ctk.CTkLabel(goals_block, text="Установите новые цели для мотивации.", font=("Segoe UI", 14), text_color="#CFA0FF").pack(pady=5)

    # ---------------------------- Calories ----------------------------
    def _build_calories_tab(self, frame):
        frame.configure(fg_color=MAIN_BG)
        title = ctk.CTkLabel(frame, text="Подсчет калорий", font=("Segoe UI", 26, "bold"), text_color=TEXT_COLOR)
        title.pack(pady=15)

        calories_block = ctk.CTkFrame(frame, fg_color=WINDOW_BG, corner_radius=15, border_width=2, border_color=GLOW)
        calories_block.pack(pady=10, padx=20, fill="x")

        foods = {
            "Яблоко": 52, "Банан": 89, "Куриная грудка": 165, "Рис": 130, "Хлеб": 265,
            "Молоко": 42, "Гречка": 123, "Овсянка": 68, "Яйцо": 68, "Картофель": 77,
            "Морковь": 41, "Огурец": 16, "Томаты": 18, "Лосось": 208, "Авокадо": 160
        }

        input_frame = ctk.CTkFrame(calories_block, fg_color=WINDOW_BG)
        input_frame.pack(pady=10, fill="x")

        food_var = tk.StringVar(value=list(foods.keys())[0])
        amount_var = tk.DoubleVar(value=100.0)

        ctk.CTkLabel(input_frame, text="Продукт:", text_color=TEXT_COLOR, font=("Segoe UI", 16)).grid(row=0, column=0, padx=10, pady=5)
        food_menu = ctk.CTkOptionMenu(input_frame, variable=food_var, values=list(foods.keys()), fg_color=ACCENT, button_color=GLOW)
        food_menu.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(input_frame, text="Количество (г):", text_color=TEXT_COLOR, font=("Segoe UI", 16)).grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkEntry(input_frame, textvariable=amount_var, width=100).grid(row=0, column=3, padx=10, pady=5)

        def add_food():
            food = food_var.get()
            amount = amount_var.get()
            calories = (foods[food] * amount) / 100
            self.total_calories.set(self.total_calories.get() + calories)
            self._save_user_data()
            messagebox.showinfo("Добавлено", f"Добавлено {food}: {calories:.1f} ккал")

        add_btn = ctk.CTkButton(input_frame, text="Добавить", fg_color=ACCENT, hover_color=GLOW, command=add_food)
        add_btn.grid(row=0, column=4, padx=10, pady=5)

        ctk.CTkLabel(calories_block, text="Общие калории:", font=("Segoe UI", 20, "bold"), text_color=GLOW).pack(pady=5)
        ctk.CTkLabel(calories_block, textvariable=self.total_calories, font=("Segoe UI", 18), text_color=TEXT_COLOR).pack()

        text = "\n".join([f"{food} — {cal} ккал / 100г" for food, cal in foods.items()])
        food_label = ctk.CTkLabel(calories_block, text=text, font=("Segoe UI", 16), text_color=TEXT_COLOR, justify="left")
        food_label.pack(pady=10, padx=20, anchor="w")

        tips = (
            "💡 Советы по питанию:\n"
            "- Ешьте больше белков для поддержания мышц.\n"
            "- Уменьшите количество сахара и фастфуда.\n"
            "- Пейте воду перед едой — это помогает контролировать аппетит.\n"
            "- Не пропускайте завтрак — это запускает обмен веществ."
        )
        ctk.CTkLabel(calories_block, text=tips, font=("Segoe UI", 14), text_color="#CFA0FF", justify="left").pack(pady=10, padx=20)

    # ---------------------------- Water ----------------------------
    def _build_water_tab(self, frame):
        frame.configure(fg_color=MAIN_BG)
        title = ctk.CTkLabel(frame, text="Трекер воды", font=("Segoe UI", 26, "bold"), text_color=TEXT_COLOR)
        title.pack(pady=15)

        water_block = ctk.CTkFrame(frame, fg_color=WINDOW_BG, corner_radius=15, border_width=2, border_color=GLOW)
        water_block.pack(pady=10, padx=20, fill="x")

        glass_container = ctk.CTkFrame(water_block, fg_color=WINDOW_BG)
        glass_container.pack(pady=10, side="left", padx=20)

        self.glass_canvas = ctk.CTkCanvas(glass_container, width=150, height=300, bg=MAIN_BG, highlightthickness=0)
        self.glass_canvas.pack(padx=10, pady=10)

        # Draw glass
        self.glass_canvas.create_rectangle(40, 20, 110, 280, outline=GLASS_OUTLINE, width=3)
        self.glass_canvas.create_arc(40, 260, 110, 280, start=0, extent=180, style="arc", outline=GLASS_OUTLINE, width=3)
        self.water_level = self.glass_canvas.create_rectangle(40, 280, 110, 280, fill=WATER_COLOR, outline="")

        slider = ctk.CTkSlider(water_block, orientation="vertical", from_=0, to=self.water_goal, number_of_steps=100, command=self.update_water_from_slider)
        slider.pack(side="left", padx=20, pady=10, fill="y")
        slider.set(self.water_intake.get())

        water_label = ctk.CTkLabel(water_block, textvariable=self.water_intake, font=("Segoe UI", 20, "bold"), text_color=GLOW)
        water_label.pack(side="left", padx=10, pady=5)
        goal_label = ctk.CTkLabel(water_block, text=f"/ {self.water_goal:.1f} л", font=("Segoe UI", 16), text_color=TEXT_COLOR)
        goal_label.pack(side="left", padx=5)

        bottom_frame = ctk.CTkFrame(frame, fg_color=WINDOW_BG, corner_radius=15, border_width=2, border_color=GLOW)
        bottom_frame.pack(pady=10, padx=20, fill="x")

        btn_frame = ctk.CTkFrame(bottom_frame, fg_color=WINDOW_BG)
        btn_frame.pack(pady=10)

        for ml in [0.1, 0.25, 0.5, 1.0]:
            btn = ctk.CTkButton(btn_frame, text=f"+{ml} л", fg_color=ACCENT, hover_color=GLOW, width=80,
                                command=lambda m=ml: self.add_water(m))
            btn.pack(side="left", padx=15, pady=5)

        water_entry = ctk.CTkEntry(bottom_frame, textvariable=self.water_intake, width=100)
        water_entry.pack(pady=5, padx=10)
        water_entry.bind("<Return>", lambda e: self.update_water_from_entry(water_entry))

        tips = (
            "💧 Пейте воду равномерно в течение дня.\n"
            "💜 Не ждите жажды, пейте заранее.\n"
            "🌙 Стакан воды утром — полезная привычка!"
        )
        ctk.CTkLabel(bottom_frame, text=tips, font=("Segoe UI", 14), text_color="#CFA0FF", justify="left").pack(pady=10, padx=20)

    def update_water_from_slider(self, value):
        self.water_intake.set(round(float(value), 2))
        self._update_glass()

    def update_water_from_entry(self, entry):
        try:
            value = float(entry.get())
            if 0 <= value <= self.water_goal:
                self.water_intake.set(round(value, 2))
                self._update_glass()
            else:
                messagebox.showwarning("Ошибка", f"Введите значение от 0 до {self.water_goal} л")
        except ValueError:
            messagebox.showwarning("Ошибка", "Введите корректное число")

    def add_water(self, amount):
        current = self.water_intake.get()
        new_value = min(current + amount, self.water_goal)
        self.water_intake.set(round(new_value, 2))
        self._update_glass()

    def _update_glass(self):
        progress = self.water_intake.get() / self.water_goal
        height = 260 * progress
        self.glass_canvas.coords(self.water_level, 40, 280 - height, 110, 280)
        self._save_user_data()

    # ---------------------------- Weight ----------------------------
    def _build_weight_tab(self, frame):
        frame.configure(fg_color=MAIN_BG)
        title = ctk.CTkLabel(frame, text="Контроль веса", font=("Segoe UI", 26, "bold"), text_color=TEXT_COLOR)
        title.pack(pady=15)

        weight_block = ctk.CTkFrame(frame, fg_color=WINDOW_BG, corner_radius=15, border_width=2, border_color=GLOW)
        weight_block.pack(pady=10, padx=20, fill="x")

        weight_var = tk.DoubleVar(value=0.0)
        height_var = tk.DoubleVar(value=0.0)
        bmi_var = tk.StringVar(value="")

        entry_frame = ctk.CTkFrame(weight_block, fg_color=WINDOW_BG)
        entry_frame.pack(pady=10, fill="x")

        ctk.CTkLabel(entry_frame, text="Вес (кг):", text_color=TEXT_COLOR, font=("Segoe UI", 16)).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkEntry(entry_frame, textvariable=weight_var, width=120).grid(row=0, column=1, padx=10)

        ctk.CTkLabel(entry_frame, text="Рост (см):", text_color=TEXT_COLOR, font=("Segoe UI", 16)).grid(row=1, column=0, padx=10, pady=5)
        ctk.CTkEntry(entry_frame, textvariable=height_var, width=120).grid(row=1, column=1, padx=10)

        def calc_bmi():
            try:
                w = weight_var.get()
                h = height_var.get() / 100
                bmi = w / (h ** 2)
                bmi_var.set(f"Ваш ИМТ: {bmi:.1f}")
                self.weight_text.set(f"{w} кг")
                if bmi < 18.5:
                    advice = "Недостаточный вес:\n- Увеличьте калорийность питания.\n- Добавьте питательные продукты.\n- Занимайтесь силовыми тренировками."
                elif 18.5 <= bmi < 25:
                    advice = "Нормальный вес:\n- Поддерживайте сбалансированное питание.\n- Регулярные упражнения.\n- Мониторьте изменения."
                elif 25 <= bmi < 30:
                    advice = "Избыточный вес:\n- Уменьшите калорийность.\n- Увеличьте кардио-активность.\n- Контролируйте порции."
                else:
                    advice = "Ожирение:\n- Обратитесь к врачу.\n- Сбалансированная диета с дефицитом.\n- Комбинируйте кардио и силовые тренировки."
                advice_label.configure(text=advice)
            except Exception:
                bmi_var.set("Ошибка ввода")

        calc_btn = ctk.CTkButton(weight_block, text="Рассчитать ИМТ", fg_color=ACCENT, hover_color=GLOW, text_color="white", width=180)
        calc_btn.pack(pady=10)

        bmi_label = ctk.CTkLabel(weight_block, textvariable=bmi_var, font=("Segoe UI", 20, "bold"), text_color=GLOW)
        bmi_label.pack(pady=5)

        advice_label = ctk.CTkLabel(weight_block, text="", font=("Segoe UI", 14), text_color="#CFA0FF", justify="left")
        advice_label.pack(pady=5, padx=20)

    # ---------------------------- Health ----------------------------
    def _build_health_tab(self, frame):
        frame.configure(fg_color=MAIN_BG)
        title = ctk.CTkLabel(frame, text="Здоровье", font=("Segoe UI", 26, "bold"), text_color=TEXT_COLOR)
        title.pack(pady=15)

        health_block = ctk.CTkFrame(frame, fg_color=WINDOW_BG, corner_radius=15, border_width=2, border_color=GLOW)
        health_block.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(health_block, text="Шагометр", font=("Segoe UI", 20, "bold"), text_color=TEXT_COLOR).pack(pady=5)
        step_entry = ctk.CTkEntry(health_block, textvariable=self.steps, width=120)
        step_entry.pack(pady=5)

        def add_steps(amount):
            self.steps.set(self.steps.get() + amount)
            self._save_user_data()

        btn_frame = ctk.CTkFrame(health_block, fg_color=WINDOW_BG)
        btn_frame.pack(pady=10)

        for steps in [100, 500, 1000]:
            btn = ctk.CTkButton(btn_frame, text=f"+{steps}", fg_color=ACCENT, hover_color=GLOW, width=80,
                                command=lambda s=steps: add_steps(s))
            btn.pack(side="left", padx=15, pady=5)

        def simulate_steps():
            total_steps = random.randint(100, 1000)
            step_increment = total_steps // 10
            current = self.steps.get()

            def add_increment(step=0):
                if step < 10:
                    self.steps.set(self.steps.get() + step_increment)
                    frame.after(500, add_increment, step + 1)
                else:
                    self.steps.set(current + total_steps)
                    self._save_user_data()
                    messagebox.showinfo("Симуляция", f"Добавлено {total_steps} шагов")

            add_increment()

        sim_btn = ctk.CTkButton(health_block, text="Симулировать шаги", fg_color=ACCENT, hover_color=GLOW, command=simulate_steps)
        sim_btn.pack(pady=10)

        pulse_var = tk.DoubleVar(value=0.0)
        ctk.CTkLabel(health_block, text="Пульс (уд/мин):", font=("Segoe UI", 16), text_color=TEXT_COLOR).pack(pady=5)
        ctk.CTkEntry(health_block, textvariable=pulse_var, width=120).pack(pady=5)

        def analyze_pulse():
            pulse = pulse_var.get()
            if pulse < 60:
                txt = "Пульс ниже нормы — обратитесь к врачу."
            elif 60 <= pulse <= 100:
                txt = "Нормальный пульс — продолжайте поддерживать активность!"
            else:
                txt = "Пульс выше нормы — отдохните и измерьте снова."
            messagebox.showinfo("Пульс", txt)

        pulse_btn = ctk.CTkButton(health_block, text="Анализ пульса", fg_color=ACCENT, hover_color=GLOW, command=analyze_pulse)
        pulse_btn.pack(pady=5)

    # ---------------------------- Meditation ----------------------------
    def _build_meditation_tab(self, frame):
        frame.configure(fg_color=MAIN_BG)

        # Full-screen star background
        canvas = ctk.CTkCanvas(frame, bg=MAIN_BG, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        stars = []
        for _ in range(200):
            x, y = random.randint(0, 1100), random.randint(0, 700)
            size = random.randint(2, 6)
            color = random.choice(["#FFFFFF", "#E0FFFF", "#ADD8E6", "#87CEEB"])
            stars.append(canvas.create_oval(x, y, x+size, y+size, fill=color, outline=""))

        def twinkle():
            for s in stars:
                new_color = random.choice(["#FFFFFF", "#E0FFFF", "#ADD8E6", "#87CEEB"])
                canvas.itemconfig(s, fill=new_color)
            frame.after(500, twinkle)

        twinkle()

        content = ctk.CTkFrame(frame, fg_color=WINDOW_BG, corner_radius=15, border_width=2, border_color=GLOW)
        content.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.7)

        title = ctk.CTkLabel(content, text="Медитация", font=("Segoe UI", 26, "bold"), text_color=GLOW)
        title.pack(pady=10)

        time_var = tk.StringVar(value="5")
        ctk.CTkLabel(content, text="Время (мин):", text_color=TEXT_COLOR, font=("Segoe UI", 16)).pack(pady=5)
        time_menu = ctk.CTkOptionMenu(content, variable=time_var, values=["1", "5", "10", "15", "20"], fg_color=ACCENT, button_color=GLOW)
        time_menu.pack(pady=5)

        timer_label = ctk.CTkLabel(content, text="00:00", font=("Segoe UI", 20, "bold"), text_color=TEXT_COLOR)
        timer_label.pack(pady=10)

        def start_meditation():
            minutes = int(time_var.get())
            seconds = minutes * 60
            start_btn.configure(state="disabled")

            def update_timer():
                nonlocal seconds
                if seconds > 0:
                    mins, secs = divmod(seconds, 60)
                    timer_label.configure(text=f"{mins:02d}:{secs:02d}")
                    seconds -= 1
                    frame.after(1000, update_timer)
                else:
                    start_btn.configure(state="normal")
                    messagebox.showinfo("Медитация", "Медитация завершена!")

            update_timer()

        start_btn = ctk.CTkButton(content, text="Начать медитацию", fg_color=ACCENT, hover_color=GLOW, command=start_meditation)
        start_btn.pack(pady=10)

        notes = (
            "🧘 Медитация помогает:\n"
            "- Снизить стресс и тревожность\n"
            "- Улучшить концентрацию\n"
            "- Повысить эмоциональное благополучие\n"
            "- Улучшить сон\n"
            "- Снизить давление\n\n"
            "💡 Советы:\n"
            "- Найдите тихое место.\n"
            "- Сядьте удобно, держите спину прямо.\n"
            "- Сосредоточьтесь на дыхании: вдох — 4 сек, выдох — 4 сек.\n"
            "- Начните с 5 минут в день.\n"
            "- Используйте направленные приложения, если новичок."
        )
        ctk.CTkLabel(content, text=notes, font=("Segoe UI", 14), text_color="#CFA0FF", justify="left").pack(pady=10, padx=20)

    # ---------------------------- Sleep ----------------------------
    def _build_sleep_tab(self, frame):
        frame.configure(fg_color=MAIN_BG)

        # Full-screen star background
        canvas = ctk.CTkCanvas(frame, bg=MAIN_BG, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        stars = []
        for _ in range(200):
            x, y = random.randint(0, 1100), random.randint(0, 700)
            size = random.randint(2, 6)
            color = random.choice(["#FFFFFF", "#E0FFFF", "#ADD8E6", "#87CEEB"])
            stars.append(canvas.create_oval(x, y, x+size, y+size, fill=color, outline=""))

        def twinkle():
            for s in stars:
                new_color = random.choice(["#FFFFFF", "#E0FFFF", "#ADD8E6", "#87CEEB"])
                canvas.itemconfig(s, fill=new_color)
            frame.after(500, twinkle)

        twinkle()

        canvas.create_oval(600, 60, 670, 130, fill="#CFA0FF", outline="")
        canvas.create_oval(615, 60, 685, 130, fill=MAIN_BG, outline="")

        content = ctk.CTkFrame(frame, fg_color=WINDOW_BG, corner_radius=15, border_width=2, border_color=GLOW)
        content.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.7)

        title = ctk.CTkLabel(content, text="Трекер сна", font=("Segoe UI", 26, "bold"), text_color=GLOW)
        title.pack(pady=10)

        sleep_hours = tk.DoubleVar(value=0.0)
        ctk.CTkLabel(content, text="Сколько часов вы спали?", text_color=TEXT_COLOR, font=("Segoe UI", 16)).pack(pady=5)
        ctk.CTkEntry(content, textvariable=sleep_hours, width=120).pack(pady=5)

        result_label = ctk.CTkLabel(content, text="", text_color="#CFA0FF", font=("Segoe UI", 16))
        result_label.pack(pady=10)

        def analyze_sleep():
            hours = sleep_hours.get()
            if hours < 5:
                txt = "😴 Очень мало сна! Попробуйте спать минимум 7 часов."
            elif 5 <= hours < 7:
                txt = "🟡 Недостаточный сон. Нужно чуть больше отдыха."
            elif 7 <= hours < 9:
                txt = "💜 Отлично! Это оптимальное количество сна."
            else:
                txt = "💤 Вы спите больше нормы — возможно, стоит ложиться позже."
            result_label.configure(text=txt)
            self._save_user_data()

        analyze_btn = ctk.CTkButton(content, text="Анализ сна", fg_color=ACCENT, hover_color=GLOW, command=analyze_sleep)
        analyze_btn.pack(pady=5)

        notes = (
            "😴 Сон важен для:\n"
            "- Восстановления организма\n"
            "- Улучшения памяти и концентрации\n"
            "- Поддержания иммунитета\n"
            "- Регуляции гормонов\n"
            "- Контроля веса\n"
            "- Улучшения настроения\n\n"
            "💡 Советы для хорошего сна:\n"
            "- Ложитесь спать в одно и то же время.\n"
            "- Избегайте экранов за час до сна.\n"
            "- Создайте темную и прохладную обстановку.\n"
            "- Нет кофеину вечером.\n"
            "- Расслабьтесь с чтением или медитацией.\n"
            "- Занимайтесь спортом днем."
        )
        ctk.CTkLabel(content, text=notes, font=("Segoe UI", 14), text_color="#CFA0FF", justify="left").pack(pady=10, padx=20)

    # ---------------------------- Goals ----------------------------
    def _build_goals_tab(self, frame):
        frame.configure(fg_color=MAIN_BG)
        title = ctk.CTkLabel(frame, text="Цели", font=("Segoe UI", 26, "bold"), text_color=TEXT_COLOR)
        title.pack(pady=15)

        goals_block = ctk.CTkFrame(frame, fg_color=WINDOW_BG, corner_radius=15, border_width=2, border_color=GLOW)
        goals_block.pack(pady=10, padx=20, fill="x")

        goal_desc = tk.StringVar()
        goal_value = tk.DoubleVar()
        goal_period = tk.StringVar(value="1 месяц")

        ctk.CTkLabel(goals_block, text="Описание цели:", font=("Segoe UI", 16), text_color=TEXT_COLOR).pack(pady=5)
        ctk.CTkEntry(goals_block, textvariable=goal_desc, width=300).pack(pady=5)

        ctk.CTkLabel(goals_block, text="Значение (напр., 5 кг):", font=("Segoe UI", 16), text_color=TEXT_COLOR).pack(pady=5)
        ctk.CTkEntry(goals_block, textvariable=goal_value, width=120).pack(pady=5)

        ctk.CTkLabel(goals_block, text="Срок:", font=("Segoe UI", 16), text_color=TEXT_COLOR).pack(pady=5)
        ctk.CTkOptionMenu(goals_block, variable=goal_period, values=["1 неделя", "1 месяц", "3 месяца"], fg_color=ACCENT, button_color=GLOW).pack(pady=5)

        def add_goal():
            desc = goal_desc.get()
            value = goal_value.get()
            period = goal_period.get()
            if not desc or value <= 0:
                messagebox.showwarning("Ошибка", "Заполните все поля корректно")
                return

            advice = ""
            if "вес" in desc.lower() and "сбросить" in desc.lower():
                advice = (
                    "💡 Советы для снижения веса:\n"
                    "- Создайте дефицит калорий (ешьте меньше, чем тратите).\n"
                    "- Добавьте кардио 3–4 раза в неделю.\n"
                    "- Увеличьте потребление белка и клетчатки.\n"
                    "- Пейте достаточно воды."
                )
            elif "вес" in desc.lower() and "набрать" in desc.lower():
                advice = (
                    "💡 Советы для набора веса:\n"
                    "- Увеличьте калорийность рациона.\n"
                    "- Ешьте больше белков и углеводов.\n"
                    "- Занимайтесь силовыми тренировками.\n"
                    "- Ешьте чаще, но меньшими порциями."
                )
            else:
                advice = "💡 Общие советы: Разбейте цель на маленькие шаги и отслеживайте прогресс!"

            self.goals.append({"desc": desc, "value": value, "period": period, "advice": advice})
            self._save_user_data()
            messagebox.showinfo("Цель добавлена", f"Цель: {desc}\nСоветы:\n{advice}")

        add_btn = ctk.CTkButton(goals_block, text="Добавить цель", fg_color=ACCENT, hover_color=GLOW, command=add_goal)
        add_btn.pack(pady=10)

        goals_text = "\n".join([f"{g['desc']} ({g['value']} за {g['period']})" for g in self.goals])
        ctk.CTkLabel(goals_block, text=goals_text or "Нет активных целей", font=("Segoe UI", 14), text_color=TEXT_COLOR, justify="left").pack(pady=10, padx=20)

        common_goals = (
            "🎯 Общие цели фитнеса:\n"
            "- Сбросить вес (напр., 5-10 кг за 3 месяца)\n"
            "- Набрать мышцы\n"
            "- Пробежать милю без остановки\n"
            "- Заниматься 3-4 раза в неделю\n"
            "- Улучшить гибкость с йогой\n"
            "- Достичь 10 000 шагов ежедневно\n"
            "- Питаться здоровее\n"
            "- Получать лучший сон (7-9 часов)"
        )
        ctk.CTkLabel(goals_block, text=common_goals, font=("Segoe UI", 14), text_color="#CFA0FF", justify="left").pack(pady=10, padx=20)

    # ---------------------------- Run ----------------------------
    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = FitnessApp()
    app.run()
