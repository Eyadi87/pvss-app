from flask import Flask, render_template, jsonify, request
import math

app = Flask(__name__)

def deg2rad(d): return d * math.pi / 180.0
def rad2deg(r): return r * 180.0 / math.pi

def solar_position(lat, lon, hour_decimal, doy=172):
    lat_r = deg2rad(lat)
    B = deg2rad((360.0 / 365.0) * (doy - 81))
    EoT = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
    TC = 4 * (lon - 15 * round(lon / 15)) + EoT
    LST = hour_decimal + TC / 60.0
    HRA = deg2rad(15.0 * (LST - 12.0))
    decl = deg2rad(23.45 * math.sin(deg2rad((360.0 / 365.0) * (doy - 81))))
    sin_alt = (math.sin(lat_r) * math.sin(decl) +
               math.cos(lat_r) * math.cos(decl) * math.cos(HRA))
    sin_alt = max(-1.0, min(1.0, sin_alt))
    altitude = rad2deg(math.asin(sin_alt))
    cos_az_den = math.cos(lat_r) * math.cos(math.asin(sin_alt))
    if abs(cos_az_den) < 1e-9:
        azimuth = 0.0
    else:
        cos_az_num = math.sin(decl) - math.sin(lat_r) * sin_alt
        cos_az = max(-1.0, min(1.0, cos_az_num / cos_az_den))
        azimuth = rad2deg(math.acos(cos_az))
        if math.sin(HRA) > 0:
            azimuth = 360.0 - azimuth
    return azimuth, altitude

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/solar', methods=['GET'])
def solar_api():
    lat = float(request.args.get('lat', 12.9716))
    lon = float(request.args.get('lon', 77.5946))
    hour = float(request.args.get('hour', 14.0))
    doy = int(request.args.get('doy', 172))
    az, alt = solar_position(lat, lon, hour, doy)
    glare_active = alt > 5.0
    h = int(hour)
    m = int((hour - h) * 60)
    return jsonify({
        'azimuth': round(az, 2),
        'altitude': round(alt, 2),
        'glare_active': glare_active,
        'time_str': f'{h:02d}:{m:02d}',
        'hour': hour,
        'lat': lat,
        'lon': lon
    })

@app.route('/api/trajectory', methods=['GET'])
def trajectory_api():
    lat = float(request.args.get('lat', 12.9716))
    lon = float(request.args.get('lon', 77.5946))
    doy = int(request.args.get('doy', 172))
    points = []
    for t in [x * 0.25 for x in range(4 * 5, 4 * 20)]:
        az, alt = solar_position(lat, lon, t, doy)
        points.append({'hour': t, 'azimuth': round(az, 2), 'altitude': round(alt, 2)})
    return jsonify(points)

if __name__ == '__main__':
    app.run(debug=True, port=5000)