import importlib
import pickle
from concurrent.futures import ThreadPoolExecutor
from utils import Metadata, Database
from constants import *
import os


class DefaultModel:
    __WRITE_MODEL_OBJECT_OPTION = "wb"
    __READ_MODEL_OBJECT_OPTION = "rb"

    def __init__(self,
                 database_connector: Database,
                 model_name: str,
                 metadata_creator: Metadata = None,
                 module_path: str = None,
                 class_name: str = None):
        self.__metadata_creator = metadata_creator
        self.__thread_pool = ThreadPoolExecutor()
        self.__database_connector = database_connector

        self.model_name = model_name
        self.module_path = module_path
        self.class_name = class_name

        self.__metadata_creator.create_file(model_name, module_path,
                                            class_name)

    def create(self,
               description: str,
               class_parameters: dict) -> None:

        self.__thread_pool.submit(self.__pipeline,
                                  class_parameters,
                                  description)

    def update(self,
               description: str,
               class_parameters: dict) -> None:
        self.__metadata_creator.update_finished_flag(self.model_name, False)

        self.__thread_pool.submit(self.__pipeline,
                                  class_parameters,
                                  description)

    def delete(self):

        self.__thread_pool.submit(self.__database_connector.delete_file,
                                  self.model_name)
        self.__thread_pool.submit(os.remove, self.__get_binary_path())

    def __get_binary_path(self):
        return os.environ[MODELS_VOLUME_PATH] + "/" + self.model_name

    def __pipeline(self,
                   class_parameters: dict, description: str) -> None:
        try:
            module = importlib.import_module(self.module_path)
            module_function = getattr(module, self.class_name)
            function_instance = module_function(**class_parameters)
            self.__save(function_instance)
            self.__metadata_creator.update_finished_flag(self.model_name,
                                                         flag=True)
        except Exception as exception:
            self.__metadata_creator.create_model_document(self.model_name,
                                                          description,
                                                          class_parameters,
                                                          str(exception))
            return

        self.__metadata_creator.create_model_document(self.model_name,
                                                      description,
                                                      class_parameters)

    def __save(self, model_instance: object) -> None:
        model_output = open(self.__get_binary_path(),
                            self.__WRITE_MODEL_OBJECT_OPTION)
        pickle.dump(model_instance, model_output)
        model_output.close()
