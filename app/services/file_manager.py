import os
from werkzeug.utils import secure_filename
from flask import current_app
from typing import List, Dict
from datetime import datetime

class FileManager:
    def __init__(self):
        self.upload_folder = current_app.config['UPLOAD_FOLDER']
        self.max_content_length = current_app.config['MAX_CONTENT_LENGTH']

    def save_file(self, file, project_id: str = None) -> Dict:
        """
        Save an uploaded file
        
        Args:
            file: FileStorage object
            project_id: Optional project identifier for organization
            
        Returns:
            dict: File information including path and size
        """
        if not file:
            return {'error': 'No file provided'}

        filename = secure_filename(file.filename)
        
        # Create project directory if needed
        if project_id:
            save_path = os.path.join(self.upload_folder, project_id)
            os.makedirs(save_path, exist_ok=True)
        else:
            save_path = self.upload_folder

        file_path = os.path.join(save_path, filename)
        
        try:
            file.save(file_path)
            
            return {
                'success': True,
                'filename': filename,
                'path': file_path,
                'size': os.path.getsize(file_path)
            }
        except Exception as e:
            return {'error': str(e)}

    def list_files(self, project_id: str = None) -> List[Dict]:
        """
        List all files in the upload directory
        
        Args:
            project_id: Optional project identifier for filtering
            
        Returns:
            list: List of file information dictionaries
        """
        path = os.path.join(self.upload_folder, project_id) if project_id else self.upload_folder
        
        if not os.path.exists(path):
            return []

        files = []
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                stats = os.stat(file_path)
                files.append({
                    'filename': filename,
                    'path': file_path,
                    'size': stats.st_size,
                    'modified': datetime.fromtimestamp(stats.st_mtime).isoformat(),
                    'created': datetime.fromtimestamp(stats.st_ctime).isoformat()
                })
        return files

    def read_file(self, filename: str, project_id: str = None) -> Dict:
        """
        Read contents of a file
        
        Args:
            filename: Name of the file to read
            project_id: Optional project identifier
            
        Returns:
            dict: File contents and metadata
        """
        path = os.path.join(self.upload_folder, project_id) if project_id else self.upload_folder
        file_path = os.path.join(path, secure_filename(filename))
        
        if not os.path.exists(file_path):
            return {'error': 'File not found'}
            
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            stats = os.stat(file_path)
            return {
                'success': True,
                'content': content,
                'size': stats.st_size,
                'modified': datetime.fromtimestamp(stats.st_mtime).isoformat()
            }
        except Exception as e:
            return {'error': str(e)}

    def delete_file(self, filename: str, project_id: str = None) -> Dict:
        """
        Delete a file
        
        Args:
            filename: Name of the file to delete
            project_id: Optional project identifier
            
        Returns:
            dict: Operation result
        """
        path = os.path.join(self.upload_folder, project_id) if project_id else self.upload_folder
        file_path = os.path.join(path, secure_filename(filename))
        
        if not os.path.exists(file_path):
            return {'error': 'File not found'}
            
        try:
            os.remove(file_path)
            return {'success': True}
        except Exception as e:
            return {'error': str(e)}
