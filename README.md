# cf-eks-cluster

## Description

### This project is to create a hight availability EKS Cluster architecture 

## Dependencies

- ### AWS credentials configured on '/.aws' path
- ### python 2.7 installed
```sh
$ sudo apt install python
```
- ### pip 9 installed
```sh
$ sudo apt install python-pip
```
## First install the dependencies of the python project:
```sh
$ pip install -r requirements.txt
```

## For create the stack, just execute:
```sh
$ python create_eks_stack.py
```

## For destroy the stack, just execute:
```sh
$ python destroy_eks_stack.py
```