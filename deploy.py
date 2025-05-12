import os
import sys
import anyio
import dagger
from pulumi import automation as auto
from pulumi_aws import s3


async def create_and_deploy_infrastructure():
    """使用 Dagger 和 Pulumi 创建和部署 AWS S3 存储桶"""

    # 定义 Pulumi 程序
    def pulumi_program():
        # 创建 S3 存储桶
        bucket = s3.Bucket("my-website-bucket",
            website={
                "index_document": "index.html",
            },
            tags={
                "Environment": "Dev",
                "ManagedBy": "Pulumi",
            }
        )
        return {
            "bucket_name": bucket.id,
            "website_url": bucket.website_endpoint,
        }

    # 配置 Pulumi 自动化 API
    stack_name = "dev"
    project_name = "dagger-pulumi-demo"
    
    # 创建或选择 Pulumi 栈
    stack = await auto.create_or_select_stack(
        stack_name=stack_name,
        project_name=project_name,
        program=pulumi_program,
    )
    
    # 设置 AWS 区域
    await stack.set_config("aws:region", auto.ConfigValue("us-west-2"))
    
    print("开始部署基础设施...")
    
    # 部署栈
    up_result = await stack.up()
    
    website_url = up_result.outputs["website_url"].value
    bucket_name = up_result.outputs["bucket_name"].value
    
    return bucket_name, website_url


async def dagger_pipeline(bucket_name):
    """使用 Dagger 构建和部署网站内容到 S3 桶"""
    
    config = dagger.Config(log_output=sys.stdout)
    
    # 初始化 Dagger 客户端
    async with dagger.Connection(config) as client:
        # 获取当前项目目录
        src = client.host().directory("./website")
        
        # 构建阶段：使用 Node 容器生成网站
        builder = (
            client.container()
            .from_("node:18-alpine")
            .with_directory("/src", src)
            .with_workdir("/src")
            .with_exec(["npm", "install"])
            .with_exec(["npm", "run", "build"])
        )
        
        # 获取构建后的文件
        build_dir = builder.directory("/src/build")
        
        # 部署阶段：使用 AWS CLI 部署到 S3
        await (
            client.container()
            .from_("amazon/aws-cli:latest")
            .with_directory("/website", build_dir)
            .with_env_variable("AWS_ACCESS_KEY_ID", os.environ.get("AWS_ACCESS_KEY_ID", ""))
            .with_env_variable("AWS_SECRET_ACCESS_KEY", os.environ.get("AWS_SECRET_ACCESS_KEY", ""))
            .with_env_variable("AWS_DEFAULT_REGION", os.environ.get("AWS_SECRET_ACCESS_KEY", ""))
            .with_exec([
                "s3", "sync", 
                "/website", 
                f"s3://{bucket_name}", 
                "--delete", 
                "--acl", "public-read"
            ])
            .stdout()
        )


async def main():
    """主函数，协调 Pulumi 和 Dagger 的工作流程"""
    
    # 步骤 1: 使用 Pulumi 创建基础设施
    print("正在使用 Pulumi 创建 AWS 基础设施...")
    bucket_name, website_url = await create_and_deploy_infrastructure()
    print(f"基础设施创建完成! 存储桶: {bucket_name}")
    print(f"网站 URL: {website_url}")
    
    # 步骤 2: 使用 Dagger 构建和部署网站内容
    print("正在使用 Dagger 构建和部署网站内容...")
    await dagger_pipeline(bucket_name)
    print("网站内容部署完成!")
    
    print(f"网站已成功部署，访问地址: {website_url}")


if __name__ == "__main__":
    anyio.run(main)