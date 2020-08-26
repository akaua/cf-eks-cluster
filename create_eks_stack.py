import boto3
import botocore
import json
import time

client_cloud_formation_main = boto3.client('cloudformation', region_name='us-east-1')

def start():
    res = raw_input("Voce gostaria de criar a stack: (Y/N) \n") 
    if res.lower()=='y': 
        print "Iniciando Criacao"
    else:
        print 'Cancelando'
        exit()

def _stack_exists(stack_name):
    stacks = client_cloud_formation_main.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackStatus'] == 'DELETE_COMPLETE':
            continue
        if stack_name == stack['StackName']:
            return True
    return False

def create_stack_vpc():
    print '######### Iniciando criacao de VPC para EKS #########'
    stack_name = 'VPCEKSStack'
    try:
        if _stack_exists(stack_name):
            print('Updating {}'.format(stack_name))
            with open('./templates/amazon-eks-vpc.yaml', 'r') as cf_main_vpc_file:
                cft_main_vpc_template = cf_main_vpc_file.read()

                response = client_cloud_formation_main.update_stack(
                            StackName=stack_name,
                            TemplateBody=cft_main_vpc_template,
                            Capabilities=[
                                'CAPABILITY_IAM'
                            ]
                        )
            waiter = client_cloud_formation_main.get_waiter('stack_update_complete')
        else:
            print('Creating {}'.format(stack_name))
            with open('./templates/amazon-eks-vpc.yaml', 'r') as cf_main_vpc_file:
                cft_main_vpc_template = cf_main_vpc_file.read()

                response = client_cloud_formation_main.create_stack(
                            StackName=stack_name,
                            TemplateBody=cft_main_vpc_template,
                            Capabilities=[
                                'CAPABILITY_IAM'
                            ],
                            OnFailure='ROLLBACK'
                        )
                    
            waiter = client_cloud_formation_main.get_waiter('stack_create_complete')
        print("...waiting for stack to be ready...")
        waiter.wait(StackName=stack_name)
    except botocore.exceptions.ClientError as ex:
        error_message = ex.response['Error']['Message']
        if error_message == 'No updates are to be performed.':
            print("No changes")
        else:
            raise
    else:
        print(
            client_cloud_formation_main.describe_stacks(StackName=response['StackId'])
        )

def create_stack_eks():
    stack_name='EKSClusterStack'
    print '######### Iniciando criacao do cluster EKS #########'

    try:
        if _stack_exists(stack_name):
            print('Updating {}'.format(stack_name))
            with open('./templates/amazon-eks-cluster.yaml', 'r') as cf_file:
                cft_template = cf_file.read()
                with open('./parameters/amazon-eks-cluster.json', 'r') as param_file:
                    cft_param = json.loads(param_file.read())
                    response_main = client_cloud_formation_main.update_stack(
                                StackName=stack_name,
                                TemplateBody=cft_template,
                                Parameters=cft_param,
                                Capabilities=[
                                    'CAPABILITY_IAM'
                                ]
                            )
            waiter = client_cloud_formation_main.get_waiter('stack_update_complete')
        else:
            print('Creating {}'.format(stack_name))
            with open('./templates/amazon-eks-cluster.yaml', 'r') as cf_file:
                cft_template = cf_file.read()
                with open('./parameters/amazon-eks-cluster.json', 'r') as param_file:
                    cft_param = json.loads(param_file.read())
                    response_main = client_cloud_formation_main.create_stack(
                                StackName=stack_name,
                                TemplateBody=cft_template,
                                Parameters=cft_param,
                                Capabilities=[
                                    'CAPABILITY_IAM'
                                ],
                                OnFailure='ROLLBACK'
                            )
            waiter = client_cloud_formation_main.get_waiter('stack_create_complete')
        print("...waiting for stack to be ready...")
        waiter.wait(StackName=stack_name)
    except botocore.exceptions.ClientError as ex:
        error_message = ex.response['Error']['Message']
        if error_message == 'No updates are to be performed.':
            print("No changes")
        else:
            raise
    else:
        print(
            client_cloud_formation_main.describe_stacks(StackName=response_main['StackId'])
        )


start()
create_stack_vpc()
create_stack_eks()
