import csv

data = [
    {'sec': 1, 'FPS': 22}
]

with open('data.csv', 'a', newline='') as csvfile:
    fieldnames = ['sec', 'FPS']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerows(data)
