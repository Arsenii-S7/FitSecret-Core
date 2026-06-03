import json
import os
from datetime import datetime

DB_FILE = "food_db.json"
HISTORY_FILE = "meal_history.json"

DEFAULT_DATABASE = {
    # ========================================================
    # 🥩 [МЯСО И ПТИЦА] (Вес в сыром виде)
    # ========================================================
    "куриное филе (грудка)": {"kcal": 113, "protein": 23.6, "fat": 1.9, "carbs": 0.4},
    "куриное бедро (без кожи)": {"kcal": 130, "protein": 21.0, "fat": 5.0, "carbs": 0.0},
    "индейка (филе грудки)": {"kcal": 84, "protein": 19.2, "fat": 0.7, "carbs": 0.0},
    "говядина (постная)": {"kcal": 158, "protein": 22.0, "fat": 7.0, "carbs": 0.0},
    "говядина (жирная)": {"kcal": 254, "protein": 18.0, "fat": 20.0, "carbs": 0.0},
    "свинина (вырезка постная)": {"kcal": 142, "protein": 20.0, "fat": 7.0, "carbs": 0.0},
    "фарш говяжий легкий": {"kcal": 180, "protein": 20.0, "fat": 11.0, "carbs": 0.0},
    "фарш куриный домашний": {"kcal": 143, "protein": 17.4, "fat": 8.1, "carbs": 0.0},

    # ========================================================
    # 🐟 [РЫБА И МОРЕПРОДУКТЫ] (Вес в сыром/чистом виде)
    # ========================================================
    "горбуша": {"kcal": 142, "protein": 20.5, "fat": 6.5, "carbs": 0.0},
    "лосось / семга (аквакультура)": {"kcal": 208, "protein": 20.0, "fat": 13.0, "carbs": 0.0},
    "треска (филе)": {"kcal": 78, "protein": 17.7, "fat": 0.7, "carbs": 0.0},
    "минтай": {"kcal": 72, "protein": 15.9, "fat": 0.9, "carbs": 0.0},
    "тунец (в собственном соку)": {"kcal": 101, "protein": 23.0, "fat": 1.0, "carbs": 0.0},
    "креветки": {"kcal": 95, "protein": 19.0, "fat": 1.0, "carbs": 0.0},
    "кальмары": {"kcal": 100, "protein": 18.0, "fat": 2.2, "carbs": 2.0},

    # ========================================================
    # 🥚 [ЯЙЦА]
    # ========================================================
    "яйцо куриное целиком": {"kcal": 157, "protein": 12.7, "fat": 11.5, "carbs": 0.7, "weight_per_piece": 55},
    "яичный белок (жидкий/сырой)": {"kcal": 44, "protein": 11.1, "fat": 0.2, "carbs": 1.0},
    "яичный желток": {"kcal": 352, "protein": 16.2, "fat": 30.8, "carbs": 1.0},

    # ========================================================
    # 🥛 [МОЛОЧНЫЕ ПРОДУКТЫ И КЕФИРЫ]
    # ========================================================
    "кефир 1%": {"kcal": 40, "protein": 3.0, "fat": 1.0, "carbs": 4.0},
    "кефир 2.5%": {"kcal": 53, "protein": 2.9, "fat": 2.5, "carbs": 4.0},
    "молоко 0.5%": {"kcal": 35, "protein": 3.0, "fat": 0.5, "carbs": 4.7},
    "молоко 2.5%": {"kcal": 52, "protein": 3.0, "fat": 2.5, "carbs": 4.7},
    "молоко 3.2%": {"kcal": 59, "protein": 2.9, "fat": 3.2, "carbs": 4.7},
    "творог 0% (обезжиренный)": {"kcal": 71, "protein": 16.5, "fat": 0.2, "carbs": 1.3},
    "творог 5%": {"kcal": 121, "protein": 17.2, "fat": 5.0, "carbs": 1.8},
    "творог 9%": {"kcal": 157, "protein": 16.0, "fat": 9.0, "carbs": 2.0},
    "йогурт греческий 0% (без добавок)": {"kcal": 57, "protein": 10.0, "fat": 0.0, "carbs": 4.0},
    "сыр легкий (типа Fitness 15-20%)": {"kcal": 250, "protein": 30.0, "fat": 15.0, "carbs": 0.0},
    "сыр российский / голландский (45%)": {"kcal": 350, "protein": 24.0, "fat": 28.0, "carbs": 0.0},

    # ========================================================
    # 🌾 [КРУПЫ И ГАРНИРЫ] (Вес строго в СУХОМ виде)
    # ========================================================
    "гречневая крупа (ядрица)": {"kcal": 330, "protein": 12.6, "fat": 3.3, "carbs": 62.0},
    "рис белый (длиннозерный)": {"kcal": 344, "protein": 6.7, "fat": 0.7, "carbs": 78.9},
    "рис бурый / нешлифованный": {"kcal": 337, "protein": 7.4, "fat": 1.8, "carbs": 72.9},
    "овсяные хлопья (геркулес)": {"kcal": 352, "protein": 12.3, "fat": 6.2, "carbs": 61.8},
    "макароны (из твердых сортов)": {"kcal": 344, "protein": 12.0, "fat": 1.5, "carbs": 71.0},
    "булгур": {"kcal": 342, "protein": 12.0, "fat": 1.5, "carbs": 63.0},
    "киноа": {"kcal": 368, "protein": 14.1, "fat": 6.1, "carbs": 57.0},
    "картофель (сырой)": {"kcal": 77, "protein": 2.0, "fat": 0.4, "carbs": 16.3, "weight_per_piece": 150},

    # ========================================================
    # 🧅 [ОВОЩИ И ЗЕЛЕНЬ] (В сыром виде)
    # ========================================================
    "огурец": {"kcal": 15, "protein": 0.8, "fat": 0.1, "carbs": 2.8, "weight_per_piece": 100},
    "помидор": {"kcal": 18, "protein": 0.6, "fat": 0.2, "carbs": 3.9, "weight_per_piece": 110},
    "болгарский перец": {"kcal": 26, "protein": 1.3, "fat": 0.0, "carbs": 5.3, "weight_per_piece": 150},
    "брокколи": {"kcal": 34, "protein": 2.8, "fat": 0.4, "carbs": 6.6},
    "белокочанная капуста": {"kcal": 25, "protein": 1.8, "fat": 0.1, "carbs": 4.7},
    "салат айсберг / листья салата": {"kcal": 14, "protein": 0.9, "fat": 0.1, "carbs": 1.8},

    # ========================================================
    # 🍌 [ФРУКТЫ, ЯГОДЫ И СЛАДОСТИ]
    # ========================================================
    "банан": {"kcal": 89, "protein": 1.1, "fat": 0.3, "carbs": 22.8, "weight_per_piece": 75},
    "яблоко": {"kcal": 52, "protein": 0.3, "fat": 0.2, "carbs": 13.8, "weight_per_piece": 150},
    "апельсин": {"kcal": 47, "protein": 0.9, "fat": 0.2, "carbs": 11.8, "weight_per_piece": 130},
    "клубника": {"kcal": 32, "protein": 0.7, "fat": 0.3, "carbs": 7.7},
    "черника / голубика": {"kcal": 57, "protein": 0.7, "fat": 0.3, "carbs": 14.5},
    "мед натуральный": {"kcal": 329, "protein": 0.8, "fat": 0.0, "carbs": 80.3, "weight_per_tbsp": 30},

    # ========================================================
    # 🥜 [ОРЕХИ, МАСЛА И ПАСТЫ]
    # ========================================================
    "миндаль": {"kcal": 579, "protein": 21.2, "fat": 49.9, "carbs": 21.6},
    "грецкий орех": {"kcal": 654, "protein": 15.2, "fat": 65.2, "carbs": 13.7},
    "кешью": {"kcal": 553, "protein": 18.2, "fat": 43.8, "carbs": 26.9, "weight_per_piece": 1.5},
    "фундук": {"kcal": 628, "protein": 15.0, "fat": 60.8, "carbs": 16.7, "weight_per_piece": 1.2},
    "бразильский орех": {"kcal": 659, "protein": 14.3, "fat": 67.1, "carbs": 12.3, "weight_per_piece": 4.0},
    "арахисовая паста (без сахара)": {"kcal": 588, "protein": 25.0, "fat": 50.0, "carbs": 20.0, "weight_per_tbsp": 15},
    "масло оливковое / подсолнечное": {"kcal": 884, "protein": 0.0, "fat": 100.0, "carbs": 0.0},
    "масло сливочное 82.5%": {"kcal": 748, "protein": 0.5, "fat": 82.5, "carbs": 0.8},

    # ========================================================
    # 🍞 [ХЛЕБ И ХЛЕБЦЫ]
    # ========================================================
    "хлеб белый (пшеничный)": {"kcal": 265, "protein": 7.5, "fat": 1.0, "carbs": 50.0},
    "хлеб ржаной / бородинский": {"kcal": 207, "protein": 6.8, "fat": 1.3, "carbs": 40.2},
    "хлебцы цельнозерновые": {"kcal": 310, "protein": 10.0, "fat": 2.0, "carbs": 63.0, "weight_per_piece": 10},

    # ========================================================
    # 🏋️‍♂️ [СПОРТПИТ И ДОБАВКИ]
    # ========================================================
    "протеин сывороточный (концентрат/изолят)": {"kcal": 383, "protein": 80.0, "fat": 3.3, "carbs": 6.6, "weight_per_scoop": 30},
    "какао-порошок (натуральный)": {"kcal": 300, "protein": 24.0, "fat": 15.0, "carbs": 10.0, "weight_per_tbsp": 15}
}


