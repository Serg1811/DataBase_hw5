import sqlalchemy
import json
import os
from settings import *
from pprint import pprint


def read_json(path_: str):
    with open(path_, encoding='utf-8') as f:
        return json.load(f)


auth = read_json('authenticator.json')

# создаем engine
engine = sqlalchemy.create_engine(f"postgresql://{auth['user']}:{auth['password']}@localhost:5432/{auth['database']}")
con = engine.connect()

# Запросы

print('1. Количество исполнителей в каждом жанре')
res = con.execute("""
SELECT name, COUNT(id) e_col FROM genre g
JOIN genre_executor a ON id = id_genre
GROUP BY g.name
ORDER BY e_col DESC;
""").fetchall()
pprint(res)
print('\n'*2)

print('2. Количество треков, вошедших в альбомы 2019-2020 годов')
res = con.execute("""
SELECT COUNT(*) FROM album a
JOIN track t ON a.id = id_album
WHERE year_of_release BETWEEN 2019 AND 2020
""").fetchall()
print(res)
print('\n'*2)

print('3. Средняя продолжительность треков по каждому альбому')
res = con.execute("""
SELECT a.name, round(AVG(duration)/(60*1000), 3), 'мин.' avg_d FROM album a
JOIN track t ON a.id = id_album
GROUP BY a.name
ORDER BY avg_d;
""").fetchall()
pprint(res)
print('\n'*2)

print('4. Все исполнители, которые не выпустили альбомы в 2020 году')
res = con.execute("""
SELECT DISTINCT e.name FROM album a
JOIN executor_album e_a ON a.id = id_album
JOIN executor e ON e.id = id_executor
WHERE year_of_release != 2020
ORDER BY e.name;
""").fetchall()
pprint(res)
print('\n'*2)

print('5. Названия сборников, в которых присутствует конкретный исполнитель (выберите сами)')
res = con.execute("""
SELECT DISTINCT c.name FROM executor e
JOIN executor_album e_a ON e.id = id_executor
JOIN album a ON a.id = e_a.id_album
JOIN track t ON a.id = t.id_album
JOIN collection_track c_t ON t.id = id_track
JOIN collection c ON c.id = id_collection
WHERE e.name iLIKE '%%The Cardigans%%'
ORDER BY c.name;
""").fetchall()
pprint(res)
print('\n'*2)

print('6. Название альбомов, в которых присутствуют исполнители более 1 жанра')
res = con.execute("""
SELECT DISTINCT a.name FROM album a
JOIN executor_album ON a.id = id_album
JOIN executor e ON e.id =id_executor
WHERE e.id in (SELECT id_executor FROM genre_executor
               GROUP BY id_executor
               HAVING COUNT(id_executor)>1)
ORDER BY a.name;
""").fetchall()
pprint(res)
print('\n'*2)

print('7. Наименование треков, которые не входят в сборники')
res = con.execute("""
SELECT name FROM track
WHERE id not in (SELECT DISTINCT id_track FROM collection_track)
ORDER BY id;
""").fetchall()
pprint(res)
print('\n'*2)

print('8. Исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть'
      'несколько)')
res = con.execute("""
SELECT DISTINCT e.name FROM executor e
JOIN executor_album e_a ON e.id = id_executor
JOIN album a ON a.id = e_a.id_album
JOIN track t ON a.id = t.id_album
WHERE duration = (SELECT MIN(duration) FROM track)
ORDER BY e.name;
""").fetchall()
pprint(res)
print('\n'*2)

print('9. Название альбомов, содержащих наименьшее количество треков')
res = con.execute("""
SELECT name FROM album
WHERE id in (SELECT id_album FROM track
             GROUP BY id_album
             HAVING COUNT(id_album)=(SELECT DISTINCT COUNT(id_album) c FROM track
                                     GROUP BY id_album
                                     ORDER BY c
                                     LIMIT 1))
ORDER BY id;
""").fetchall()
pprint(res)
