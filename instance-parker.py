#from __future__ import print_function
#import json
import cal
import datetime


def lambda_handler(event, context):
    return park_instances()
    
def park_instances():
    import boto3
    ec2 = boto3.resource('ec2')
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
    return {"parker-controlled":len(parker_instances), "stopped":len(toStop),"started": len(toStart)}


if __name__ == "__main__":
    #print("main is here", string.split(global_calendars['weekdays'],','))
    #print(cal.is_time_in_cal("workdays",datetime.datetime.now()))
    park_instances()