from boto3 import session
import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

__author__ = 'Klera DevOps'
__version__ = '0.0.1'


class aws_client:
    def __init__(self, **kwargs):
        if 'aws_access_key_id' in kwargs.keys() and 'aws_secret_access_key' in kwargs.keys():
            self.session = session.Session(
                aws_access_key_id=kwargs['aws_access_key_id'],
                aws_secret_access_key=kwargs['aws_secret_access_key'],
            )
        elif 'profile_name' in kwargs.keys():
            self.session = session.Session(profile_name=kwargs['profile_name'])

    from .utils import get_regions, list_elastic_beanstalk_envs, list_eks_clusters, list_ecr_repositories, \
        list_codebuild_projects
    from .elastic_beanstalk import enhanced_health_reporting_enabled, managed_updates_enabled
    from .cloudformation import stack_notification_check
    from .eks import eks_secrets_encrypted, eks_endpoint_no_public_access
    from .ecr import ecr_private_image_scanning_enabled
    from .codebuild import project_artifact_encryption_enabled, project_environment_privileged_check, \
        project_logging_enabled, project_s3_logs_encrypted

    def get_compliance(self) -> list:
        """
        :return:
        """
        regions = self.get_regions()
        eb_envs = self.list_elastic_beanstalk_envs(regions=regions)

        compliance = [
            self.enhanced_health_reporting_enabled(eb_envs),
            self.managed_updates_enabled(environments=eb_envs),
            self.stack_notification_check(regions),
        ]

        # calling the compliance methods for eks
        try:
            eks_clusters = self.list_eks_clusters(regions)
        except ClientError as e:
            logger.error("Access Denied")
            compliance.append(self.eks_secrets_encrypted(exception=True, exception_text=e.response['Error']['Code']))
            compliance.append(self.eks_endpoint_no_public_access(
                exception=True, exception_text=e.response['Error']['Code']
            ))
        else:
            compliance.append(self.eks_secrets_encrypted(eks_lst=eks_clusters))
            compliance.append(self.eks_endpoint_no_public_access(eks_lst=eks_clusters))

        # calling the compliance methods for ecr
        try:
            repos = self.list_ecr_repositories(regions=regions)
        except ClientError as e:
            logger.error("Access Denied")
            compliance.append(self.ecr_private_image_scanning_enabled(
                exception=True, exception_text=e.response['Error']['Code']))
        else:
            compliance.append(self.ecr_private_image_scanning_enabled(repo_lst=repos))

        # calling the compliance methods of codebuild
        try:
            projects = self.list_codebuild_projects(regions=regions)
        except ClientError as e:
            logger.error("Access Denied")
            compliance.append(self.project_artifact_encryption_enabled(
                exception=True, exception_text=e.response['Error']['Code']))
            compliance.append(self.project_environment_privileged_check(
                exception=True, exception_text=e.response['Error']['Code']))
            compliance.append(self.project_logging_enabled(
                exception=True, exception_text=e.response['Error']['Code']))
            compliance.append(self.project_s3_logs_encrypted(
                exception=True, exception_text=e.response['Error']['Code']))
        else:
            compliance.append(self.project_artifact_encryption_enabled(projects=projects))
            compliance.append(self.project_environment_privileged_check(projects=projects))
            compliance.append(self.project_logging_enabled(projects=projects))
            compliance.append(self.project_s3_logs_encrypted(projects=projects))

        return compliance
