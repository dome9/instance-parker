# AWS Instance Parker (by Dome9)

A scheduled Lambda script that automatically stops and starts AWS instances according to predefined schedules.
This could yield a significant saving in your EC2 spent.

Installation / Usage:
--
Prep: make sure you have AWS CLI installed. In the future we'll add CF template to simplify the process.
It is possible to use AWS Lambda web console without the CLI. It is not documented here, but you can follow the utils/install script...
1. Create an IAM role for the Lambda script. This role should be able to query the instances and stop/start them. See 'IAM Policy' section for recommended IAM execution and trust policies
1. Clone this repo into your local workstation.
1. Edit the calendars.cfg file. Add your organization calendars (see 'Schedule format' section)
1. Add execution permissions for all scripts in utils folder.
```bash
chmod +x utils/*
```
1. Run the install script, you'll need to provide the ARN of role you have created:
```bash
utils/install <ARN of my newly created role>
```
1. If you got the error "A client error (InvalidParameterValueException) occurred when calling the CreateFunction operation: The role defined for the function cannot be assumed by Lambda." make sure you have added the *trust relationship* as defined in the IAM section.
1. Verify that the script is correctly deployed to Lambda by running utils/run or manually invoking it from Lambda web console.
You should get result like:
```javascript
{
  "started": 0,
  "stopped": 0,
  "parker-controlled": 0
}
```
1. Now is the fun time. Add the tag 'instance-parker' to all your EC2 instances you wish to schedule. The value should be the name of the schedule.
(Example: "instance-parker":"weekdays") run the Lambda function again, and test that the instances are started or stopped according to your chosen schedules.
1. After validated, it is time to schedule your lambda function to run periodically. The easiest way to do so is via the Lambda Web console, by adding event source and choosing CloudWatch Events - Schedule.
The minimal interval is 5 minutes, which should be sufficient for this kind of task.
1. Enjoy saving resources and money. You just made the world a greener place :) 

IAM Policies:
--
This is the IAM execution policy for your new role:
```javascript
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "lambdaLogging",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
        "Sid": "d9Parker",
        "Effect": "Allow",
        "Action": [
            "ec2:DescribeInstances",
            "ec2:StopInstances",
            "ec2:StartInstances"
        ],
        "Resource": [
            "*"
        ]
    }
  ]
}
```
In addition you'll need to allow the Lambda service to assume this role.
MyRole> Edit trsut relationship:
```javascript
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Schedules format:
--
* You'll need to edit the calendars.cfg file in order to define your own organizational schedules.
* The format is:
[calendar_name]
DAY = HH:MM-HH:MM (ex. TUE = 08:00-20:00)

* For now, the timezone is UTC. So a schedule like Saturday between 7AM to 8PM PST (UTC+8) would be written as SAT-15:00-24:00,SUN-00:00-04:00
(converted into UTC and split into 2 days)
Some builtin schedules are provided. You can review / edit / delete them

TODOs and future directions:
--
* Adding multiple schedules per a single instance - allowing a composition of schedules
* Supporting custom schedules that are defined ad-hok at the instance (tag) level (rather at a global location)
* Adding more complex schedules schemes (like cron format)
* Moving the schedules into a seperate location (S3?) allowing to add / modify global scedules without modifying/ redeploying the Lambda code
* Adding CloudFormation to ease deployment of the script.
* Better error handling when schedule name does not match, schedule syntaxt error...
* Think about concept of dry-run and how to test schedules.

