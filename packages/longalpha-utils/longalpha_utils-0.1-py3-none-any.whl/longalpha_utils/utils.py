
import pandas as pd
from minio import Minio
from io import BytesIO
from typing import List
def max_pandas_display(pd: pd, max_row: int = 100) -> None:
    """
    set pandas print format to print all
    Args:
        pd: pandas object

    Returns: None

    """
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", max_row)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)
    pd.set_option("display.expand_frame_repr", False)


class MinioParquet:
    def __init__(self, minio_url, minio_access_key, minio_secret_key):
        self.minio_client = Minio(
            endpoint=minio_url,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=False,
        )

    def put(
        self,
        dataframe: pd.DataFrame,
        bucket_name: str,
        object_name: str,
    ) -> None:
        """

        Args:
            dataframe: a pandas dataframe
            bucket_name: Minio bucket_name
            object_name: path + file_name

        Returns:

        """
        file = dataframe.to_parquet()
        self.minio_client.put_object(
            bucket_name,
            object_name,
            data=BytesIO(file),
            length=len(file),
        )

    def get(
        self,
        bucket_name: str,
        object_name: str,
    ) -> pd.DataFrame:
        """

        Args:
             bucket_name: Minio bucket_name
            object_name: path + file_name

        Returns: A pandas dataframe

        """
        file = self.minio_client.get_object(
            bucket_name,
            object_name,
        )
        res = pd.read_parquet(BytesIO(file.data))
        file.close()
        file.release_conn()
        return res

    def get_latest(self, bucket_name: str) -> pd.DataFrame:
        """
        get the latest file
        Args:
            bucket_name: bucket_name: Minio bucket_name

        Returns: A pandas dataframe

        """
        objects = [i for i in self.minio_client.list_objects(bucket_name)]
        time_obj = {obj.last_modified: obj for obj in objects}
        latest_time = max(time_obj.keys())
        latest_obj = time_obj[latest_time]
        return self.get(bucket_name=bucket_name, object_name=latest_obj.object_name)

    def list(self, bucket_name: str) -> List[str]:
        return [i.object_name for i in self.minio_client.list_objects(bucket_name)]
