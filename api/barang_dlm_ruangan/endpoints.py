"""Routes for module books"""
import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data

barang_dlm_ruangan_endpoints = Blueprint('barang_dlm_ruangan', __name__)
UPLOAD_FOLDER = "img"


@barang_dlm_ruangan_endpoints.route('/read', methods=['GET'])
def read():
    """Routes for module get list books"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM barang_dlm_ruangan"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    connection.close()
    return jsonify({"message": "OK", "datas": results}), 200

@barang_dlm_ruangan_endpoints.route('/read/<id_ruangan>', methods=['GET'])
def readid(id_ruangan):
    """Routes for module get list books"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM barang_dlm_ruangan WHERE id_ruangan=%s"
    cursor.execute(select_query, (id_ruangan,))
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    connection.close()
    return jsonify({"message": "OK", "datas": results}), 200


@barang_dlm_ruangan_endpoints.route('/create', methods=['POST'])
def create():
    """Routes for module create a book"""
    id_ruangan = request.form['id_ruangan']
    nama_barang_dlm_ruangan = request.form['nama_barang_dlm_ruangan']
    desc_barang_dlm_ruangan = request.form['desc_barang_dlm_ruangan']
    qnty_barang_dlm_ruangan = request.form['qnty_barang_dlm_ruangan']

    uploaded_file = request.files['gambar_barang_dlm_ruangan']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        connection = get_connection()
        cursor = connection.cursor()
        insert_query = "INSERT INTO barang_dlm_ruangan (id_ruangan, nama_barang_dlm_ruangan, desc_barang_dlm_ruangan, qnty_barang_dlm_ruangan, gambar_barang_dlm_ruangan) VALUES (%s, %s, %s)"
        request_insert = (id_ruangan, nama_barang_dlm_ruangan, desc_barang_dlm_ruangan, qnty_barang_dlm_ruangan, uploaded_file.filename)
        cursor.execute(insert_query, request_insert)
        connection.commit()  # Commit changes to the database
        cursor.close()
        new_id = cursor.lastrowid  # Get the newly inserted book's ID\
        if new_id:
            return jsonify({"title": nama_barang_dlm_ruangan, "message": "Inserted", "id_barang_dlm_ruangan": new_id}), 201
        return jsonify({"message": "Cant Insert Data"}), 500

@barang_dlm_ruangan_endpoints.route('/delete/<id_barang_dlm_ruangan>', methods=['DELETE'])
def delete(id_barang_dlm_ruangan):
    connection = get_connection()
    cursor = connection.cursor()
    delete_query = "DELETE FROM barang_dlm_ruangan WHERE id_barang_dlm_ruangan=%s"
    delete_id = (id_barang_dlm_ruangan,)
    cursor.execute(delete_query, delete_id)
    connection.commit()
    cursor.close()
    return jsonify({
        "message": "Deleted"
    }), 200


@barang_dlm_ruangan_endpoints.route('/update/<id_barang_dlm_ruangan>', methods=['PUT'])
def update(id_barang_dlm_ruangan):
    """Routes for module update a book"""
    nama_barang_dlm_ruangan = request.form['nama_barang_dlm_ruangan']
    desc_barang_dlm_ruangan = request.form['desc_barang_dlm_ruangan']
    qnty_barang_dlm_ruangan = request.form['qnty_barang_dlm_ruangan']

    uploaded_file = request.files['gambar_barang_dlm_ruangan']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        connection = get_connection()
        cursor = connection.cursor()

        update_query = "UPDATE barang_dlm_ruangan SET nama_barang_dlm_ruangan=%s, gambar_barang_dlm_ruangan=%s WHERE id_barang_dlm_ruangan=%s"
        update_request = (nama_barang_dlm_ruangan, uploaded_file.filename, id_barang_dlm_ruangan)
        cursor.execute(update_query, update_request)
        connection.commit()
        cursor.close()
        data = {"message": "updated", "id_container": id_barang_dlm_ruangan}
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