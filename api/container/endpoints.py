"""Routes for module container"""
import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data

container_endpoints = Blueprint('container', __name__)
UPLOAD_FOLDER = "img"


@container_endpoints.route('/read', methods=['GET'])
def read():
    """Routes for module get list container"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM container"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    connection.close()
    return jsonify({"message": "OK", "datas": results}), 200

@container_endpoints.route('/read/<id_ruangan>', methods=['GET'])
def readbyid(id_ruangan):
    """Routes for module get list container"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM container where id_ruangan=%s"
    select_id = (id_ruangan,)
    cursor.execute(select_query, select_id)
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    connection.close()
    return jsonify({"message": "OK", "datas": results}), 200


@container_endpoints.route('/create', methods=['POST'])
def create():
    """Routes for module create a book"""
    id_ruangan = request.form['id_ruangan']
    nama_container = request.form['nama_container']

    uploaded_file = request.files.get('gambar_container')
    if uploaded_file and uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        gambar_container = uploaded_file.filename
    else:
        gambar_container = 'default.png'  # Use the default image filename

    connection = get_connection()
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO container (id_ruangan, nama_container, gambar_container) 
        VALUES (%s, %s, %s)
    """
    request_insert = (
        id_ruangan,
        nama_container,
        gambar_container
    )
    cursor.execute(insert_query, request_insert)
    connection.commit()  # Commit changes to the database
    new_id = cursor.lastrowid  # Get the newly inserted container's ID
    cursor.close()

    if new_id:
        return jsonify({"title": nama_container, "message": "Inserted", "id_container": new_id}), 201
    return jsonify({"message": "Can't Insert Data"}), 500



@container_endpoints.route('/delete/<id_container>', methods=['DELETE'])
def delete(id_container):
    connection = get_connection()
    cursor = connection.cursor()
    delete_query = "DELETE FROM container WHERE id_container=%s"
    delete_id = (id_container,)
    cursor.execute(delete_query, delete_id)
    connection.commit()
    cursor.close()
    return jsonify({
        "message": "Deleted"
    }), 200


@container_endpoints.route('/update/<id_container>', methods=['POST'])
def update(id_container):
    """Routes for module update a book"""
    nama_container = request.form['nama_container']

    uploaded_file = request.files['gambar_container']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        connection = get_connection()
        cursor = connection.cursor()

        update_query = "UPDATE container SET nama_container=%s, gambar_container=%s WHERE id_container=%s"
        update_request = (nama_container, uploaded_file.filename, id_container)
        cursor.execute(update_query, update_request)
        connection.commit()
        cursor.close()
        data = {"message": "updated", "id_container": id_container}
        return jsonify(data), 200


# @container_endpoints.route("/upload", methods=["POST"])
# def upload():
#     """Routes for upload file"""
#     uploaded_file = request.files['file']
#     if uploaded_file.filename != '':
#         file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
#         uploaded_file.save(file_path)
#         return jsonify({"message": "ok", "data": "uploaded", "file_path": file_path}), 200
#     return jsonify({"err_message": "Can't upload data"}), 400