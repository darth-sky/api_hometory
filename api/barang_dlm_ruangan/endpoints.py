"""Routes for module books"""
import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data

barang_dlm_ruangan_endpoints = Blueprint('barang_dlm_ruangan', __name__)
UPLOAD_FOLDER = "img"

@barang_dlm_ruangan_endpoints.route('/readTotalBarang/<id_barang_dlm_ruangan>', methods=['GET'])
def readLocation(id_barang_dlm_ruangan):
    """Routes for module get list books"""
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        select_query = "SELECT ruangan.nama_ruangan FROM barang_dlm_ruangan INNER JOIN ruangan ON barang_dlm_ruangan.id_ruangan = ruangan.id_ruangan  WHERE barang_dlm_ruangan.id_barang_dlm_ruangan = %s"
        select_request = (id_barang_dlm_ruangan,)
        cursor.execute(select_query, select_request)
        results = cursor.fetchall()
    finally:
        cursor.close()  # Close the cursor after query execution
        connection.close()
        return jsonify({"message": "OK", "datas": results}), 200


@barang_dlm_ruangan_endpoints.route('/readAll', methods=['GET'])
def readAll():
    """Routes for module get list books"""
    page = int(request.args.get('page', 1))
    per_page = 5  # Tetapkan jumlah item per halaman

    # Hitung offset
    offset = (page - 1) * per_page

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
                 SELECT *
                 FROM barang_dlm_ruangan
                 LIMIT %s OFFSET %s
             """
    cursor.execute(query, (per_page, offset))
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    connection.close()
    return jsonify({"message": "OK", "datas": results}), 200

# @barang_dlm_ruangan_endpoints.route('/read', methods=['GET'])
# def read():
#     try:
#         # Ambil parameter page dan search dari query string
#         page = int(request.args.get('page', 1))
#         search = request.args.get('search', '')
#         idRuangan = int(request.args.get('id_ruangan', ))
#         per_page = 5  # Tetapkan jumlah item per halaman

#         # Hitung offset
#         offset = (page - 1) * per_page

#         connection = get_connection()
#         cursor = connection.cursor(dictionary=True)

#         if search:
#             # Jika ada parameter search, tambahkan kondisi WHERE dengan LIKE
#             search_param = f"%{search}%"
#             count_query = """
#                 SELECT COUNT(*) AS total 
#                 FROM barang_dlm_ruangan 
#                 WHERE nama_barang_dlm_ruangan LIKE %s
#             """
#             cursor.execute(count_query, (search_param,))
#             total_items = cursor.fetchone()['total']

#             query = """
#                 SELECT *
#                 FROM barang_dlm_ruangan
#                 WHERE nama_barang_dlm_ruangan LIKE %s
#                 LIMIT %s OFFSET %s
#             """
#             cursor.execute(query, (search_param, per_page, offset))
#         else:
#             # Jika tidak ada parameter search, ambil semua data tanpa kondisi WHERE
#             count_query = "SELECT COUNT(*) AS total FROM barang_dlm_ruangan"
#             cursor.execute(count_query)
#             total_items = cursor.fetchone()['total']

#             query = """
#                 SELECT *
#                 FROM barang_dlm_ruangan
#                 WHERE id_ruangan = %s
#                 LIMIT %s OFFSET %s
#             """
#             cursor.execute(query, (idRuangan, per_page, offset))

#         results = cursor.fetchall()

#         cursor.close()
#         connection.close()

#         total_pages = (total_items + per_page - 1) // per_page  # Hitung total halaman

#         return jsonify({
#             "message": "OK",
#             "datas": results,
#             "pagination": {
#                 "total_items": total_items,
#                 "total_pages": total_pages,
#                 "current_page": page,
#                 "per_page": per_page
#             }
#         }), 200
#     except Exception as e:
#         return jsonify({
#             "message": "Failed to fetch data",
#             "error": str(e)
#         }), 500

