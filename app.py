from flask import Flask, request, jsonify
import sqlite3
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def get_db_connection():
    try:
        conn = sqlite3.connect('zomato.db') 
        conn.row_factory = sqlite3.Row
        app.logger.debug("Database connection established")
        return conn
    except Exception as e:
        app.logger.error(f"Database connection error: {e}")
        return None

@app.route('/')
def home():
    return "Welcome to Zomato"

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    app.logger.debug(f"Fetching restaurant with ID: {id}")
    conn = get_db_connection()
    if conn is None:
        app.logger.error("Failed to establish database connection")
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        restaurant = conn.execute('SELECT * FROM restaurants WHERE "Restaurant ID" = ?', (id,)).fetchone()
        conn.close()
        if restaurant is None:
            app.logger.debug(f"Restaurant with ID: {id} not found")
            return jsonify({'error': 'Restaurant not found'}), 404
        app.logger.debug(f"Restaurant with ID: {id} found: {dict(restaurant)}")
        return jsonify(dict(restaurant))
    except sqlite3.Error as e:
        app.logger.error(f"SQLite error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    app.logger.debug("Fetching restaurants with pagination")
    conn = get_db_connection()
    if conn is None:
        app.logger.error("Failed to establish database connection")
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        offset = (page - 1) * per_page
        
        # Get total count for pagination
        total_count = conn.execute('SELECT COUNT(*) FROM restaurants').fetchone()[0]

        # Fetch current page restaurants
        restaurants = conn.execute('SELECT * FROM restaurants LIMIT ? OFFSET ?', (per_page, offset)).fetchall()
        conn.close()
        #http://127.0.0.1:5000/restaurants?page=1&per_page=5 for certain number of pages
        
        # Return data with total count
        return jsonify({
            'total_count': total_count,
            'restaurants': [dict(row) for row in restaurants]
        })
    except sqlite3.Error as e:
        app.logger.error(f"SQLite error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
        
@app.route('/restaurants/search', methods=['GET'])
def search_restaurants():
    app.logger.debug("Searching restaurants")
    conn = get_db_connection()
    if conn is None:
        app.logger.error("Failed to establish database connection")
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        query = request.args.get('query', '')
        restaurants = conn.execute('''
            SELECT * FROM restaurants
            WHERE "Restaurant Name" LIKE ? OR City LIKE ? OR Cuisines LIKE ?
            LIMIT 20
        ''', (f'%{query}%', f'%{query}%', f'%{query}%')).fetchall()
        conn.close()
        app.logger.debug(f"Restaurants found: {restaurants}")
        return jsonify([dict(row) for row in restaurants])
    except sqlite3.Error as e:
        app.logger.error(f"SQLite error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
