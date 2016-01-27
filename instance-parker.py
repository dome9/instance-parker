#from __future__ import print_function
#import json
import cal
import datetime
import boto3


def lambda_handler(event, context):
    return park_instances()
    
def park_instances():
    regions_result = boto3.client('ec2').describe_regions()
    regions = [x["RegionName"] for x in regions_result["Regions"]]
    # all regions are dynamically fetched from AWS. 
    # alternatively you can comment the prev block and use a hard coded list like in the next line:
    #regions = ["eu-west-1", "ap-southeast-1", "ap-southeast-2", "eu-central-1", "ap-northeast-2", "ap-northeast-1", "us-east-1", "sa-east-1", "us-west-1", "us-west-2"]
    return [park_instances_in_region(region) for region in regions]
    

def park_instances_in_region(region):
    print "Starting instance parker for region: ", region
    session = boto3.session.Session(region_name=region)
    ec2 = session.resource('ec2')
    
    instances = ec2.instances.filter()
    parker_instances = [i for i in instances if any(x['Key']=="instance-parker" for x in i.tags)]
    
    print("Found %d instance-parker controlled instances" % len(parker_instances))
    running = [i for i in parker_instances if i.state['Name']=="running"]
    stopped = [i for i in parker_instances if i.state['Name']=="stopped"]
    
    now = datetime.datetime.now();
    toStop= [i for i in running if not cal.is_time_in_cal(next(t for t in i.tags if t['Key']=="instance-parker")['Value'],now)]
    toStart= [i for i in stopped if cal.is_time_in_cal(next(t for t in i.tags if t['Key']=="instance-parker")['Value'],now)]
    print("toStop",toStop,"toStart",toStart);
    for i in toStop:
        print("about to stop",i)
        i.stop();
    for i in toStart:
        print("about to start",i)
        i.start();
    return {"parker-controlled":len(parker_instances), "region": region, "stopping":len(toStop),"starting": len(toStart)}

if __name__ == "__main__":
    park_instances()
    