@barang_dlm_ruangan_endpoints.route('/read', defaults={'idRuangan': None})
@barang_dlm_ruangan_endpoints.route('/read/<idRuangan>', methods=['GET'])
def read(idRuangan):
    try:
        # Ambil parameter page dan search dari query string
        page = int(request.args.get('page', 1))
        search = request.args.get('search', '')
        per_page = 5  # Tetapkan jumlah item per halaman

        # Hitung offset
        offset = (page - 1) * per_page

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        if search:
            # Jika ada parameter search, tambahkan kondisi WHERE dengan LIKE
            search_param = f"%{search}%"
            if idRuangan:
                count_query = """
                    SELECT COUNT(*) AS total 
                    FROM barang_dlm_ruangan 
                    WHERE nama_barang_dlm_ruangan LIKE %s AND id_ruangan = %s
                """
                cursor.execute(count_query, (search_param, idRuangan))
            else:
                count_query = """
                    SELECT COUNT(*) AS total 
                    FROM barang_dlm_ruangan 
                    WHERE nama_barang_dlm_ruangan LIKE %s
                """
                cursor.execute(count_query, (search_param,))
            
            total_items = cursor.fetchone()['total']

            if idRuangan:
                query = """
                    SELECT *
                    FROM barang_dlm_ruangan
                    WHERE nama_barang_dlm_ruangan LIKE %s AND id_ruangan = %s
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (search_param, idRuangan, per_page, offset))
            else:
                query = """
                    SELECT *
                    FROM barang_dlm_ruangan
                    WHERE nama_barang_dlm_ruangan LIKE %s
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (search_param, per_page, offset))
        else:
            # Jika tidak ada parameter search, ambil semua data
            if idRuangan:
                count_query = "SELECT COUNT(*) AS total FROM barang_dlm_ruangan WHERE id_ruangan = %s"
                cursor.execute(count_query, (idRuangan,))
            else:
                count_query = "SELECT COUNT(*) AS total FROM barang_dlm_ruangan"
                cursor.execute(count_query)

            total_items = cursor.fetchone()['total']

            if idRuangan:
                query = """
                    SELECT *
                    FROM barang_dlm_ruangan
                    WHERE id_ruangan = %s
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (idRuangan, per_page, offset))
            else:
                query = """
                    SELECT *
                    FROM barang_dlm_ruangan
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (per_page, offset))

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        total_pages = (total_items + per_page - 1) // per_page  # Hitung total halaman

        return jsonify({
            "message": "OK",
            "datas": results,
            "pagination": {
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": page,
                "per_page": per_page
            }
        }), 200
    except Exception as e:
        return jsonify({
            "message": "Failed to fetch data",
            "error": str(e)
        }), 500


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


@barang_dlm_ruangan_endpoints.route('/readByUser/<id_pengguna>', methods=['GET'])
def readByUser(id_pengguna):
    """Routes for module get list of items in rooms owned by a user"""
    # Ambil parameter page dan search dari query string
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '')
    per_page = 5  # Tetapkan jumlah item per halaman

    # Hitung offset
    offset = (page - 1) * per_page

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if search:
        # Jika ada parameter search, tambahkan kondisi WHERE dengan LIKE
        search_param = f"%{search}%"
        count_query = """
            SELECT COUNT(*) AS total 
            FROM barang_dlm_ruangan bdr
            INNER JOIN ruangan r ON bdr.id_ruangan = r.id_ruangan 
            WHERE bdr.nama_barang_dlm_ruangan LIKE %s AND r.id_pengguna = %s
        """
        cursor.execute(count_query, (search_param, id_pengguna))
        total_items = cursor.fetchone()['total']
        
        query = """
            SELECT bdr.*
            FROM barang_dlm_ruangan bdr
            INNER JOIN ruangan r ON bdr.id_ruangan = r.id_ruangan
            WHERE bdr.nama_barang_dlm_ruangan LIKE %s AND r.id_pengguna = %s
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (search_param, id_pengguna, per_page, offset))
    else:
        # Jika tidak ada parameter search, ambil semua data
        count_query = """
            SELECT COUNT(*) AS total 
            FROM barang_dlm_ruangan bdr
            INNER JOIN ruangan r ON bdr.id_ruangan = r.id_ruangan
            WHERE r.id_pengguna = %s
        """
        cursor.execute(count_query, (id_pengguna,))
        total_items = cursor.fetchone()['total']
        
        query = """
            SELECT bdr.*
            FROM barang_dlm_ruangan bdr
            INNER JOIN ruangan r ON bdr.id_ruangan = r.id_ruangan
            WHERE r.id_pengguna = %s
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (id_pengguna, per_page, offset))

    results = cursor.fetchall()
    
    cursor.close()
    connection.close()

    total_pages = (total_items + per_page - 1) // per_page  # Hitung total halaman

    return jsonify({
        "message": "OK",
        "datas": results,
        "pagination": {
            "total_items": total_items,
            "total_pages": total_pages,
            "current_page": page,
            "per_page": per_page
        }
    }), 200


    # # Query to get items in rooms owned by the user
    # select_query = """
    # SELECT bdr.*
    # FROM barang_dlm_ruangan bdr
    # INNER JOIN ruangan r ON bdr.id_ruangan = r.id_ruangan
    # WHERE r.id_pengguna = %s
    # """
    # cursor.execute(select_query, (id_pengguna,))
    # results = cursor.fetchall()
    
    # cursor.close()  # Close the cursor after query execution
    # connection.close()
    
    # return jsonify({"message": "OK", "datas": results}), 200


