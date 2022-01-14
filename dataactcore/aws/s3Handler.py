import logging
from datetime import datetime
import boto3

from botocore.exceptions import ClientError

from dataactcore.config import CONFIG_BROKER


logger = logging.getLogger(__name__)


class S3Handler:
    """ This class acts a wrapper for S3 URL Signing

        Attributes:
            bucketRoute: The name of the bucket to be used

        Constants:
            BASE_URL: The start of the urls generated by S3Handler
            ENABLE_S3: whether to use S3 or not
            URL_LIFETIME: Length of time before s3 URLs expire in seconds
    """
    BASE_URL = "https://files-broker-nonprod.usaspending.gov"
    ENABLE_S3 = True
    URL_LIFETIME = 60

    def __init__(self, name=None):
        """ Creates the object for signing URLS

            Args:
                name: Name of the S3 bucket
        """
        if name is None:
            self.bucketRoute = CONFIG_BROKER['aws_bucket']
        else:
            self.bucketRoute = name

    def _sign_url(self, path, file_name, bucket_route, url_mapping=None, method="put_object"):
        """ Creates the object for signing URLS

            Args:
                path: Path to folder
                file_name: Name of file to get signed URL for.
                bucket_route: Name of the bucket being accessed
                url_mapping: The mapping to replace the S3 URL before giving it to the user
                method: method to create signed url for

            Returns:
                A string containing the signed URL to the file
        """
        if S3Handler.ENABLE_S3:
            s3 = boto3.client('s3', region_name=CONFIG_BROKER['aws_region'])
            s3_params = {'Bucket': bucket_route,
                         'Key': (path + "/" + file_name) if path else file_name}
            presigned_url = s3.generate_presigned_url(method, s3_params, ExpiresIn=S3Handler.URL_LIFETIME)
            if url_mapping:
                presigned_url = presigned_url.replace(presigned_url.split('/')[2],
                                                      CONFIG_BROKER['proxy_url'] + '/' + url_mapping[1])
            return presigned_url
        return S3Handler.BASE_URL + "/" + self.bucketRoute + "/" + path + "/" + file_name

    def get_signed_url(self, path, file_name, bucket_route=None, url_mapping=None, method="put_object"):
        """ Signs a URL

            Args:
                path: Path to folder
                file_name: Name of file to get signed URL for.
                bucket_route: Name of the bucket being accessed
                url_mapping: The mapping to replace the S3 URL before giving it to the user
                method: method to create signed url for

            Returns:
                A string containing the signed URL to the file
        """
        bucket_route = self.bucketRoute if bucket_route is None else bucket_route

        if method == "put_object":
            file_name = S3Handler.get_timestamped_filename(file_name)
        return self._sign_url(path, file_name, bucket_route, url_mapping, method)

    @staticmethod
    def get_timestamped_filename(filename):
        """ Gets a Timestamped file name to prevent conflicts on S3 Uploading

            Args:
                filename: name of the file to timestamp

            Returns:
                The filename with a timestamp prepended
        """
        seconds = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())
        return str(seconds) + "_" + filename

    @staticmethod
    def get_file_size(filename):
        """ Get the size of the specified file from the submission bucket

            Args:
                filename: Name of the file in the submission bucket to check the size of

            Returns:
                File size in number of bytes for specified filename, or 0 if file doesn't exist
        """
        s3_reso = boto3.resource('s3', region_name=CONFIG_BROKER['aws_region'])
        obj_info = s3_reso.ObjectSummary(CONFIG_BROKER['aws_bucket'], filename)
        try:
            return obj_info.size
        except ClientError:
            logger.warning("File doesn't exist on AWS: %s", filename)
            return 0

    @staticmethod
    def copy_file(original_bucket, new_bucket, original_path, new_path):
        """ Copies a file from one bucket to another.

            Args:
                original_bucket: Name of the bucket to copy from
                new_bucket: Name of the bucket to copy to
                original_path: Path and filename of the original file
                new_path: Path and filename for the copied file
        """
        s3 = boto3.resource('s3', region_name=CONFIG_BROKER['aws_region'])
        source_info = {
            'Bucket': original_bucket,
            'Key': original_path
        }
        s3.meta.client.copy(source_info, new_bucket, new_path)
