"""Routes for module books"""
import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data

barang_dlm_container_endpoints = Blueprint('barang_dlm_container', __name__)
UPLOAD_FOLDER = "img"

@barang_dlm_container_endpoints.route('/readTotalBarangContainer/<id_barang_dlm_container>', methods=['GET'])
def readLocationContianer(id_barang_dlm_container):
    """Routes for module get list books"""
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        select_query = "SELECT ruangan.nama_ruangan, container.nama_container FROM barang_dlm_container INNER JOIN container ON barang_dlm_container.id_container = container.id_container INNER JOIN ruangan ON ruangan.id_ruangan = container.id_ruangan WHERE barang_dlm_container.id_barang_dlm_container = %s"
        select_request = (id_barang_dlm_container,)
        cursor.execute(select_query, select_request)
        results = cursor.fetchall()
    finally:
        cursor.close()  # Close the cursor after query execution
        connection.close()
        return jsonify({"message": "OK", "datas": results}), 200

# @barang_dlm_container_endpoints.route('/read', methods=['GET'])
# def read():
#     """Routes for module get list books"""
#     connection = get_connection()
#     cursor = connection.cursor(dictionary=True)
#     select_query = "SELECT * FROM barang_dlm_container"
#     cursor.execute(select_query)
#     results = cursor.fetchall()
#     cursor.close()  # Close the cursor after query execution
#     connection.close()
#     return jsonify({"message": "OK", "datas": results}), 200

# @barang_dlm_container_endpoints.route('/readTotalBarang/<id_barang_dlm_ruangan>', methods=['GET'])
# def readLocation(id_barang_dlm_ruangan):
#     """Routes for module get list books"""
#     try:
#         connection = get_connection()
#         cursor = connection.cursor(dictionary=True)
#         select_query = "SELECT ruangan.nama_ruangan FROM barang_dlm_ruangan INNER JOIN ruangan ON barang_dlm_ruangan.id_ruangan = ruangan.id_ruangan  WHERE barang_dlm_ruangan.id_barang_dlm_ruangan = 31"
#         select_request = (id_barang_dlm_ruangan,)
#         cursor.execute(select_query, select_request)
#         results = cursor.fetchall()
#     finally:
#         cursor.close()  # Close the cursor after query execution
#         connection.close()
#         return jsonify({"message": "OK", "datas": results}), 200


