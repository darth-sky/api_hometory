"""Routes for module pengguna"""
import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data

pengguna_endpoints = Blueprint('pengguna', __name__)
UPLOAD_FOLDER = "img"


@pengguna_endpoints.route('/read', methods=['GET'])
def read():
    """Routes for module get list pengguna"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM pengguna"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    return jsonify({"message": "OK", "datas": results}), 200

@pengguna_endpoints.route('/readByIdUser/<id_pengguna>', methods=['GET'])
def readByUserId(id_pengguna):
    """Routes for module get list pengguna"""
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        select_query = "SELECT * FROM pengguna WHERE id_pengguna = %s"
        select_request = (id_pengguna,)  # Tuple harus memiliki koma jika hanya ada satu elemen
        cursor.execute(select_query, select_request)
        results = cursor.fetchall()
    # except mysql.connector.Error as err:
    #     return jsonify({"message": "Error", "error": str(err)}), 500
    finally:
        cursor.close()  # Pastikan cursor selalu ditutup
        connection.close()  # Pastikan koneksi selalu ditutup
    return jsonify({"message": "OK", "datas": results}), 200



# @pengguna_endpoints.route('/update/<id_pengguna>', methods=['PUT'])
# def update(product_id):
#     """Routes for module update a book"""
#     title = request.form['title']
#     description = request.form['description']

#     connection = get_connection()
#     cursor = connection.cursor()

#     update_query = "UPDATE tb_pengguna SET title=%s, description=%s WHERE id_pengguna=%s"
#     update_request = (title, description, product_id)
#     cursor.execute(update_query, update_request)
#     connection.commit()
#     cursor.close()
#     data = {"message": "updated", "id_pengguna": product_id}
#     return jsonify(data), 200

@pengguna_endpoints.route('/update/<id_pengguna>', methods=['PUT'])
def update(id_pengguna):
    """Routes for module update a book"""
    email = request.form['email']
    longtitude = request.form['longtitude']
    latitude = request.form['latitude']

    uploaded_file = request.files['foto_profil']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        connection = get_connection()
        cursor = connection.cursor()

        update_query = "UPDATE pengguna SET email=%s, longtitude=%s, latitude=%s, foto_profil=%s where id_pengguna = %s"
        update_request = (email, longtitude, latitude, uploaded_file.filename, id_pengguna)
        cursor.execute(update_query, update_request)
        connection.commit()
        cursor.close()
        data = {"message": "updated", "id_pengguna": id_pengguna}
        return jsonify(data), 200

@pengguna_endpoints.route('/updateRole/<id_pengguna>', methods=['PUT'])
def updateRole(id_pengguna):
    """Routes for module update a book"""


    connection = get_connection()
    cursor = connection.cursor()

    update_query = "UPDATE pengguna SET role=%s WHERE id_pengguna=%s"
    update_request = ("pro", id_pengguna)
    cursor.execute(update_query, update_request)
    connection.commit()
    cursor.close()
    data = {"message": "updated", "id_pengguna": id_pengguna}
    return jsonify(data), 200


@pengguna_endpoints.route('/delete/<product_id>', methods=['GET'])
def delete(product_id):
    """Routes for module to delete a book"""
    connection = get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM tb_pengguna WHERE id_pengguna = %s"
    delete_id = (product_id,)
    cursor.execute(delete_query, delete_id)
    connection.commit()
    cursor.close()
    data = {"message": "Data deleted", "id_pengguna": product_id}
    return jsonify(data)


@pengguna_endpoints.route("/upload", methods=["POST"])
def upload():
    """Routes for upload file"""
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        return jsonify({"message": "ok", "data": "uploaded", "file_path": file_path}), 200
    return jsonify({"err_message": "Can't upload data"}), 400


@pengguna_endpoints.route('/userReadRuangan/<id_pengguna>', methods=['GET'])
def readTotalRuangan(id_pengguna):
    """Routes for module get list books"""
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        select_query = "SELECT COUNT(*) AS jumlah_ruangan FROM ruangan WHERE id_pengguna = %s GROUP BY id_pengguna"
        select_request = (id_pengguna,)
        cursor.execute(select_query, select_request)
        results = cursor.fetchall()
    finally:
        cursor.close()  # Close the cursor after query execution
        connection.close()
        return jsonify({"message": "OK", "datas": results}), 200
    
@pengguna_endpoints.route('/userReadBrgContainer/<id_pengguna>', methods=['GET'])
def readTotalBrgRuangan(id_pengguna):
    """Routes for module get list books"""
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        select_query = "SELECT COUNT(b.id_barang_dlm_container) AS jumlah_barang_container FROM pengguna p JOIN ruangan r ON p.id_pengguna = r.id_pengguna JOIN container c ON r.id_ruangan = c.id_ruangan JOIN barang_dlm_container b ON c.id_container = b.id_container WHERE p.id_pengguna = %s GROUP BY p.id_pengguna"
        select_request = (id_pengguna,)
        cursor.execute(select_query, select_request)
        results = cursor.fetchall()
    finally:
        cursor.close()  # Close the cursor after query execution
        connection.close()
        return jsonify({"message": "OK", "datas": results}), 200
    
@pengguna_endpoints.route('/userReadBrgRuangan/<id_pengguna>', methods=['GET'])
def readTotalBrgContainer(id_pengguna):
    """Routes for module get list books"""
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        select_query = """SELECT COUNT(b.id_barang_dlm_ruangan) AS jumlah_barang_ruangan 
        FROM pengguna p JOIN ruangan r ON p.id_pengguna = r.id_pengguna JOIN barang_dlm_ruangan b ON r.id_ruangan = b.id_ruangan
        WHERE p.id_pengguna = %s
        GROUP BY p.id_pengguna;
        """
        select_request = (id_pengguna,)
        cursor.execute(select_query, select_request)
        results = cursor.fetchall()
    finally:
        cursor.close()  # Close the cursor after query execution
        connection.close()
        return jsonify({"message": "OK", "datas": results}), 200