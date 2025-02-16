import os

import boto3
import requests
from botocore.config import Config


def purge_cache(file_url):
    """清除 Cloudflare CDN 缓存"""
    headers = {
        "Authorization": f"Bearer {os.getenv('CLOUDFLARE_API_TOKEN')}",
        "Content-Type": "application/json",
    }

    data = {"files": [file_url]}

    zone_id = os.getenv("CLOUDFLARE_ZONE_ID")
    response = requests.post(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache",
        headers=headers,
        json=data,
    )
    return response.json()


def Upload_To_R2(local_file_path, r2_object_name):
    """
    上传文件到 Cloudflare R2

    :param local_file_path: 本地文件路径
    :param r2_object_name: R2中的对象名称
    """
    # R2 配置
    r2 = boto3.client(
        service_name="s3",
        endpoint_url=os.getenv("R2_ENDPOINT_URL"),
        aws_access_key_id=os.getenv("R2_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("R2_SECRET_ACCESS_KEY"),
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )

    bucket_name = os.getenv("R2_BUCKET_NAME")

    try:
        r2.upload_file(
            local_file_path,
            bucket_name,
            r2_object_name,
            ExtraArgs={
                "CacheControl": "no-cache"  # 防止缓存
            },
        )

        try:
            # 上传成功后清除CDN缓存
            file_url = f"{os.getenv('R2_ENDPOINT_URL')}/{bucket_name}/{r2_object_name}"
            cache_result = purge_cache(file_url)
            print(f"Cache purge result: {cache_result}")
        except Exception as cache_error:
            # 如果清除缓存失败，只记录错误但不影响上传结果
            print(f"Warning: Cache purge failed: {str(cache_error)}")

        print(f"Successfully uploaded {local_file_path} to R2")

    except Exception as e:
        print(f"Error uploading {local_file_path} to R2: {str(e)}")
