from sqlalchemy import create_engine

engine = create_engine("postgresql://bloguser:bloguser17899@localhost/blogdb")

try:
    conn = engine.connect()
    print("✅ Connection successful!")
except Exception as e:
    print("❌ Connection failed:", e)
