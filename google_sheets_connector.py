from weight_scale_measurement import ScaleMeasurement
import pygsheets
import datetime 

def append_weight_measurement(measurement: ScaleMeasurement):
    SPREADSHEET_ID = '1JYkbkh0m-_AeFxiVQjdQYyWzGFs0KrLg3EGAlJUHNww'

    client = pygsheets.authorize(client_secret='google_api_secret.json')
    document = client.open_by_key(SPREADSHEET_ID)
    sheet = document.worksheet_by_title('Pi_Collected')
    
    row = [str(measurement.time), str(measurement.collection_time), measurement.weight, measurement.unit, measurement.stabilized]
    
    sheet.append_table(row)

if __name__ == "__main__":
   append_weight_measurement(ScaleMeasurement(100, 'kg', datetime.datetime.now(), False))
