config = dict()

with open('../resources/config.cfg') as file:
    for line in file:
        line = line.replace('\n', '')
        elements = line.split('=')
        config[elements[0]] = elements[1]
with open('../resources/config.cfg', 'w') as file:
    if config['erase'] == '1':
        file.write('DELETED')
