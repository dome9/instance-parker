```
|          |                            ,---.          |              
|,---.,---.|--- ,---.,---.,---.,---.    |---',---.,---.|__/ ,---.,---.
||   |`---.|    ,---||   ||    |---'    |    ,---||    |  \ |---'|    
``   '`---'`---'`---^`   '`---'`---'    `    `---^`    `   ``---'`    
```
# AWS Instance Parker By Dome9

A scheduled AWS Lambda script that automatically stops and starts AWS instances according to predefined schedules.
This could reduce your AWS EC2 spend by 10%-30%%.

Installation / Usage
--
* (Recomemnded) Make sure you have the AWS CLI installed. In the future we might replace this with CF template to simplify the process.
It is possible to use AWS Lambda web console without the CLI. It is not documented here, but you can follow the utils/install script...
* Make sure that you (more correctly, your IAM user- the one that is assinged to the CLI / AWS console) have enough permissions to create lambda functions. The needed permissions are:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "myLambdaAdminPermisisons",
            "Effect": "Allow",
            "Action": [
                "lambda:*",
                "iam:PassRole"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```
* Make sure that your AWS CLI is configured to the relevant region that you wish to run the Lambda. FYI the AWS Lambda service is operational in these regions: http://docs.aws.amazon.com/general/latest/gr/rande.html#lambda_region.
***Note: the script will still connect to all regions in your account, so there is no need to deploy the same script on multiple regions.***
* Clone this repo into your local workstation.
* Edit the calendars.cfg file. Add your organization's calendars (see 'Schedule format' section)
* Create an IAM role for the Lambda script. This role should be able to query the instances and stop/start them. See 'IAM Policy' section for detailed IAM execution and trust policies
* Add execution permissions for all scripts in utils folder.
```bash
chmod +x utils/*
```
* Run the install script, you'll need to provide the ARN of role you have created:
```bash
utils/install <ARN of my newly created role>
```
* If you got the error "A client error (InvalidParameterValueException) occurred when calling the CreateFunction operation: The role defined for the function cannot be assumed by Lambda." make sure you have added the *trust relationship* as defined in the IAM section.
* Verify that the script is correctly deployed to Lambda by running utils/run or manually invoking it from Lambda web console.
You should get result like:
```javascript
[{
  "started": 0,
  "stopped": 0,
  "parker-controlled": 0,
  "region":"XYZ"
}...]
```
* Now is the fun time. Add the tag 'instance-parker' to all your EC2 instances you wish to schedule. The value should match the name of one of your schedules.
(Example: "instance-parker":"weekdays") run the Lambda function again, and test that the instances are started or stopped according to your chosen schedules.
* After validated, it is time to schedule your lambda function to run periodically. The easiest (and only) way to do so is via the Lambda Web console, by adding event source and choosing CloudWatch Events - Schedule.
The minimal interval is 5 minutes, which should be sufficient for this kind of task.
* Enjoy saving resources and money. You just made the world a greener place :) 

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
            "ec2:DescribeRegions",
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

* Timezone of these schedules is in ***UTC***. A schedule like Saturday between 7AM to 8PM PST (UTC+8) would be written as:
```
[mycal]
SAT = 15:00-24:00
SUN = 00:00-04:00
```
(converted into UTC and split into 2 days)
* It is possible to have multiple time slots for a single day. For that just use comma (without spaces). Ex:
```
[test]
TUE = 06:00-07:00,20:00-21:00
```
* Some builtin schedules are provided. You can review / edit / delete them

TODOs and future directions:
--
* Adding multiple schedules per a single instance - allowing a composition of schedules
* Supporting ad-hock schedules that are defined the instance (tag) level (rather at a global location)
* Adding more complex schedules schemes (like cron format)
* Moving the schedules into a seperate location (S3?) allowing to add / modify global scedules without modifying/ redeploying the Lambda code
* Adding CloudFormation to ease deployment of the script.
* Better error handling when schedule name do not match, schedule syntaxt error...

