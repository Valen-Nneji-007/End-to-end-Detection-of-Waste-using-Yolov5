import os,sys
import shutil
from wasteDetection.logger import logging
from wasteDetection.exception import AppException
from wasteDetection.entity.config_entity import DataValidationConfig
from wasteDetection.entity.artifacts_entity import (DataIngestionArtifact,
                                                 DataValidationArtifact)






class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config

        except Exception as e:
            raise AppException(e, sys) 
        


    
    def validate_all_files_exist(self) -> bool:
        try:
            validation_status = True

            feature_store_path = self.data_ingestion_artifact.feature_store_path
            required_file_list = self.data_validation_config.required_file_list

            logging.info(
                f"Validating files in: {feature_store_path}"
            )

            all_files = os.listdir(feature_store_path)

            for required_file in required_file_list:
                if required_file not in all_files:
                    logging.error(
                        f"Required file/folder is missing: {required_file}"
                    )
                    validation_status = False

                os.makedirs(
                    self.data_validation_config.data_validation_dir,
                    exist_ok=True
                    )

                with open(
                    self.data_validation_config.valid_status_file_dir,
                        "w"
                    ) as f:
                    f.write(f"Validation status: {validation_status}")

                    logging.info(
                        f"Data validation status: {validation_status}"
                            )

                return validation_status

        except Exception as e:
            raise AppException(e, sys)
        


    
    def initiate_data_validation(self) -> DataValidationArtifact: 
        logging.info("Entered initiate_data_validation method of DataValidation class")
        try:
            status = self.validate_all_files_exist()
            data_validation_artifact = DataValidationArtifact(
                validation_status=status)

            logging.info("Exited initiate_data_validation method of DataValidation class")
            logging.info(f"Data validation artifact: {data_validation_artifact}")

            if status:
                shutil.copy(self.data_ingestion_artifact.data_zip_file_path, os.getcwd())

            return data_validation_artifact

        except Exception as e:
            raise AppException(e, sys)
        