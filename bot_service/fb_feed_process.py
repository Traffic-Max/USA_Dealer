import csv

# Список словарей с данными об автомобилях
vehicles = [
    {
        'vehicle_id': '1',
        'title': 'Toyota Camry 2017',
        'description': 'Отличный автомобиль, немного б/у',
        'availability': 'в наличии',
        'condition': 'б/у',
        'price': '15000',
        'url': 'http://yoursite.com/car1',
        'make': 'Toyota',
        'model': 'Camry',
        'year': '2017',
        'image[0].url': 'http://yoursite.com/car1.jpg',
        'dealer_id': 'dealer1',
        'vin': '1HGCM82633A123456',
        'exterior_color': 'Черный',
        'interior_color': 'Бежевый',
        'transmission': 'Автомат',
        'body_style': 'Седан',
        'fuel_type': 'Бензин',
    },
    # Другие автомобили...
]

# Имена полей для csv-файла
fieldnames = vehicles[0].keys()

# Запись данных в csv-файл
with open('vehicles.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(vehicles)
