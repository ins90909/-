import numpy as np
from sklearn.tree import DecisionTreeClassifier
import os
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "materials_data.txt"
STATS_FILE = "material_stats.txt"

material_classes = {
    0: "Стекло",
    1: "Бумага",
    2: "Пластик",
    3: "Металл",
    4: "Органика",
    5: "Неизвестный материал"
}

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as file:
            lines = file.readlines()
            stats = {int(line.split(":")[0]): int(line.split(":")[1].strip()) for line in lines}
        return stats
    else:
        return {key: 0 for key in material_classes}

def save_stats():
    with open(STATS_FILE, "w") as file:
        for key, value in material_stats.items():
            file.write(f"{key}:{value}\n")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            lines = file.readlines()
            data = [list(map(float, line.strip().split(","))) for line in lines]
        return data
    else:
        return [
            [10, 5, 50, 0.2, 0],  # Стекло
            [15, 10, 30, 0.05, 1],  # Бумага
            [8, 4, 20, 0.03, 2],  # Пластик
            [12, 6, 80, 0.7, 3],  # Металл
            [10, 8, 25, 0.3, 4],  # Органика
        ]

def update_statistics(material_class):
    if material_class in material_stats:
        material_stats[material_class] += 1

data = load_data()
material_stats = load_stats()

def train_model(data):
    # Используем только проводимость как признак для обучения
    X = np.array([row[3] for row in data]).reshape(-1, 1)
    y = np.array([row[4] for row in data])
    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model

model = train_model(data)

def save_data():
    with open(DATA_FILE, "w") as file:
        for row in data:
            file.write(",".join(map(str, row)) + "\n")

def add_new_data():
    try:
        length = float(entry_length.get())
        width = float(entry_width.get())
        weight = float(entry_weight.get())
        conductivity = float(entry_conductivity.get())
        material_class = int(combo_material.get())

        if material_class not in material_classes:
            raise ValueError("Неверный класс материала.")

        data.append([length, width, weight, conductivity, material_class])
        update_statistics(material_class)

        save_data()
        save_stats()

        global model
        model = train_model(data)
        messagebox.showinfo("Успех", "Данные успешно добавлены и модель обновлена!")

    except ValueError as e:
        messagebox.showerror("Ошибка", f"Ошибка ввода: {e}")

def show_statistics():
    stats_text.config(state=tk.NORMAL)
    stats_text.delete(1.0, tk.END)
    stats_text.insert(tk.END, "Статистика добавленных материалов:\n")
    for key, value in material_stats.items():
        stats_text.insert(tk.END, f"{material_classes[key]}: {value} объектов\n")
    stats_text.config(state=tk.DISABLED)

def classify_object_auto():
    try:
        conductivity = float(entry_conductivity.get())
        input_data = np.array([[conductivity]])
        predicted_class = model.predict(input_data)[0]

        messagebox.showinfo("Результат", f"Результат классификации: {material_classes[predicted_class]}")
    except ValueError as e:
        messagebox.showerror("Ошибка", f"Ошибка ввода: {e}")

def create_ui():
    window = tk.Tk()
    window.title("Классификатор материалов")
    window.geometry("450x550")
    window.resizable(False, False)
    window.configure(bg="#e0f7fa")

    header_frame = tk.Frame(window, bg="#004d40")
    header_frame.pack(fill=tk.X)

    header_label = tk.Label(header_frame, text="Классификатор материалов", bg="#004d40", fg="white", font=('Arial', 16))
    header_label.pack(pady=10)

    frame_inputs = tk.Frame(window, bg="#e0f7fa")
    frame_inputs.pack(padx=10, pady=10, fill=tk.X)

    tk.Label(frame_inputs, text="Длина объекта (см):", bg="#e0f7fa").grid(row=0, column=0, sticky="w")
    global entry_length
    entry_length = tk.Entry(frame_inputs, width=25)
    entry_length.grid(row=0, column=1)

    tk.Label(frame_inputs, text="Ширина объекта (см):", bg="#e0f7fa").grid(row=1, column=0, sticky="w")
    global entry_width
    entry_width = tk.Entry(frame_inputs, width=25)
    entry_width.grid(row=1, column=1)

    tk.Label(frame_inputs, text="Вес объекта (г):", bg="#e0f7fa").grid(row=2, column=0, sticky="w")
    global entry_weight
    entry_weight = tk.Entry(frame_inputs, width=25)
    entry_weight.grid(row=2, column=1)

    tk.Label(frame_inputs, text="Проводимость объекта:", bg="#e0f7fa").grid(row=3, column=0, sticky="w")
    global entry_conductivity
    entry_conductivity = tk.Entry(frame_inputs, width=25)
    entry_conductivity.grid(row=3, column=1)

    tk.Label(frame_inputs, text="Класс материала:", bg="#e0f7fa").grid(row=4, column=0, sticky="w")
    global combo_material
    combo_material = tk.StringVar()
    material_options = list(material_classes.values())
    combo_material.set(material_options[0])
    material_menu = tk.OptionMenu(frame_inputs, combo_material, *material_options)
    material_menu.grid(row=4, column=1)

    frame_buttons = tk.Frame(window, bg="#e0f7fa")
    frame_buttons.pack(padx=10, pady=5, fill=tk.X)

    button_style = {'width': 25, 'bg': "#00796b", 'fg': "white", 'font': ('Arial', 10)}

    button_add_data = tk.Button(frame_buttons, text="Добавить данные", command=add_new_data, **button_style)
    button_add_data.pack(pady=5)

    button_classify = tk.Button(frame_buttons, text="Классифицировать", command=classify_object_auto, **button_style)
    button_classify.pack(pady=5)

    button_show_stats = tk.Button(frame_buttons, text="Показать статистику", command=show_statistics, **button_style)
    button_show_stats.pack(pady=5)

    frame_stats = tk.Frame(window, bg="#e0f7fa")
    frame_stats.pack(padx=10, pady=10, fill=tk.X)

    global stats_text
    stats_text = tk.Text(frame_stats, height=10, width=50, wrap=tk.WORD)
    stats_text.pack()
    stats_text.config(state=tk.DISABLED)

    window.mainloop()

if __name__ == "__main__":
    create_ui()
