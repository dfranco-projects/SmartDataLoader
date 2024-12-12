import os

# Centralized Path Manager
class PathManager:
    '''
    A class to manage the central paths for the project. 
    Users can customize the folder structure by modifying this class as needed.
    '''

    def __init__(self, root_path: str = None, data_folder: str = 'data', 
                extracted_data_folder: str = 'extracted_data', metadata_folder: str = 'metadata') -> None:
        '''
        Initializes the PathManager with the given folder structure.

        Args:
            root_path (str, optional): Path to the project root folder. Defaults to None, 
                                        which means the project directory is used (assuming 
                                        the `SmartDataLoader` folder is placed inside the project).
            data_folder (str, optional): Name of the data folder. Defaults to 'data'.
            extracted_data_folder (str, optional): Name of the extracted data folder. Defaults to 'extracted_data'.
            metadata_folder (str, optional): Name of the metadata folder. Defaults to 'metadata'.
        '''
        self.root_path = root_path or os.path.abspath(os.path.join(os.getcwd(), '..', '..'))
        self.data_folder = os.path.join(self.root_path, data_folder)
        self.extracted_data_folder = os.path.join(self.root_path, extracted_data_folder)
        self.metadata_folder = os.path.join(self.root_path, metadata_folder)

    def get_project_root(self) -> str:
        return self.root_path

    def get_data_path(self) -> str:
        return self.data_folder

    def get_extracted_data_path(self) -> str:
        return self.extracted_data_folder

    def get_metadata_path(self) -> str:
        return self.metadata_folder