def load_database():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_DATABASE

def save_database(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

def save_history(result_kbju):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": result_kbju
    })
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def get_exclusive_product(db, product_name):
    print(f"\n❔ Продукта '{product_name}' нет в базе.")
    choice = input("Хотите внести КБЖУ для этого продукта? (да/нет): ").strip().lower()
    if choice in ["да", "y", "yes"]:
        try:
            print("Введите значения строго на 100 грамм / миллилитров:")
            kcal = float(input("Калории (ккал): "))
            protein = float(input("Белки (г): "))
            fat = float(input("Жиры (г): "))
            carbs = float(input("Углеводы (г): "))
            weight_piece = input("Если есть стандартный вес штуки, введите его в граммах (или Enter): ").strip()
            product_data = {"kcal": kcal, "protein": protein, "fat": fat, "carbs": carbs}
            if weight_piece:
                product_data["weight_per_piece"] = float(weight_piece)
            db[product_name] = product_data
            save_database(db)
            print(f"✅ Продукт '{product_name}' успешно сохранен!")
            return product_name
        except ValueError:
            print("❌ Ошибка ввода. Продукт не добавлен.")
    return None

def find_product(db, search_name):
    search_name = search_name.strip().lower()
    if search_name in db:
        return search_name
    matches = [key for key in db.keys() if search_name in key]
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        print(f"\n🔍 Найдено несколько совпадений:")
        for idx, match in enumerate(matches, 1):
            print(f"{idx}. {match} ({db[match]['kcal']} ккал)")
        try:
            choice = int(input("Выберите номер (или 0 для ввода нового продукта): "))
            if 0 < choice <= len(matches):
                return matches[choice - 1]
        except ValueError:
            pass
    return get_exclusive_product(db, search_name)

