# Import required libraries
from rdflib import Graph
import json

def load_graph(input_file, format=None):
    # Parse the RDF file with rdflib
    g = Graph()
    g.parse(input_file, format=format)
    return g

# This function reads an RDF file and convert it into a JSON file
def rdf_to_json(input_file, format=None):
    # Parse the RDF file with rdflib
    g = load_graph(input_file, format=format)
    # Serialize the graph in JSON-LD format
    json_data = g.serialize(format='json-ld')
    
    print('json conversion done')
    return json_data

def save_json(json_data, output_file):
    with open(output_file, 'w', encoding="utf-8") as json_file:
        #json.dump(json_data, json_file)
        json_file.write(json_data)
    print('json saved as '+output_file)

def load_jsonfile(path):
    with open(path,'r', encoding='utf-8') as file:
        filejs = file.read()
    file.close()
    js = json.loads(filejs)
    return js

def json2df(path):
    imported_js = load_jsonfile(path)
    df = pd.DataFrame(imported_js)
    return df

def help():
    print('''
    path = r"C:\...\data\SBO_OWL."
    js = rdf_to_json(path+'owl', format='xml')
    save_json(js, path+'json')
    
    imported_js = load_jsonfile(path+'json')
    
    df = json2df(path+'json')
    ''')