import boto3
import os
import io
from PIL import Image


class S3(object):
    client = boto3.client('s3')

    session = boto3.Session(aws_access_key_id=os.environ.get('AWS_RAILS_ACCESS_KEY_ID'),
                            aws_secret_access_key=os.environ.get('AWS_RAILS_SECRET_ACCESS_KEY'),
                            region_name=os.environ.get('AWS_RAILS_REGION'))
    rails_bucket = session.resource('s3').Bucket(os.environ.get('RAILS_BUCKET_NAME'))

    @classmethod
    def ensure_file(cls, filepath: str) -> None:
        if os.path.exists(filepath):
            return
        dirname, filename = os.path.split(filepath)
        bucket_name = os.environ.get('BUCKET_NAME')
        cls.client.download_file(bucket_name, filename, filepath)

    @classmethod
    def fetch_image(cls, image_key):
        with io.BytesIO() as file_stream:
            cls.rails_bucket.download_fileobj(image_key, file_stream)
            image = Image.open(file_stream).convert('RGB')
        return image


if __name__ == '__main__':
    # S3.ensure_file('embeddings-xs-model.vec')
    S3.ensure_file('recommender_api/recommender_model/embeddings-xs-model.vec')
    print(S3.fetch_image('zvg7WTKwtKxLH3eni1ZTwTiM'))
