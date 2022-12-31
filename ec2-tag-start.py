import json,boto3
ec2 = boto3.client('ec2')

def lambda_handler(event,context):
    ec2_dict =ec2.describe_instances()
    reservation_list = ec2_dict['Reservations']
    print(type(reservation_list))
    print(len(reservation_list))
    for instances in reservation_list:
        instance_id = instances['Instances'][0]['InstanceId']
        instance_state = instances['Instances'][0]['State']['Name']
        tages = instances['Instances'][0]['Tags']
        print("instance id is :",instance_id )
        print("instance state is :",instance_state )
        print("instance tags is :",tages )
        instanceIdlist = []
        for tag in tages:
            if tag['Key'] == 'env' and tag['Value'] == 'qa':
                if instance_state == 'stopped':
                    print(instance_id ,"will be started")
                    instanceIdlist.append(instance_id)
                    ec2.start_instances(InstanceIds=instanceIdlist)