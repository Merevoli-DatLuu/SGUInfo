from flask import Flask, render_template, request, jsonify
import sys

sys.path.append("..")
from sguinfo import sguinfo

app = Flask(__name__)

@app.route("/api/v1/students", methods=['GET'])
def get_student_list():
    sgu = sguinfo()
    if "from_id" in request.args and "to_id" in request.args and "id_list" not in request.args:
        from_id = request.args['from_id']
        to_id = request.args['to_id']
        if sgu.validate_range_mssv(from_id, to_id):
            data = []
            for d in sgu.find_range_info(from_id, to_id):
                data.append(sgu.change_to_eng_info(d))
            return jsonify(data)
        else:
            return jsonify({})
    elif "from_id" not in request.args and "to_id" not in request.args and "id_list" in request.args:
        list_id = request.args['id_list'].split(",")
        data = []
        for id in list_id:
            if sgu.validate_mssv(id):
                data.append(sgu.change_to_eng_info(sgu.find_info(id)))
        return jsonify(data)

    else:
        return jsonify({})


@app.route("/api/v1/students/<id>", methods = ['GET'])
def get_a_student(id):
    sgu = sguinfo()
    if sgu.validate_mssv(id):
        return jsonify(sgu.change_to_eng_info(sgu.find_info(id)))
    else:
        return jsonify({})

@app.route("/api/v1/students/<id>/<param>", methods = ['GET'])
def get_a_student_with_param(id, param):
    sgu = sguinfo()
    if sgu.validate_mssv(id):
        data = sgu.change_to_eng_info(sgu.find_info(id))
        if param in data.keys():
            return jsonify(data[param])
        else:
            return jsonify({})
    else:
        return jsonify({})

@app.route("/test")
def tessst():
    return request.args


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.config['JSON_SORT_KEYS'] = False
    app.run(debug = True)