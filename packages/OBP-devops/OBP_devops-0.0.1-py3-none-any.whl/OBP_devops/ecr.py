"""
Contains the methods for all the compliance checks for AWS Elastic Container Registry
"""

import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Checks if a private Amazon Elastic Container Registry (ECR) repository has image scanning enabled
def ecr_private_image_scanning_enabled(self, **kwargs) -> dict:
    """
    :param repo_lst:
    :param self:
    :return:
    """
    logger.info(" ---Inside ecr :: ecr_private_image_scanning_enabled()--- ")

    result = True
    failReason = ''
    offenders = []
    compliance_type = "ECR Private Image Scanning Enabled"
    description = "Checks if a private Amazon Elastic Container Registry (ECR) repository has image scanning enabled"
    resource_type = "Elastic Container Registry"
    risk_level = 'Medium'

    if 'exception' in kwargs.keys() and kwargs['exception']:
        return {
            'Result': False,
            'failReason': kwargs['exception_text'],
            'resource_type': resource_type,
            'Offenders': offenders,
            'Compliance_type': compliance_type,
            'Description': description,
            'Risk Level': risk_level
        }

    for region, repos in kwargs['repo_lst'].items():
        for repo in repos:
            try:
                scan_on_push = repo['imageScanningConfiguration']['scanOnPush']
                if not scan_on_push:
                    result = False
                    failReason = 'Private image scanning is not enabled'
                    offenders.append(repo['repositoryName'])
            except KeyError:
                result = False
                failReason = 'Private image scanning is not enabled'
                offenders.append(repo['repositoryName'])

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level
    }


'''*************************This is an incomplete method, complete it first then include it in final compliance 
result'''


# Checks if a private Amazon Elastic Container Registry (ECR) repository has at least one lifecycle policy configured
def ecr_private_lifecycle_policy_configured(self, **kwargs) -> dict:
    """
    :param self:
    :param repo_lst:
    :return:
    """
    logger.info(" ---Inside ecr :: ecr_private_lifecycle_policy_configured()--- ")

    result = True
    failReason = ''
    offenders = []
    compliance_type = "ECR Private lifecycle policy configured"
    description = "Checks if a private Amazon Elastic Container Registry (ECR) repository has at least one lifecycle policy configured"
    resource_type = "Elastic Container Registry"
    risk_level = 'Low'

    if 'exception' in kwargs.keys() and kwargs['exception']:
        return {
            'Result': False,
            'failReason': kwargs['exception_text'],
            'resource_type': resource_type,
            'Offenders': offenders,
            'Compliance_type': compliance_type,
            'Description': description,
            'Risk Level': risk_level
        }

    for region, repos in kwargs['repo_lst'].items():
        client = self.session.client('ecr', region_name=region)
        for repo in repos:
            try:
                response = client.get_lifecycle_policy(
                    repositoryName=repo['repositoryName']
                )
                text = response['lifecyclePolicyText']
            except ClientError as e:
                if e.response['Error']['Code'] == 'LifecyclePolicyNotFoundException':
                    result = False
                    failReason = 'No lifecycle policy configured'
                    offenders.append(repo['repositoryName'])

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level
    }