def convert_to_grams(db, product_name, value, unit):
    product_info = db.get(product_name, {})
    if unit in ["грамм", "г", "мл"]: return value
    if unit in ["кг", "килограмм"]: return value * 1000
    if unit in ["литр", "л"]: return value * 1000
    if unit in ["шт", "штука"]: return value * product_info.get("weight_per_piece", 100)
    if unit in ["скуп", "черпак"]: return value * product_info.get("weight_per_scoop", 30)
    if unit in ["ст л", "столовая ложка"]: return value * product_info.get("weight_per_tbsp", 15)
    return value

def calculate_kbju(db, recipe_dict, portion=1.0):
    total = {"kcal": 0.0, "protein": 0.0, "fat": 0.0, "carbs": 0.0}
    for product, data in recipe_dict.items():
        if product in db:
            grams = convert_to_grams(db, product, data["value"], data["unit"])
            prod_base = db[product]
            for key in total:
                total[key] += (prod_base[key] * grams / 100)
    return {macro: round(val * portion, 1) for macro, val in total.items()}

def build_recipe_interactively(db):
    user_recipe = {}
    print("--- 🍏 Интерактивный счетчик макронутриентов 🍏 ---")
    print("Команды: 'выход' - посчитать итог, 'база' - посмотреть доступные продукты.")
    while True:
        raw_input = input("\nВведите продукт: ").strip()
        if raw_input.lower() == 'выход': break
        if raw_input.lower() == 'база':
            print("\nПродукты в базе:", ", ".join(sorted(db.keys())))
            continue
        if not raw_input: continue
        product = find_product(db, raw_input)
        if not product: continue

        unit = input(f"Мера измерения для '{product}' (г, мл, кг, шт, скуп, ст л): ").strip().lower()
        try:
            value = float(input(f"Количество ({unit}): "))
            user_recipe[product] = {"value": value, "unit": unit}
        except ValueError:
            print("❌ Ошибка: введите число.")

    return user_recipe


