"""Routes for module books"""
import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data

ruangan_endpoints = Blueprint('ruangan', __name__)
UPLOAD_FOLDER = "img"


@ruangan_endpoints.route('/read', methods=['GET'])
def read():
    """Routes for module get list books"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM ruangan"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    connection.close()
    return jsonify({"message": "OK", "datas": results}), 200



@ruangan_endpoints.route('/create', methods=['POST'])
def create():
    """Routes for module create a book"""
    id_pengguna = int(request.form['id_pengguna'])
    nama_ruangan = request.form['nama_ruangan']
    print(id_pengguna)
    print(nama_ruangan)

    uploaded_file = request.files['gambar_ruangan']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        connection = get_connection()
        cursor = connection.cursor()
        insert_query = "INSERT INTO ruangan (id_pengguna, nama_ruangan, gambar_ruangan) VALUES (%s, %s, %s)"
        request_insert = (id_pengguna, nama_ruangan, uploaded_file.filename)
        cursor.execute(insert_query, request_insert)
        connection.commit()  # Commit changes to the database
        cursor.close()
        new_id = cursor.lastrowid  # Get the newly inserted book's ID\
        if new_id:
            return jsonify({"title": nama_ruangan, "message": "Inserted", "id_ruangan": new_id}), 201
        return jsonify({"message": "Cant Insert Data"}), 500


@ruangan_endpoints.route('/delete/<id_ruangan>', methods=['DELETE'])
def delete(id_ruangan):
    connection = get_connection()
    cursor = connection.cursor()
    delete_query = "DELETE FROM ruangan WHERE id_ruangan=%s"
    delete_id = (id_ruangan,)
    cursor.execute(delete_query, delete_id)
    connection.commit()
    cursor.close()
    return jsonify({
        "message": "Deleted"
    }), 200


@ruangan_endpoints.route('/update/<id_ruangan>', methods=['PUT'])
def update(id_ruangan):
    """Routes for module update a book"""
    nama_ruangan = request.form['nama_ruangan']

    uploaded_file = request.files['gambar_ruangan']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        connection = get_connection()
        cursor = connection.cursor()

        update_query = "UPDATE ruangan SET nama_ruangan=%s, gambar_ruangan=%s WHERE id_ruangan=%s"
        update_request = (nama_ruangan, uploaded_file.filename, id_ruangan)
        cursor.execute(update_query, update_request)
        connection.commit()
        cursor.close()
        data = {"message": "updated", "id_container": id_ruangan}
        return jsonify(data), 200

# @books_endpoints.route("/upload", methods=["POST"])
# def upload():
#     """Routes for upload file"""
#     uploaded_file = request.files['file']
#     if uploaded_file.filename != '':
#         file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
#         uploaded_file.save(file_path)
#         return jsonify({"message": "ok", "data": "uploaded", "file_path": file_path}), 200
#     return jsonify({"err_message": "Can't upload data"}), 400