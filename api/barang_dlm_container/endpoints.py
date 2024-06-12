"""Routes for module books"""
import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data

barang_dlm_container_endpoints = Blueprint('barang_dlm_container', __name__)
UPLOAD_FOLDER = "img"


@barang_dlm_container_endpoints.route('/read', methods=['GET'])
def read():
    """Routes for module get list books"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM barang_dlm_container"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    connection.close()
    return jsonify({"message": "OK", "datas": results}), 200

@barang_dlm_container_endpoints.route('/read/<id_container>', methods=['GET'])
def readid(id_container):
    """Routes for module get list books"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM barang_dlm_container WHERE id_container=%s"
    cursor.execute(select_query, (id_container,))
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    connection.close()
    return jsonify({"message": "OK", "datas": results}), 200


@barang_dlm_container_endpoints.route('/create', methods=['POST'])
def create():
    """Routes for module create a book"""
    id_container = request.form['id_container']
    nama_barang_dlm_container = request.form['nama_barang_dlm_container']
    desc_barang_dlm_container = request.form['desc_barang_dlm_container']
    qnty_barang_dlm_container = request.form['qnty_barang_dlm_container']

    uploaded_file = request.files['gambar_barang_dlm_container']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        connection = get_connection()
        cursor = connection.cursor()
        insert_query = "INSERT INTO barang_dlm_container (id_container, nama_barang_dlm_container, desc_barang_dlm_container, qnty_barang_dlm_container, gambar_barang_dlm_container) VALUES (%s, %s, %s, %s, %s)"
        request_insert = (id_container, nama_barang_dlm_container, desc_barang_dlm_container, qnty_barang_dlm_container, uploaded_file.filename)
        cursor.execute(insert_query, request_insert)
        connection.commit()  # Commit changes to the database
        cursor.close()
        new_id = cursor.lastrowid  # Get the newly inserted book's ID\
        if new_id:
            return jsonify({"title": nama_barang_dlm_container, "message": "Inserted", "id_barang_dlm_container": new_id}), 201
        return jsonify({"message": "Cant Insert Data"}), 500

@barang_dlm_container_endpoints.route('/delete/<id_barang_dlm_container>', methods=['DELETE'])
def delete(id_barang_dlm_container):
    connection = get_connection()
    cursor = connection.cursor()
    delete_query = "DELETE FROM barang_dlm_container WHERE id_barang_dlm_container=%s"
    delete_id = (id_barang_dlm_container,)
    cursor.execute(delete_query, delete_id)
    connection.commit()
    cursor.close()
    return jsonify({
        "message": "Deleted"
    }), 200


@barang_dlm_container_endpoints.route('/update/<id_barang_dlm_container>', methods=['PUT'])
def update(id_barang_dlm_container):
    """Routes for module update a book"""
    nama_barang_dlm_container = request.form['nama_barang_dlm_container']
    desc_barang_dlm_container = request.form['desc_barang_dlm_container']
    qnty_barang_dlm_container = request.form['qnty_barang_dlm_container']

    uploaded_file = request.files['gambar_barang_dlm_container']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        connection = get_connection()
        cursor = connection.cursor()

        update_query = "UPDATE barang_dlm_container SET nama_barang_dlm_container=%s, gambar_barang_dlm_container=%s WHERE id_barang_dlm_container=%s"
        update_request = (nama_barang_dlm_container, uploaded_file.filename, id_barang_dlm_container)
        cursor.execute(update_query, update_request)
        connection.commit()
        cursor.close()
        data = {"message": "updated", "id_container": id_barang_dlm_container}
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