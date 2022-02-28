from flask import Flask, jsonify, abort, request
import pandas as pd
import io
app = Flask(__name__)


@app.route('/api/v1/bestProduct')
def getBestProduct():
    csv_file = request.files.get('csvFile', None)
    if not csv_file or csv_file.filename == '':
        return (jsonify({'success': False, 'error': 400,
                'message': 'Missing file'}), 400)
    fileStream = io.StringIO(csv_file.stream.read().decode('UTF8'),
                             newline=None)
    fileDataFrame = pd.read_csv(fileStream)
    if list(fileDataFrame.columns) != ['id', 'product_name',
                                       'customer_average_rating']:
        return (jsonify({'success': False, 'error': 400,
                'message': 'Incorrect columns'}), 400)
    fileDataFrame = fileDataFrame.sort_values('customer_average_rating',
                                              ascending=False)
    topProduct = fileDataFrame.head(1)
    return jsonify({'success': True,
                    'top_product':
                        topProduct.product_name.iloc[0],
                    'product_rating':
                        topProduct.customer_average_rating.iloc[0]})
