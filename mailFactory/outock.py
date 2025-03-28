
import os 
import httpx 
import mimetypes
import base64
from ms_token import get_access_token , MS_GRAPH_ENDPOINT
from pathlib import Path

def create_attachment(file_path: Path):
    """Crea un adjunto correctamente codificado"""
    with open(file_path, 'rb') as f:
        content = f.read()
    return {
        '@odata.type': '#microsoft.graph.fileAttachment',
        'name': file_path.name,
        'contentType': mimetypes.guess_type(file_path.name)[0] or 'application/octet-stream',
        'contentBytes': base64.b64encode(content).decode('utf-8')
    }


def get_mine_type(file_path):
    mine_type,_ = mimetypes.guess_type(file_path)
    return mine_type

def get_sub_folders(headers,folder_id):
    endpoint = f'{MS_GRAPH_ENDPOINT}/me/mailFolders/{folder_id}/childFolders'
    response = httpx.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json().get('value',[])

def get_messages(headers,folder_id=None ,fields ='*' , top = 5 , order_by = 'receivedDateTime',order_by_desc=True,max_results=5):
    
    if folder_id is None:
        endpoint = f'{MS_GRAPH_ENDPOINT}/me/messages'
    else:
        endpoint = f'{MS_GRAPH_ENDPOINT}/me/mailFolders/{folder_id}/messages'
    params = {
        '$select': fields,
        '$top': min(top,max_results),
        '$orderby': f'{order_by} {"desc" if order_by_desc else "asc"}'
    }

    endpoint = f'{MS_GRAPH_ENDPOINT}/me/mailFolders/{folder_id}/messages'
    response = httpx.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json().get('value',[])