import boto3
import time

client_cloud_formation_main = boto3.client('cloudformation', region_name='us-east-1')

def start():
    res = raw_input("Voce gostaria de destruir a stack: (Y/N) \n") 
    if res.lower()=='y': 
        print "Iniciando destruicao"
    else:
        print 'Cancelando'
        exit()

def verificar_delete_stack_main(stack_name):
    nao_finalizado = True
    while nao_finalizado:
        time.sleep(30)
        try:
            Stack = client_cloud_formation_main.describe_stacks(StackName=stack_name)['Stacks'][0]
            StackStatus = Stack['StackStatus']
            print StackStatus
            print 'Ainda nao finalizou'
        except Exception:
            nao_finalizado = False

def destroy_stack_vpc():
    print '######### Iniciando destruicao de VPC #########'
    stack_name = 'VPCEKSStack'
    response_main = client_cloud_formation_main.delete_stack(StackName=stack_name)


def destroy_stack_eks_cluster():
    print '######### Iniciando destruicao de EKS Cluster Stack #########'
    stack_name='EKSClusterStack'
    response = client_cloud_formation_main.delete_stack(StackName=stack_name)
    print '######### Verificando se EKS Cluster foi destruido com sucesso #########'   
    verificar_delete_stack_main(stack_name=stack_name)
    print '######### Finalizada destruicao de EKS Cluster com sucesso #########'  

def destroy_stack_eks_node_group():
    print '######### Iniciando destruicao de EKS Node Group Stack #########'
    stack_name='EKSNodeGroupStack'
    response = client_cloud_formation_main.delete_stack(StackName=stack_name)
    print '######### Verificando se EKS Node Group foi destruido com sucesso #########'   
    verificar_delete_stack_main(stack_name=stack_name)
    print '######### Finalizada destruicao de EKS Node Group com sucesso #########'  


start()
destroy_stack_eks_node_group()
destroy_stack_eks_cluster()
destroy_stack_vpc()



