import numpy as np
from sklearn.tree import DecisionTreeClassifier
import os

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
    """
    Загружает статистику из файла, если он существует.
    :return: Словарь с количеством объектов для каждого материала.
    """
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as file:
            lines = file.readlines()
            stats = {int(line.split(":")[0]): int(line.split(":")[1].strip()) for line in lines}
        print(f"Статистика загружена из {STATS_FILE}")
        return stats
    else:
        return {key: 0 for key in material_classes}

def save_stats():
    """
    Сохраняет текущую статистику в файл.
    """
    with open(STATS_FILE, "w") as file:
        for key, value in material_stats.items():
            file.write(f"{key}:{value}\n")
    print(f"Статистика сохранена в {STATS_FILE}")

def load_data():
    """
    Загружает данные из файла, если он существует.
    :return: Список данных [длина, ширина, вес, проводимость, класс материала].
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            lines = file.readlines()
            data = [list(map(float, line.strip().split(","))) for line in lines]
        print(f"Данные загружены из {DATA_FILE}")
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
    """
    Обновляет статистику по материалам после добавления нового объекта.
    """
    if material_class in material_stats:
        material_stats[material_class] += 1
    else:
        print(f"Ошибка: неизвестный класс материала {material_class}")

data = load_data()
material_stats = load_stats()

def train_model(data):
    """
    Обучает модель на основе предоставленных данных.
    :param data: Список данных в формате [длина, ширина, вес, проводимость, класс материала].
    :return: Обученная модель.
    """
    X = np.array([row[:4] for row in data])  # Входные параметры
    y = np.array([row[4] for row in data])  # Классы материалов
    
    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model

model = train_model(data)

def save_data():
    """
    Сохраняет таблицу данных в файл.
    """
    with open(DATA_FILE, "w") as file:
        for row in data:
            file.write(",".join(map(str, row)) + "\n")
    print(f"Данные сохранены в {DATA_FILE}")

def add_new_data():
    """
    Добавляет новые данные в таблицу.
    Пользователь вводит параметры объекта и класс материала.
    """
    print("\nДобавление новых данных:")
    try:
        length = float(input("Введите длину объекта (см): "))
        width = float(input("Введите ширину объекта (см): "))
        weight = float(input("Введите вес объекта (г): "))
        conductivity = float(input("Введите проводимость объекта: "))
        print("Выберите класс материала:")
        for key, value in material_classes.items():
            print(f"{key}: {value}")
        material_class = int(input("Введите номер класса материала: "))
        if material_class not in material_classes:
            raise ValueError("Неверный класс материала.")

        data.append([length, width, weight, conductivity, material_class])
        print("Данные успешно добавлены!")
        print(f"Текущая таблица данных: {data}")

        update_statistics(material_class)

        save_data()
        save_stats()

        global model
        model = train_model(data)
        print("Модель успешно обновлена!")
    except ValueError as e:
        print(f"Ошибка ввода: {e}")

def show_statistics():
    """
    Отображает текущую статистику по материалам.
    """
    print("\nСтатистика добавленных материалов:")
    for key, value in material_stats.items():
        print(f"{material_classes[key]}: {value} объектов")

def classify_object_auto():
    """
    Имитирует автоматическое измерение объекта и классификацию.
    В реальной системе данные поступают от сенсоров.
    """
    print("\nАвтоматическое измерение:")
    # Имитируем данные сенсоров
    length = float(input("Введите длину объекта (см): "))
    width = float(input("Введите ширину объекта (см): "))
    weight = float(input("Введите вес объекта (г): "))
    conductivity = float(input("Введите проводимость объекта: "))
    
    input_data = np.array([[length, width, weight, conductivity]])
    predicted_class = model.predict(input_data)[0]
    print(f"Результат: {material_classes[predicted_class]}")
    return predicted_class

def main():
    """
    Главное меню программы.
    Пользователь может выбрать, что делать: добавить данные, классифицировать объект, показать статистику или выйти.
    """
    while True:
        print("\nВыберите действие:")
        print("1: Добавить новые данные")
        print("2: Классифицировать объект (автоматическое измерение)")
        print("3: Показать текущую таблицу данных")
        print("4: Показать статистику добавленных материалов")
        print("5: Выйти")
        
        choice = input("Введите номер действия: ")
        if choice == "1":
            add_new_data()
        elif choice == "2":
            classify_object_auto()
        elif choice == "3":
            print(f"\nТекущая таблица данных: {data}")
        elif choice == "4":
            show_statistics()
        elif choice == "5":
            print("Выход из программы. До свидания!")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()