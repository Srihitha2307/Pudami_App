import re
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from pyairtable import Table

app = Flask(__name__)
app.secret_key = "pudami_2026_pro"

# --- Airtable Configuration ---
# Integrated your specific credentials
AIRTABLE_API_KEY = 'patDB4vtAQ5htk3cs.2b1800d03aa91b6e36ffd6c030afcae4960de68dd49143f91fef09208677b19a' 
BASE_ID = 'appcwboqULu5U8nl7' 
USER_TABLE_NAME = 'Pudami' 
table = Table(AIRTABLE_API_KEY, BASE_ID, USER_TABLE_NAME)

# --- Global Sensor Data ---
live_sensor_data = {
    'vol': 0, 'n': 0, 'p': 0, 'k': 0, 'ph': 0, 'temp': 0,
    'sunlight': '0 hrs', 'wind': '0 km/h'
}

def is_strong_password(pw):
    if len(pw) < 8: return False
    if not re.search(r"[A-Z]", pw): return False
    if not re.search(r"[a-z]", pw): return False
    if not re.search(r"\d", pw): return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw): return False
    return True

# 1. SPLASH ROUTE
@app.route('/')
def splash():
    return render_template('logo.html')

# 2. LOGIN PAGE ROUTE
@app.route('/login')
def index():
    return render_template('register.html')

# 3. SENSOR API (Hardware Bridge)
@app.route('/update_sensors', methods=['POST'])
def update_sensors():
    global live_sensor_data
    sensor_json = request.json
    live_sensor_data['vol'] = sensor_json.get('moisture', 0)
    live_sensor_data['n'] = sensor_json.get('n', 0)
    live_sensor_data['p'] = sensor_json.get('p', 0)
    live_sensor_data['k'] = sensor_json.get('k', 0)
    return jsonify({"status": "success"}), 200

# 4. LOGIN HANDLER
@app.route('/login_handler', methods=['POST'])
def login_handler():
    un = request.form.get('username')
    pw = request.form.get('password')
    try:
        user_record = table.first(formula=f"{{Username}} = '{un}'")
        if user_record and user_record['fields'].get('Password') == pw:
            session['user_name'] = user_record['fields'].get('Name')
            session['crop'] = 'Paddy'
            session['soil'] = 'Alluvial'
            return redirect(url_for('dashboard_view', section='water'))
        else:
            flash("Invalid credentials.")
    except Exception as e:
        flash(f"Login Error: {str(e)}")
    return redirect(url_for('index'))

# 5. DYNAMIC DASHBOARD (Accessing 28 Tables)
@app.route('/dashboard/<section>')
def dashboard_view(section):
    crop = request.args.get('crop', session.get('crop', 'Paddy'))
    soil = request.args.get('soil', session.get('soil', 'Alluvial'))
    session['crop'], session['soil'] = crop, soil

    target_val = 0
    insight = "Select a category."

    try:
        if section == 'water':
            t_water = Table(AIRTABLE_API_KEY, BASE_ID, 'Indian Crop Water Footprint Data')
            spec = t_water.first(formula=f"{{Crop Name}} = '{crop}'")
            target_val = spec['fields'].get('Target_Moisture', 40) if spec else 40
            insight = f"Target for {crop} is {target_val}%. Current: {live_sensor_data['vol']}%."

        elif section == 'npk':
            # Dynamic lookup: e.g., "Nitrogen for sugarcane"
            t_n_name = f"Nitrogen for {crop.lower()}"
            t_n = Table(AIRTABLE_API_KEY, BASE_ID, t_n_name)
            records = t_n.all()
            if records:
                target_val = records[0]['fields'].get('Target', 20)
                insight = f"Analyzing {crop} Nitrogen needs in {soil} soil."
            else:
                insight = f"No data found in table: {t_n_name}"
                
        elif section == 'pests':
            t_pest = Table(AIRTABLE_API_KEY, BASE_ID, 'Pest and Disease Details')
            pests = t_pest.all(formula=f"{{Affected_Crop}} = '{crop}'")
            insight = f"Found {len(pests)} recorded threats for {crop}."

    except Exception as e:
        insight = f"Data sync error: {str(e)}"

    return render_template('dashboard.html', 
                           section=section, crop=crop, soil=soil,
                           data=live_sensor_data, target=target_val, 
                           insight=insight, user_name=session.get('user_name'))

# 6. REGISTER HANDLER
@app.route('/register_handler', methods=['POST'])
def register_handler():
    data = request.form
    un = data.get('reg_username')
    pw = data.get('reg_password')
    name = data.get('name')
    
    if pw != data.get('confirm_password'):
        flash("Passwords do not match.")
    elif not is_strong_password(pw):
        flash("Weak Password: Need 8+ chars, Caps, and Special Symbol.")
    else:
        try:
            table.create({"Username": un, "Password": pw, "Name": name})
            flash("Registration successful!")
        except:
            flash("Database error.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    # host='0.0.0.0' allows external devices like ESP32 to connect
    app.run(host='0.0.0.0', port=5000, debug=True)
