import os

from dotenv import load_dotenv

from src.converts.loon import Loon
from src.converts.mihomo import Client, Router
from src.converts.share import ShareLoon, ShareMihomo
from src.utils.upload import Upload_To_R2

load_dotenv()


def main():
    # 检查必要的环境变量
    required_env_vars = [
        "R2_ENDPOINT_URL",
        "R2_ACCESS_KEY_ID",
        "R2_SECRET_ACCESS_KEY",
        "R2_BUCKET_NAME",
    ]

    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file")
        return

    # 配置文件转换器映射
    export_files = {
        "share_mihomo.yaml": ShareMihomo(
            input_file="config/base.yaml", output_file="export/share_mihomo.yaml"
        ),
        "share_loon.conf": ShareLoon(
            input_file="config/base.yaml", output_file="export/share_loon.conf"
        ),
        "router.yaml": Router(
            input_file="config/base.yaml", output_file="export/router.yaml"
        ),
        "config.yaml": Client(
            input_file="config/base.yaml", output_file="export/config.yaml"
        ),
        "loon.conf": Loon(
            input_file="config/base.yaml", output_file="export/loon.conf"
        ),
    }

    # 执行转换
    print("Starting configuration conversion...")
    for filename, converter in export_files.items():
        try:
            converter.convert()
            print(f"Successfully converted {filename}")
        except Exception as e:
            print(f"Error converting {filename}: {str(e)}")
            continue

    # 上传到 R2
    print("\nStarting upload to R2...")
    for filename, _ in export_files.items():
        local_path = f"export/{filename}"
        if os.path.exists(local_path):
            # 在文件名前加上 'sub/' 目录
            r2_path = f"sub/{filename}"
            Upload_To_R2(local_path, r2_path)
        else:
            print(f"Warning: File {local_path} does not exist")


if __name__ == "__main__":
    main()
