import os

source_file = 'assets/path/js.js'

replacement_path = "{{ url_for('assets', path='assets/path/js.js') }}"

with open(source_file, 'r') as file:
    content = file.read()

modified_content = content.replace('assets/path/js.js', replacement_path)

with open(source_file, 'w') as file:
    file.write(modified_content)

print(f"Файл '{source_file}' успешно обновлен.")
