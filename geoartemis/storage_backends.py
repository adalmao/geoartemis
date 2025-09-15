from storages.backends.s3boto import S3BotoStorage

class MediaStorage(S3BotoStorage):
    location = 'media'
    file_overwrite = False
