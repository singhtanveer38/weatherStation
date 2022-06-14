import snowflake.connector
import credentials
from datetime import datetime
import fetch
import time

conn = snowflake.connector.connect(user=credentials.user, password=credentials.password, account=credentials.account)
curr = conn.cursor()

try:
	curr.execute("use role sysadmin")
	print("Using role sysadmin")

	curr.execute(f"create database {credentials.db}")
	print(f"Database {credentials.db} created")
	
	curr.execute(f"use database {credentials.db}")
	print(f"Using database {credentials.db}")

	curr.execute(f"create table {credentials.table} (eventdate datetime, temp float)")
	print(f"{credentials.table} table created")

	curr.execute(f"create warehouse {credentials.wh} warehouse_size={credentials.wh_size} auto_suspend=10 auto_resume=true")
	print(f"{credentials.wh} warehouse created")

	curr.execute(f"use warehouse {credentials.wh}")
	print(f"Using {credentials.wh} warehouse")

	while True:
		weather = fetch.fetch()

		dt = datetime.fromtimestamp(weather["dt"]).strftime("%Y-%m-%d %H:%M:%S")
		temp = weather["main"]["temp"]
		# sunrise = weather["sys"]["sunrise"]
		# sunset = weather["sys"]["sunset"]
		# description = weather["weather"][0]["description"]

		print(f'{dt}, {temp}')

		curr.execute(f'insert into {credentials.table} values ({dt}, {temp})')

		# print(f'{dt}, {temp}, {sunrise}, {sunset}, {description}')

		time.sleep(10)

	conn.close()

except Exception as e:
	print(e)


# temp["dt"]
# temp["main"]["temp"]
# temp["sys"]["sunrise"]
# temp["sys"]["sunset"]
# temp["weather"]["description"]