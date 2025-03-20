import boto3
from imbox import Imbox
from urllib.parse import unquote
import os
import sys
import time

def get_timestamp():
    """生成统一时间戳格式"""
    return f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]"

def check_env_variable(var_name, error_msg):
    """环境变量校验函数"""
    value = os.getenv(var_name)
    if not value:
        print(f"{get_timestamp()} 错误：{error_msg}")
        sys.exit(1)
    return value

def main():
    # 环境变量校验
    r2_access_key_id = check_env_variable('access_key_id', "环境变量 access_key_id 未设置")
    r2_secret_access_key = check_env_variable('secret_access_key', "环境变量 secret_access_key 未设置")
    r2_endpoint_url = check_env_variable('endpoint_url', "环境变量 endpoint_url 未设置")
    r2_bucket_name = check_env_variable('bucket_name', "环境变量 bucket_name 未设置")
    mail_username = check_env_variable('username', "环境变量 username 未设置")
    mail_password = check_env_variable('password', "环境变量 password 未设置")

    # 创建客户端
    s3_client = boto3.client(
        's3',
        aws_access_key_id=r2_access_key_id,
        aws_secret_access_key=r2_secret_access_key,
        endpoint_url=r2_endpoint_url
    )

    print(f"{get_timestamp()} 开始执行程序")

    try:
        with Imbox('imap.gmail.com',
                   username=mail_username,
                   password=mail_password,
                   ssl=True) as imbox:
            filtered_messages = imbox.messages(subject='Z-Library')
            print(f"{get_timestamp()} 找到 {len(filtered_messages)} 封目标邮件")

            for uid, message in filtered_messages:
                print(f"{get_timestamp()} 正在处理邮件ID: {uid}，主题: {message.subject}")

                for attachment in message.attachments:
                    filename = attachment['filename']
                    if filename.startswith('utf-8'):
                        filename = unquote(filename[7:])
                    print(f"{get_timestamp()} 检测到附件: {filename}")

                    file_content = attachment['content'].read()
                    s3_client.put_object(
                        Bucket=r2_bucket_name,
                        Key=f"book/{filename}",
                        Body=file_content
                    )
                    print(f"{get_timestamp()} 附件已上传至 R2 存储桶: {r2_bucket_name}/book/{filename}")

                    imbox.delete(uid)
                    print(f"{get_timestamp()} 已删除邮件ID: {uid}")
    except Exception as e:
        print(f"{get_timestamp()} 程序异常：{type(e).__name__} - {str(e)}")
    finally:
        print(f"{get_timestamp()} 程序执行完毕")

if __name__ == "__main__":
    main()
