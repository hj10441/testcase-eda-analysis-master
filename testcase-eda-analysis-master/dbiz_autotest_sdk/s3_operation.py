import os
from os import listdir
import boto3
from boto3.session import Session
import datetime
from loguru import logger


@logger.catch()
def init_s3(region_name, aws_access_key_id,aws_secret_access_key):
    """
    初始化S3连接
    """
    s3 = boto3.resource('s3', region_name=region_name, aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
    return s3

@logger.catch()
def upload_file_to_S3(s3,bucket_name,source_file,upload_key):
    """
    上传单个文件到S3指定位置
    :param bucket_name
    :param source_file: 本地文件路径
    :param upload_key: 上传到S3的文件位置
    """
    with open(source_file, 'rb') as f:
        try:
            s3.Bucket(bucket_name).put_object(Key=upload_key, Body=f)
            logger.info("{} upload done".format(source_file))
        except Exception as e:
            logger.error("upload {} error:{}".format(source_file, e))
            # print("upload {} error:{}".format(source_file, e))


@logger.catch()
def download_file_from_S3(s3,bucket_name,source_file,target_file):
    """
    下载单个文件
    :param bucket_name
    :param source_file
    :param target_file
    """
    s3.meta.client.download_file(bucket, source_file, target_file)

@logger.catch()
def upload_file_by_folder(s3,bucket_name,folder_path,init_upload_key):
    """
    上传文件夹下文件到S3
    :param folder_path: 本地文件夹路径
    :param init_upload_key: 本次上传的S3文件夹名称
    """
    allfilelist=os.listdir(folder_path)
    if len(allfilelist)== 0:
        logger.info("folder {} is empty!".format(folder_path))
    else:
        # 遍历该文件夹下的所有目录或者文件
        for file in allfilelist:
            filepath=os.path.join(folder_path,file)
            upload_key = init_upload_key
            # 如果是文件夹，递归调用函数
            if os.path.isdir(filepath):
                path = filepath.replace(folder_path, '')
                pathlist = path.split(os.sep)
                for f in pathlist[1:]:
                    upload_key =  upload_key + f + '/'
                upload_file_by_folder(s3,bucket_name,filepath,upload_key)
            # 如果不是文件夹，上传文件到S3
            elif os.path.isfile(filepath):
                upload_key = init_upload_key
                filename = os.path.basename(filepath)
                upload_key = upload_key + filename
                try:
                    upload_file_to_S3(s3,bucket_name,filepath,upload_key)
                except Exception as e:
                    logger.error("upload {} error:{}".format(filepath, e))
