#! /usr/bin/python
import psycopg2
import time


def connect():
    return psycopg2.connect("dbname=news")

# 1. What are the most popular three articles of all time?
query1 = """
SELECT articles.title , count(log.path) AS views
FROM articles, log
WHERE log.path LIKE ('%' || articles.slug)
GROUP BY articles.title
ORDER BY views DESC
limit 3;"""

# 2. Who are the most popular article authors of all time?
query2 = """
SELECT author_name , sum(collect.views) AS views
FROM collect
GROUP BY author_name
ORDER BY views DESC;"""

# 3. On which days did more than 1% of requests lead to errors?
query3 = """
SELECT to_char(date,'Mon DD,YYYY') AS date,error_percentage
FROM error_percentage
WHERE error_percentage > 1.0;"""


def most_popular_articles(query1):
    db = connect()
    c = db.cursor()
    c.execute(query1)
    results = c.fetchall()
    for i in range(len(results)):
        title = results[i][0]
        views = results[i][1]
        print(("%s -- %d views" % (title, views)))
    db.close()


def most_popular_authors(query2):
    db = connect()
    c = db.cursor()
    c.execute(query2)
    results = c.fetchall()
    for i in range(len(results)):
        name = results[i][0]
        views = results[i][1]
        print(("%s -- %d views" % (name, views)))
    db.close()


def error_percent(query3):
    db = connect()
    c = db.cursor()
    c.execute(query3)
    results = c.fetchall()
    for i in range(len(results)):
        date = results[i][0]
        err_prc = results[i][1]
        print(("%s -- %.1f %%" % (date, err_prc)))

if __name__ == '__main__':
    print("1. The most popular three articles of all time:")
    most_popular_articles(query1)
    print("\n")
    print("2. The most popular article authors of all time:")
    most_popular_authors(query2)
    print("\n")
    print("3. The days that more than 1.00 of requests lead to errors:")
    error_percent(query3)
