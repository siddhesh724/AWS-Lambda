import json
import boto3
ec2 = boto3.client('ec2')
def lambda_handler(event, context):
    print("event object is ",event)
    ec2_dict=ec2.describe_instances()
    reservations_list=ec2_dict['Reservations']
    print("reservations_list:",reservations_list,"type(reservations_list):",type(reservations_list),"len(reservations_list):",len(reservations_list))
    print("-----------------------------------------")
    InstanceIdsList=[]
    for instance in reservations_list:
        print("instance is of type",type(instance))
        instance_id=instance['Instances'][0]['InstanceId']
        instance_state=instance['Instances'][0]['State']['Name']
        tags_list=instance['Instances'][0]['Tags']
        print("tags_list is - ", tags_list)
        print("instance_id is",instance_id)
        print("instance_state is",instance_state)
    # [{'Key': 'env', 'Value': 'dev'}, {'Key': 'Name', 'Value': 'EC2-B'}]
        for tags in tags_list:
            print(type(tags))
            if tags['Key'] == 'env' and tags['Value'] == 'dev':
                if instance_state == 'stopped':
                    print(instance_id ,"will be started")
                    InstanceIdsList.append(instance_id)
    if not InstanceIdsList:
        print("InstanceIdsList is empty, cannot perform start operation")
    else:
        print("Starting all the instances with instance ids: ",InstanceIdsList)
        ec2.start_instances(InstanceIds=InstanceIdsList)
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
