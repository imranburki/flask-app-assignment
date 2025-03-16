import json
import psycopg2

# Load JSON data
with open('blogdata/blogdata.json', 'r', encoding='utf-8') as file:
    blog_data = json.load(file)

# Database connection
conn = psycopg2.connect(
    dbname="blogdb",
    user="bloguser",
    password="bloguser17899",
    host="localhost"
)
cur = conn.cursor()

# Insert only the first 5 records
for post in blog_data["blog_posts"][:5]:  # Slice to get first 5 records
    cur.execute("""
        INSERT INTO blog_posts (title, author, date, tags, content_path)
        VALUES (%s, %s, %s, %s, %s)
    """, (post["title"], post["author"], post["date"], post["tags"], post["content_path"]))

# Commit and close
conn.commit()
cur.close()
conn.close()

print("Inserted first 5 records successfully.")
