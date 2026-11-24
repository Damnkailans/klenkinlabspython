import json
import os
import pandas as pd


def main() -> None:
    # 3.1 DataFrame с вложенными структурами (списки и словари)
    data = [
        {
            "id": 1,
            "name": "Алексей Иванов",
            "department": "IT",
            "skills": ["Python", "SQL", "Docker"],
            "profile": {"experience_years": 5, "level": "Senior"},
        },
        {
            "id": 2,
            "name": "Мария Смирнова",
            "department": "Analytics",
            "skills": ["Pandas", "Spark", "Tableau"],
            "profile": {"experience_years": 3, "level": "Middle"},
        },
        {
            "id": 3,
            "name": "Дмитрий Кузнецов",
            "department": "IT",
            "skills": ["Go", "Kubernetes"],
            "profile": {"experience_years": 7, "level": "Lead"},
        },
        {
            "id": 4,
            "name": "Елена Попова",
            "department": "Marketing",
            "skills": ["SEO", "Python", "GA4"],
            "profile": {"experience_years": 2, "level": "Junior"},
        },
    ]
    df_nested = pd.DataFrame(data)
    print("3.1 Исходный DataFrame с вложенностью")
    print(df_nested, "\n")

    # 3.2 Сохранение в разных ориентациях
    orientations = ["records", "columns", "index", "split"]
    files = {}

    for orient in orientations:
        fname = f"employees_{orient}.json"
        df_nested.to_json(fname, orient=orient, force_ascii=False, indent=2)
        files[orient] = fname

    # 3.3 Сравнение размеров и структуры
    print("3.3 Сравнение размеров и структуры JSON")
    for orient, fname in files.items():
        size = os.path.getsize(fname)
        with open(fname, "r", encoding="utf-8") as f:
            preview = f.read(180).replace("\n", " ")
        print(f"orient='{orient:<7}' | размер: {size:>4} байт | начало: {preview}...")
    print()

    # 3.4 Чтение JSON обратно и разворачивание вложенности через json_normalize
    with open(files["records"], "r", encoding="utf-8") as f:
        raw_records = json.load(f)

    # Разворачивание вложенного словаря profile
    df_flat_profile = pd.json_normalize(raw_records, sep="_")
    print("3.4a После pd.json_normalize (развёрнут словарь profile)")
    print(df_flat_profile, "\n")

    # Разворачивание списка навыков skills (по одной строке на каждый навык)
    df_flat_skills = pd.json_normalize(
        raw_records,
        record_path=["skills"],
        meta=["id", "name", "department", ["profile", "level"]],
        meta_prefix="emp_",
    ).rename(columns={0: "skill"})
    print("3.4b После pd.json_normalize с record_path='skills'")
    print(df_flat_skills)


if __name__ == "__main__":
    main()
