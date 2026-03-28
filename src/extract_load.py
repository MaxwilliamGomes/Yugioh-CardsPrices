import requests
import pandas as pd
import time
import psycopg2
import os
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

# 🔧 CONFIG
BASE_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

ARQUETIPOS = [
    "Blue-Eyes",
    "Dark Magician",
    "Red-Eyes",
    "Elemental HERO",
    "Cyber Dragon",
    "Toon",
    "Dragonmaid",
    "Branded",
    "Exodia",
    "Sky Striker"
]

DELAY = 1  # segundos entre requests
MAX_RETRIES = 3

# 🗄️ DATABASE CONFIG
DB_CONFIG = {
    "host":     os.getenv("DB_HOST"),
    "port":     os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

# 📦 STORAGE
cards_dict = {}   # para evitar duplicidade
prices_list = []
sets_list = []

# 🔁 FUNÇÃO DE REQUEST COM RETRY
def fetch_data(params):
    for attempt in range(MAX_RETRIES):
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            return response.json()

        elif response.status_code == 429:
            print("Rate limit atingido, esperando...")
            time.sleep(5)

        else:
            print(f"Erro {response.status_code}, tentativa {attempt+1}")
            time.sleep(2)

    return None

# 🚀 LOOP PRINCIPAL
for archetype in ARQUETIPOS:
    print(f"🔎 Buscando arquétipo: {archetype}")

    data = fetch_data({"archetype": archetype})

    if not data:
        print(f"❌ Falha ao buscar {archetype}")
        continue

    for card in data.get("data", []):
        card_id = card.get("id")

        # 🃏 DIMENSÃO CARTA (sem duplicar)
        if card_id not in cards_dict:
            image_url = None
            if card.get("card_images"):
                image_url = card["card_images"][0]["image_url"]

            cards_dict[card_id] = {
                "id": card_id,
                "name": card.get("name"),
                "type": card.get("type"),
                "atk": card.get("atk"),
                "def": card.get("def"),
                "level": card.get("level"),
                "race": card.get("race"),
                "attribute": card.get("attribute"),
                "archetype": card.get("archetype"),
                "image_url": image_url
            }

        # 💰 FATO PREÇOS
        prices = card.get("card_prices", [{}])[0]

        marketplace_map = {
            "cardmarket": ("cardmarket_price", "EUR"),
            "tcgplayer": ("tcgplayer_price", "USD"),
            "ebay": ("ebay_price", "USD"),
            "amazon": ("amazon_price", "USD")
        }

        for marketplace, (field, currency) in marketplace_map.items():
            price = prices.get(field)

            if price and float(price) > 0:
                prices_list.append({
                    "card_id": card_id,
                    "marketplace": marketplace,
                    "price": float(price),
                    "currency": currency
                })

        # 📦 FATO SETS
        for card_set in card.get("card_sets", []):
            set_price = card_set.get("set_price")
            try:
                set_price_float = float(set_price) if set_price else None
            except (ValueError, TypeError):
                set_price_float = None

            sets_list.append({
                "card_id": card_id,
                "set_name": card_set.get("set_name"),
                "set_code": card_set.get("set_code"),
                "set_rarity": card_set.get("set_rarity"),
                "set_price": set_price_float
            })

    # ⏳ respeitando rate limit
    time.sleep(DELAY)

# 📊 DATAFRAMES
df_cards = pd.DataFrame(cards_dict.values())
df_prices = pd.DataFrame(prices_list)
df_sets = pd.DataFrame(sets_list)

# 🔧 HELPER: converte float do Pandas pra int ou None
def safe_int(val):
    if pd.isna(val):
        return None
    return int(val)

# 💾 SAVE TO POSTGRES
try:
    conn = psycopg2.connect(**DB_CONFIG)
    conn.set_client_encoding('UTF8')
    cur = conn.cursor()

    # 🗂️ DROPAR E RECRIAR TABELAS
    print("📋 Criando tabelas...")

    cur.execute("DROP TABLE IF EXISTS card_sets")
    cur.execute("DROP TABLE IF EXISTS card_prices")
    cur.execute("DROP TABLE IF EXISTS cards")

    cur.execute("""
        CREATE TABLE cards (
            id BIGINT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            type VARCHAR(100),
            atk INTEGER,
            def INTEGER,
            level INTEGER,
            race VARCHAR(100),
            attribute VARCHAR(50),
            archetype VARCHAR(100),
            image_url VARCHAR(500)
        )
    """)

    cur.execute("""
        CREATE TABLE card_prices (
            id SERIAL PRIMARY KEY,
            card_id BIGINT NOT NULL,
            marketplace VARCHAR(50) NOT NULL,
            price NUMERIC(10, 2) NOT NULL,
            currency VARCHAR(10),
            FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE card_sets (
            id SERIAL PRIMARY KEY,
            card_id BIGINT NOT NULL,
            set_name VARCHAR(255),
            set_code VARCHAR(50),
            set_rarity VARCHAR(100),
            set_price NUMERIC(10, 2),
            FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE
        )
    """)

    # 📥 INSERIR CARTAS
    print("💾 Inserindo cartas...")
    insert_cards = """
        INSERT INTO cards (id, name, type, atk, def, level, race, attribute, archetype, image_url)
        VALUES %s
        ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            type = EXCLUDED.type,
            atk = EXCLUDED.atk,
            def = EXCLUDED.def,
            level = EXCLUDED.level,
            race = EXCLUDED.race,
            attribute = EXCLUDED.attribute,
            archetype = EXCLUDED.archetype,
            image_url = EXCLUDED.image_url
    """

    cards_data = [
        (int(row['id']), row['name'], row['type'],
         safe_int(row['atk']), safe_int(row['def']), safe_int(row['level']),
         row['race'], row['attribute'], row['archetype'], row['image_url'])
        for _, row in df_cards.iterrows()
    ]

    if cards_data:
        execute_values(cur, insert_cards, cards_data)

    # 📥 INSERIR PREÇOS
    print("💰 Inserindo preços...")
    insert_prices = """
        INSERT INTO card_prices (card_id, marketplace, price, currency)
        VALUES %s
    """

    prices_data = [
        (row['card_id'], row['marketplace'], row['price'], row['currency'])
        for _, row in df_prices.iterrows()
    ]

    if prices_data:
        execute_values(cur, insert_prices, prices_data)

    # 📥 INSERIR SETS
    print("📦 Inserindo sets...")
    insert_sets = """
        INSERT INTO card_sets (card_id, set_name, set_code, set_rarity, set_price)
        VALUES %s
    """

    sets_data = [
        (row['card_id'], row['set_name'], row['set_code'], row['set_rarity'],
         row['set_price'] if pd.notna(row['set_price']) else None)
        for _, row in df_sets.iterrows()
    ]

    if sets_data:
        execute_values(cur, insert_sets, sets_data)

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Dados salvos no Postgres!")

except Exception as e:
    print(f"❌ Erro ao conectar ao banco: {e}")
    print("💡 Certifique-se de que o Docker está rodando: docker-compose up -d")

# 📊 RELATÓRIO FINAL
print("\n✅ Finalizado!")
print(f"Cartas únicas: {len(df_cards)}")
print(f"Registros de preço: {len(df_prices)}")
print(f"Registros de sets: {len(df_sets)}")