from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# 连接到MySQL数据库的函数


def get_db_connection():
    connection = mysql.connector.connect(
        host="your_host",       # MySQL服务器地址
        user="your_username",   # 用户名
        password="your_password",  # 密码
        database="information_schema"  # 使用 information_schema 获取数据库信息
    )
    return connection

# 获取所有数据库名称


def get_databases():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT schema_name FROM schemata;")
    databases = [row['schema_name'] for row in cursor.fetchall()]
    conn.close()
    return databases

# 获取某个数据库中的所有表名


def get_tables(database_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        f"SELECT table_name FROM tables WHERE table_schema='{database_name}';")
    tables = [row['table_name'] for row in cursor.fetchall()]
    conn.close()
    return tables

# 获取某个表的所有列名


def get_columns(database_name, table_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        f"SELECT column_name FROM columns WHERE table_schema='{database_name}' AND table_name='{table_name}';")
    columns = [row['column_name'] for row in cursor.fetchall()]
    conn.close()
    return columns

# 查询数据


def query_data(database_name, table_name, selected_columns):
    conn = mysql.connector.connect(
        host="your_host",
        user="your_username",
        password="your_password",
        database=database_name
    )
    cursor = conn.cursor(dictionary=True)
    columns_str = ", ".join(selected_columns)
    query = f"SELECT {columns_str} FROM {table_name};"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows


@app.route('/')
def index():
    databases = get_databases()
    return render_template('index.html', databases=databases)


@app.route('/get_tables', methods=['POST'])
def get_tables_route():
    database_name = request.json.get('database_name')
    tables = get_tables(database_name)
    return jsonify(tables)


@app.route('/get_columns', methods=['POST'])
def get_columns_route():
    database_name = request.json.get('database_name')
    table_name = request.json.get('table_name')
    columns = get_columns(database_name, table_name)
    return jsonify(columns)


@app.route('/query_data', methods=['POST'])
def query_data_route():
    database_name = request.json.get('database_name')
    table_name = request.json.get('table_name')
    selected_columns = request.json.get('selected_columns')
    data = query_data(database_name, table_name, selected_columns)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
