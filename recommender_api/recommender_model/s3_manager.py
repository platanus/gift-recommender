import boto3
import os


class S3(object):
    client = boto3.client('s3')

    @classmethod
    def ensure_file(cls, filepath: str) -> None:
        if os.path.exists(filepath):
            return
        dirname, filename = os.path.split(filepath)
        bucket_name = os.environ.get('BUCKET_NAME')
        cls.client.download_file(bucket_name, filename, filepath)


if __name__ == '__main__':
    # S3.ensure_file('embeddings-xs-model.vec')
    S3.ensure_file('recommender_api/recommender_model/embeddings-xs-model.vec')
