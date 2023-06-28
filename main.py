import sqlite3
from flask import Flask, request
import paho.mqtt.client as mqtt
# Kết nối đến SQLite database
conn = sqlite3.connect('database.db')
# Xác định cấu trúc bảng dữ liệu
create_table_query = '''
	CREATE TABLE IF NOT EXISTS data (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		value TEXT NOT NULL
	)
'''
# Tạo bảng trong database
conn.execute(create_table_query)
# Lưu trữ dữ liệu vào bảng "data"
def save_data(value):
	insert_query = f"INSERT INTO data (value) VALUES ('{value}')"
	conn.execute(insert_query)
	conn.commit()
	print("Data saved successfully")
# Truy xuất dữ liệu từ bảng "data"
def get_data():
	select_query = "SELECT * FROM data"
	result = conn.execute(select_query)
	for row in result:
		print(row[0], row[1])
# Khởi tạo Flask app và MQTT client
app = Flask(__name__)
mqtt_client = mqtt.Client()
# Các route và hàm xử lý của Flask app
@app.route('/api/send', methods = ['POST'])
def send_data():
	data = request.json.get('data')
	save_data(data)
	mqtt_client.publish('data_topic', data)
	return 'Data sent successfully'
@app.route('/api/read', methods = ['GET'])
def read_data():
	get_data()
	return 'Data read successfully'
# MQTT server callbacks
def on_connect(client, userdata, flags, rc):
	print('Connected to MQTT broker')
	mqtt_client.subscribe('data_topic')
def on_message(client, userdata, msg):
	data = msg.payload.decode()
	save_data(data)
# Khi Flask app được chạy, kết nối MQTT client và bắt đầu lắng nghe MQTT messages
if __name__ == '__main__':
	mqtt_client.on_connect = on_connect
	mqtt_client.on_message = on_message
	mqtt_client.connect('localhost', 1883, 60)
	mqtt_client.loop_start()
	app.run()
# Đóng kết nối đến SQLite database
conn.close()

# 1/Với HTTP server:
# API /api/send nhận phương thức POST để gửi dữ liệu. Dữ liệu được lưu vào database bằng cách thực hiện một câu lệnh INSERT vào bảng data.  
# Sau đó, dữ liệu được publish lên MQTT topic data_topic.
# API /api/read nhận phương thức GET để đọc dữ liệu. Dữ liệu được truy vấn từ database bằng câu lệnh SELECT và trả về dưới dạng JSON.

# 2/Với MQTT server:
# Khi MQTT client được kết nối thành công với MQTT broker, callback on_connect được gọi và MQTT client subscribe vào MQTT topic data_topic.
# Callback on_message được gọi khi MQTT client nhận được một message trên MQTT topic. 
# Message này được giải mã và lưu vào database bằng câu lệnh INSERT.

# 3/Database trong hệ thống này được sử dụng để lưu trữ dữ liệu gửi và nhận từ HTTP và MQTT server.  
# Để thực hiện việc lưu trữ và truy xuất dữ liệu, hệ thống sử dụng một database SQLite.
# Đầu tiên, khi hệ thống chạy, kết nối đến SQLite database được thiết lập. 
# Sau đó, hệ thống tạo một bảng trong database (nếu chưa tồn tại) để lưu trữ dữ liệu. 
# Dữ liệu được lưu trữ trong bảng "data" với hai cột: "id" và "value".

















# from flask import Flask, request
# import paho.mqtt.client as mqtt
# import mysql.connector
# app = Flask(__name__)
# mqtt_client = mqtt.Client()
# db = mysql.connector.connect(
#   host = "localhost",
#   user = "admin2",
#   password = "admin",
#   database = "database"
# )
# @app.route('/api/data', methods = ['POST'])
# def store_data():
# 	data = request.get_json()
# 	# Lưu dữ liệu vào database
# 	cursor = db.cursor()
# 	sql = "INSERT INTO data (value) VALUES (%s)"
# 	val = (data['value'],)
# 	cursor.execute(sql, val)
# 	db.commit()
# 	cursor.close()
# 	# Publish dữ liệu lên MQTT
# 	mqtt_client.publish('data', data['value'])
# 	return 'Data stored successfully'
# @app.route('/api/data', methods=['GET'])
# def read_data():
# 	# Đọc dữ liệu từ database
# 	cursor = db.cursor()
# 	cursor.execute("SELECT value FROM data")
# 	result = cursor.fetchall()
# 	cursor.close()
# 	# Subcribe dữ liệu từ MQTT
# 	mqtt_client.subscribe('data')
# 	return str(result)
# if __name__ == '__main__':
# 	app.run()
# mqtt_client.loop_start()
# from flask import Flask, request
# import paho.mqtt.client as mqtt
# import mysql.connector
# app = Flask(__name__)
# mqtt_client = mqtt.Client()
# db = mysql.connector.connect(
#   host = "localhost",
#   user = "admin1",
#   password = "admin",
#   database = "database1"
# )
# @app.route('/api/data', methods = ['POST'])
# def store_data():
# 	data = request.get_json()
# 	# Lưu dữ liệu vào database
# 	cursor = db.cursor()
# 	sql = "INSERT INTO data (value) VALUES (%s)"
# 	val = (data['value'],)
# 	cursor.execute(sql, val)
# 	db.commit()
# 	cursor.close()
# 	# Publish dữ liệu lên MQTT
# 	mqtt_client.publish('data', data['value'])
# 	return 'Data stored successfully'
# @app.route('/api/data', methods=['GET'])
# def read_data():
# 	# Đọc dữ liệu từ database
# 	cursor = db.cursor()
# 	cursor.execute("SELECT value FROM data")
# 	result = cursor.fetchall()
# 	cursor.close()
# 	# Subcribe dữ liệu từ MQTT
# 	mqtt_client.subscribe('data')
# 	return str(result)
# if __name__ == '__main__':
# 	app.run()
# mqtt_client.loop_start()