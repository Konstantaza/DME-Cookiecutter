# etl/load.py
import os
import pandas as pd
from sqlalchemy import create_engine, exc
import getpass

YOUR_LAST_NAME = "iamshchikov"


def get_creds_from_input():
    """
    Интерактивно запрашивает у пользователя креды для Postgres
    прямо в терминале.
    """
    print("  [Load] Пожалуйста, введите учетные данные для PostgreSQL:")
    
    creds = {}
    creds['host'] = input("  Введите PG_HOST: ")
    creds['port'] = input("  Введите PG_PORT: ")
    creds['user'] = input("  Введите PG_USER: ")
    creds['password'] = getpass.getpass("  Введите PG_PASS (ввод будет скрыт): ") # Скрытый ввод пароля
    creds['dbname'] = input("  Введите PG_DBNAME (например homeworks): ")
    
    if not all(creds.values()):
        print("  [Load Ошибка] Не все учетные данные были введены.")
        return None
        
    print("  [Load] Учетные данные приняты.")
    return creds


def load_to_postgres(df: pd.DataFrame, creds: dict, table_name: str):
    """
    Загружает DataFrame в PostgreSQL (первые 100 строк).
    """
    engine = None
    try:
        db_url = (
            f"postgresql+psycopg2://{creds['user']}:{creds['password']}"
            f"@{creds['host']}:{creds['port']}/{creds['dbname']}"
        )
        engine = create_engine(db_url)

        with engine.connect() as conn:
            print("  [Load] Проверка подключения к PostgreSQL... Успешно.")

        # Берем только 100 строк
        df_to_load = df.head(100)

        if df_to_load.empty:
            print(f"  [Load Предупреждение] DataFrame пуст. Валидация не пройдена. Пропускаем.")
            return True

        df_to_load.to_sql(
            name=table_name,
            con=engine,
            schema="public",
            if_exists="replace",
            index=False,
        )

        print(f"  [Load] Первые 100 строк успешно загружены в таблицу '{table_name}'.")
        return True

    except exc.OperationalError as e:
        print(f"  [Load Ошибка] Ошибка подключения к PostgreSQL: {e}")
        return False
    except Exception as e:
        print(f"  [Load Ошибка] Неизвестная ошибка при загрузке в PostgreSQL: {e}")
        return False
    finally:
        if engine:
            engine.dispose()


def save_as_parquet(df: pd.DataFrame, file_name: str, processed_dir: str):
    """
    Сохраняет DataFrame в .parquet в папку processed.
    """
    try:
        # Строим путь от processed_dir
        parquet_path = os.path.join(processed_dir, file_name + ".parquet")
        df.to_parquet(parquet_path, index=False)
        print(f"  [Load] Полные данные сохранены в: {parquet_path}")
        return True
    except Exception as e:
        print(f"  [Load Ошибка] Не удалось сохранить {parquet_path}: {e}")
        return False


def load_all_data(transformed_data: dict[str, pd.DataFrame], root_dir: str):
    """
    Главная функция модуля load.
    """
    print("--- 3. Этап загрузки (LOAD) ---")

    processed_data_dir = os.path.join(root_dir, "data", "processed")
    os.makedirs(processed_data_dir, exist_ok=True)

    # Получаем креды по правильному пути
    creds = get_creds_from_input()
    if creds is None:
        print("  [Load Ошибка] Не удалось получить креды. Загрузка в БД отменена.")
        db_ready = False
    else:
        db_ready = True

    # Проходим по всем трансформированным данным
    for file_name, df in transformed_data.items():
        print(f"  [Load] Обработка: {file_name}")

        # Валидация
        if df.empty:
            print(
                f"  [Load Предупреждение] DataFrame {file_name} пуст. Валидация не пройдена. Пропускаем."
            )
            continue  

        # Сохраняем .parquet
        save_as_parquet(df, file_name, processed_data_dir)

        # Загружаем в БД
        if "count" in df.columns and db_ready:
            print(f"  [Load] Загружаем {file_name} в PostgreSQL...")
            table_name = file_name.lower().replace("dada2_clean_asv_counts_", "")

            if "roots" in table_name:
                load_to_postgres(df, creds, YOUR_LAST_NAME)
            else:
                print(
                    f"  [Load] Пропускаем загрузку {file_name} в БД (загружаем только 'roots')."
                )

        elif "count" not in df.columns and db_ready:
            print(
                f"  [Load] Пропускаем загрузку {file_name} в БД (это не 'counts' файл)."
            )

    print("--- Этап загрузки завершен ---\n")


if __name__ == "__main__":
    print("Запущен etl/load.py как самостоятельный скрипт.")
