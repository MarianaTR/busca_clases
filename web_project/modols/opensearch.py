from opensearchpy import OpenSearch
import requests


host = 'http://34.222.58.202'
port = 9200
#auth = ('admin', 'admin') # For testing only. Don't store credentials in code.
#ca_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

# Optional client certificates if you don't want to use HTTP basic authentication.
# client_cert_path = '/full/path/to/client.pem'
# client_key_path = '/full/path/to/client-key.pem'

# Create the client with SSL/TLS enabled, but hostname verification disabled.

client = OpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_compress = True, # enables gzip compression for request bodies
        #http_auth = auth,
        # client_cert = client_cert_path,
        # client_key = client_key_path,
        use_ssl = False,
        verify_certs = False,
        #ssl_assert_hostname = False,
        #ssl_show_warn = False,
        #ca_certs = ca_certs_path
    )




index_name="iaps-index"

def search_query(q):

    # Search for the document.

    query = {
        "size": 5,
        "query": {
            "multi_match": {
                "query" : q,
                "fields": ["name","description","modalidad"]
            }
        }
    }

    response = client.search(
        body = query,
        index = index_name
    )
    #print('\nSearch results:')
    #print(response)

    return response

def search():
    # Search for the document.
    """
    query = {
        "query": {
        }
    }

    response = client.search(
        body=query,
        index=index_name
    )
    #print('\nSearch results:')
    #print(response)
"""
    response = requests.get('http://34.222.58.202:9200/iaps-index/_search')
    response = response.json()
    return response


def add_document(user_id,clase):

    # Add a document to the index.
    document = {
        'name': clase.name,
        'user_id': user_id,
        'description': clase.description,
        'duracion': clase.duracion,
        'precio' : clase.precio,
        'modalidad': clase.modalidad
    }

    response = client.index(
        index=index_name,
        body=document,
        refresh=True
    )

    #print('\nAdding document:')
    #print(response)

def delete_all():
    # Delete the document.
    response = client.delete(
        index=index_name,
        id='lCOW84MBB2WVqVtDxosX'
    )

    #print('\nDeleting document:')
    #print(response)