def show_history_by_date():
    if not os.path.exists(HISTORY_FILE):
        print("\n📭 История приемов пищи пока пуста.")
        return

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            print("\n❌ Файл истории поврежден.")
            return

    # Извлекаем только уникальные даты (без времени)
    available_dates = sorted(list(set(item["timestamp"].split()[0] for item in history)))

    print("\n📅 Доступные даты в истории:")
    for d in available_dates:
        print(f" - {d}")

    target_date = input(
        f"\nВведите дату для просмотра (ГГГГ-ММ-ДД) или нажмите Enter для сегодняшней ({datetime.now().strftime('%Y-%m-%d')}): ").strip()
    if not target_date:
        target_date = datetime.now().strftime('%Y-%m-%d')

    day_total = {"kcal": 0.0, "protein": 0.0, "fat": 0.0, "carbs": 0.0}
    meals_found = 0

    print(f"\n--- 📋 Приемы пищи за {target_date} ---")
    for item in history:
        # Проверяем совпадение даты
        if item["timestamp"].split()[0] == target_date:
            meals_found += 1
            data = item["data"]
            print(
                f"⏱️ [{item['timestamp'].split()[1]}] Калории: {data['kcal']} | Б: {data['protein']}г | Ж: {data['fat']}г | У: {data['carbs']}г")
            for key in day_total:
                day_total[key] += data[key]

    if meals_found > 0:
        print("-" * 50)
        print(
            f"📊 ВСЕГО ЗА ДЕНЬ: {round(day_total['kcal'], 1)} ккал | Б: {round(day_total['protein'], 1)}г | Ж: {round(day_total['fat'], 1)}г | У: {round(day_total['carbs'], 1)}г")
    else:
        print(f"🤷‍♂️ За {target_date} записей не найдено.")


if __name__ == "__main__":
    FOOD_DB = load_database()

    print("=== Главное меню ===")
    print("1. Посчитать новый прием пищи")
    print("2. Посмотреть историю КБЖУ по датам")

    mode = input("\nВыберите действие (1 или 2): ").strip()

    if mode == "1":
        recipe = build_recipe_interactively(FOOD_DB)
        if recipe:
            try:
                portion = float(input("\nКакую часть порции вы съели? (1.0 = всё, 0.75 = 3/4): "))
            except ValueError:
                portion = 1.0
            final_kbju = calculate_kbju(FOOD_DB, recipe, portion)
            print(f"\n📊 Итоговый расчет КБЖУ вашей порции: {final_kbju}")
            save_history(final_kbju)
            print("💾 Прием пищи успешно записан в историю (`meal_history.json`)!")
    elif mode == "2":
        show_history_by_date()
    else:
        print("❌ Неверный выбор. Перезапустите программу.")





