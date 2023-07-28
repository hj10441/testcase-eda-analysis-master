from .s3_operation import *
import threading
from .storage import Storage

class s3Storage(Storage):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.s3 = init_s3()


    def __new__(cls, *args, **kwargs):
        if not hasattr(s3Storage, "_instance"):
            with s3Storage._instance_lock:
                if not hasattr(s3Storage, "_instance"):
                    s3Storage._instance = object.__new__(cls)  
        return s3Storage._instance

    def store(self,data_folder,report_id):
        return upload_all_file_to_s3(self.s3,data_folder,report_id)
