import os
import re
from collections import defaultdict

def find_external_references(po_folder_path, root_folder_path):
    po_files = get_files_in_folder(po_folder_path, '.cs')
    all_files = get_files_in_folder(root_folder_path, '.cs')

    external_references = []

    component_dependencies = defaultdict(set)

    for po_file in po_files:
        po_class = get_class_name(po_file)
        with open(po_file, 'r') as file:
            content = file.read()
            references, dependencies = find_references(content, all_files)
            external_references += references
            component_dependencies[po_class].update(dependencies)

    print_external_references(external_references, component_dependencies)

def get_files_in_folder(folder_path, extension):
    files = []

    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith(extension):
                file_path = os.path.join(root, filename)
                files.append(file_path)

    return files

def get_class_name(file_path):
    file_name = os.path.basename(file_path)
    class_name = os.path.splitext(file_name)[0]
    return class_name

def find_references(content, all_files):
    references = []
    dependencies = set()

    for file in all_files:
        with open(file, 'r') as f:
            file_content = f.read()
            matches = re.findall(r'\b(?<!\.)(?!\d)\w+\b', file_content)

            for match in matches:
                if match in content:
                    reference = {
                        'component_name': match,
                        'component_file': os.path.basename(file),
                        'component_file_path': file,
                        'caller_file': os.path.basename(po_file),
                        'caller_type': get_component_type(file_content, match)
                    }
                    references.append(reference)
                    if file != po_file:
                        dependencies.add(match)

    return references, dependencies

def get_component_type(file_content, component_name):
    class_regex = fr'(?<![\w.])class\s+{component_name}\b'
    interface_regex = fr'(?<![\w.])interface\s+{component_name}\b'
    enum_regex = fr'(?<![\w.])enum\s+{component_name}\b'
    attribute_regex = fr'(?<![\w.])\[.*{component_name}\b.*\]'
    method_regex = fr'(?<![\w.])\w+\s+{component_name}\s*\('

    if re.search(class_regex, file_content):
        return 'class_definition'
    elif re.search(interface_regex, file_content):
        return 'interface'
    elif re.search(enum_regex, file_content):
        return 'enum'
    elif re.search(attribute_regex, file_content):
        return 'attribute'
    elif re.search(method_regex, file_content):
        return 'method'
    else:
        return 'other'

def print_external_references(external_references, component_dependencies):
    for reference in external_references:
        component_name = reference['component_name']
        component_file = reference['component_file']
        component_file_path = reference['component_file_path']
        caller_file = reference['caller_file']
        caller_type = reference['caller_type']
        cbo = len(component_dependencies[component_name])

        print(f"Component: {component_name}")
        print(f"Component File: {component_file}")
        print(f"Component File Path: {component_file_path}")
        print(f"Caller File: {caller_file}")
        print(f"Caller Type: {caller_type}")
        print(f"CBO: {cbo}")
       