@barang_dlm_ruangan_endpoints.route('/create', methods=['POST'])
def create():
    """Routes for module create a book"""
    id_ruangan = request.form['id_ruangan']
    nama_barang_dlm_ruangan = request.form['nama_barang_dlm_ruangan']
    desc_barang_dlm_ruangan = request.form['desc_barang_dlm_ruangan']
    qnty_barang_dlm_ruangan = request.form['qnty_barang_dlm_ruangan']
    category_barang_dlm_ruangan = request.form['category_barang_dlm_ruangan']

    uploaded_file = request.files['gambar_barang_dlm_ruangan']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        connection = get_connection()
        cursor = connection.cursor()
        insert_query = "INSERT INTO barang_dlm_ruangan (id_ruangan, nama_barang_dlm_ruangan, desc_barang_dlm_ruangan, qnty_barang_dlm_ruangan, category_barang_dlm_ruangan, gambar_barang_dlm_ruangan) VALUES (%s, %s, %s, %s, %s, %s)"
        request_insert = (id_ruangan, nama_barang_dlm_ruangan, desc_barang_dlm_ruangan, qnty_barang_dlm_ruangan, category_barang_dlm_ruangan, uploaded_file.filename)
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


@barang_dlm_ruangan_endpoints.route('/update/<id_barang_dlm_ruangan>', methods=['POST'])
def update(id_barang_dlm_ruangan):
    """Routes for module update a book"""
    nama_barang_dlm_ruangan = request.form['nama_barang_dlm_ruangan']
    desc_barang_dlm_ruangan = request.form['desc_barang_dlm_ruangan']
    qnty_barang_dlm_ruangan = request.form['qnty_barang_dlm_ruangan']
    category_barang_dlm_ruangan = request.form['category_barang_dlm_ruangan']

    uploaded_file = request.files['gambar_barang_dlm_ruangan']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        connection = get_connection()
        cursor = connection.cursor()

        update_query = "UPDATE barang_dlm_ruangan SET nama_barang_dlm_ruangan=%s, desc_barang_dlm_ruangan=%s, qnty_barang_dlm_ruangan=%s, category_barang_dlm_ruangan=%s, gambar_barang_dlm_ruangan=%s WHERE id_barang_dlm_ruangan=%s"
        update_request = (nama_barang_dlm_ruangan, desc_barang_dlm_ruangan, qnty_barang_dlm_ruangan, category_barang_dlm_ruangan, uploaded_file.filename, id_barang_dlm_ruangan)
        cursor.execute(update_query, update_request)
        connection.commit()
        cursor.close()
        data = {"message": "updated", "id_barang_dlm_ruangan": id_barang_dlm_ruangan}
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