@barang_dlm_container_endpoints.route('/readAll', methods=['GET'])
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
                 FROM barang_dlm_container
                 LIMIT %s OFFSET %s
             """
    cursor.execute(query, (per_page, offset))
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    connection.close()
    return jsonify({"message": "OK", "datas": results}), 200

@barang_dlm_container_endpoints.route('/readByUserContainer/<id_pengguna>', methods=['GET'])
def readByUserContainer(id_pengguna):
    """Routes for module to get list of items in containers owned by a user"""
    try:
        # Get page and search parameters from query string
        page = int(request.args.get('page', 1))
        search = request.args.get('search', '')
        per_page = 5  # Set number of items per page

        # Calculate offset
        offset = (page - 1) * per_page

        print(f"page: {page}, search: {search}, per_page: {per_page}, offset: {offset}")

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        if search:
            # If search parameter is present, add WHERE condition with LIKE
            search_param = f"%{search}%"
            count_query = """
                SELECT COUNT(*) AS total 
                FROM barang_dlm_container bdc
                INNER JOIN container c ON bdc.id_container = c.id_container
                INNER JOIN ruangan r ON c.id_ruangan = r.id_ruangan
                INNER JOIN pengguna p ON r.id_pengguna = p.id_pengguna
                WHERE bdc.nama_barang_dlm_container LIKE %s AND p.id_pengguna = %s
            """
            print(f"count_query: {count_query}")
            cursor.execute(count_query, (search_param, id_pengguna))
            total_items = cursor.fetchone()['total']
            print(f"total_items with search: {total_items}")
            
            query = """
                SELECT bdc.*
                FROM barang_dlm_container bdc
                INNER JOIN container c ON bdc.id_container = c.id_container
                INNER JOIN ruangan r ON c.id_ruangan = r.id_ruangan
                INNER JOIN pengguna p ON r.id_pengguna = p.id_pengguna
                WHERE bdc.nama_barang_dlm_container LIKE %s AND p.id_pengguna = %s
                LIMIT %s OFFSET %s
            """
            print(f"query with search: {query}")
            cursor.execute(query, (search_param, id_pengguna, per_page, offset))
        else:
            # If no search parameter, fetch all data
            count_query = """
                SELECT COUNT(*) AS total 
                FROM barang_dlm_container bdc
                INNER JOIN container c ON bdc.id_container = c.id_container
                INNER JOIN ruangan r ON c.id_ruangan = r.id_ruangan
                INNER JOIN pengguna p ON r.id_pengguna = p.id_pengguna
                WHERE p.id_pengguna = %s
            """
            print(f"count_query: {count_query}")
            cursor.execute(count_query, (id_pengguna,))
            total_items = cursor.fetchone()['total']
            print(f"total_items without search: {total_items}")
            
            query = """
                SELECT bdc.*
                FROM barang_dlm_container bdc
                INNER JOIN container c ON bdc.id_container = c.id_container
                INNER JOIN ruangan r ON c.id_ruangan = r.id_ruangan
                INNER JOIN pengguna p ON r.id_pengguna = p.id_pengguna
                WHERE p.id_pengguna = %s
                LIMIT %s OFFSET %s
            """
            print(f"query without search: {query}")
            cursor.execute(query, (id_pengguna, per_page, offset))

        results = cursor.fetchall()
        print(f"results: {results}")
        
        cursor.close()
        connection.close()

        total_pages = (total_items + per_page - 1) // per_page  # Calculate total pages
        print(f"total_pages: {total_pages}")

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
        import traceback
        traceback.print_exc()
        return jsonify({
            "message": "Failed to fetch data",
            "error": str(e)
        }), 500




@barang_dlm_container_endpoints.route('/read', defaults={'id_container': None})
@barang_dlm_container_endpoints.route('/read/<id_container>', methods=['GET'])
def read(id_container):
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
            if id_container:
                count_query = """
                    SELECT COUNT(*) AS total 
                    FROM barang_dlm_container
                    WHERE nama_barang_dlm_container LIKE %s AND id_container = %s
                """
                cursor.execute(count_query, (search_param, id_container))
            else:
                count_query = """
                    SELECT COUNT(*) AS total 
                    FROM barang_dlm_container
                    WHERE nama_barang_dlm_container LIKE %s
                """
                cursor.execute(count_query, (search_param,))
            
            total_items = cursor.fetchone()['total']

            if id_container:
                query = """
                    SELECT *
                    FROM barang_dlm_container
                    WHERE nama_barang_dlm_container LIKE %s AND id_container = %s
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (search_param, id_container, per_page, offset))
            else:
                query = """
                    SELECT *
                    FROM barang_dlm_container
                    WHERE nama_barang_dlm_container LIKE %s
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (search_param, per_page, offset))
        else:
            # Jika tidak ada parameter search, ambil semua data
            if id_container:
                count_query = "SELECT COUNT(*) AS total FROM barang_dlm_container WHERE id_container = %s"
                cursor.execute(count_query, (id_container,))
            else:
                count_query = "SELECT COUNT(*) AS total FROM barang_dlm_container"
                cursor.execute(count_query)

            total_items = cursor.fetchone()['total']

            if id_container:
                query = """
                    SELECT *
                    FROM barang_dlm_container
                    WHERE id_container = %s
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (id_container, per_page, offset))
            else:
                query = """
                    SELECT *
                    FROM barang_dlm_container
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


# @barang_dlm_container_endpoints.route('/read/<id_container>', methods=['GET'])
# def readid(id_container):
#     """Routes for module get list books"""
#     connection = get_connection()
#     cursor = connection.cursor(dictionary=True)
#     select_query = "SELECT * FROM barang_dlm_container WHERE id_container=%s"
#     cursor.execute(select_query, (id_container,))
#     results = cursor.fetchall()
#     cursor.close()  # Close the cursor after query execution
#     connection.close()
#     return jsonify({"message": "OK", "datas": results}), 200


@barang_dlm_container_endpoints.route('/create', methods=['POST'])
def create():
    """Routes for module create a book"""
    id_container = request.form['id_container']
    nama_barang_dlm_container = request.form['nama_barang_dlm_container']
    desc_barang_dlm_container = request.form['desc_barang_dlm_container']
    qnty_barang_dlm_container = request.form['qnty_barang_dlm_container']
    category_barang_dlm_container = request.form['category_barang_dlm_container']

    uploaded_file = request.files['gambar_barang_dlm_container']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        connection = get_connection()
        cursor = connection.cursor()
        insert_query = "INSERT INTO barang_dlm_container (id_container, nama_barang_dlm_container, desc_barang_dlm_container, qnty_barang_dlm_container, gambar_barang_dlm_container, category_barang_dlm_container) VALUES (%s, %s, %s, %s, %s, %s)"
        request_insert = (id_container, nama_barang_dlm_container, desc_barang_dlm_container, qnty_barang_dlm_container, uploaded_file.filename, category_barang_dlm_container)
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


@barang_dlm_container_endpoints.route('/update/<id_barang_dlm_container>', methods=['POST'])
def update(id_barang_dlm_container):
    """Routes for module update a book"""
    nama_barang_dlm_container = request.form['nama_barang_dlm_container']
    desc_barang_dlm_container = request.form['desc_barang_dlm_container']
    qnty_barang_dlm_container = request.form['qnty_barang_dlm_container']
    category_barang_dlm_container = request.form['category_barang_dlm_container']

    uploaded_file = request.files['gambar_barang_dlm_container']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        connection = get_connection()
        cursor = connection.cursor()

        update_query = "UPDATE barang_dlm_container SET nama_barang_dlm_container=%s, desc_barang_dlm_container=%s, qnty_barang_dlm_container=%s, gambar_barang_dlm_container=%s, category_barang_dlm_container=%s WHERE id_barang_dlm_container=%s"
        update_request = (nama_barang_dlm_container, desc_barang_dlm_container, qnty_barang_dlm_container, uploaded_file.filename, category_barang_dlm_container, id_barang_dlm_container)
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