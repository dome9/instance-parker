import datetime
import ConfigParser

config = ConfigParser.ConfigParser()
config.read(['calendars.cfg'])
days = ["mon","tue","wed","thu","fri","sat","sun"]

def is_time_in_cal(cal_name,time):
    today = days[time.weekday()]
    time_int = int(time.strftime("%H%M"))
    instance_cal = parse_cal(cal_name)
    if today in instance_cal:
        today_cal = instance_cal[today]
        return (today_cal[0] <= time_int) & (time_int < today_cal[1])
    return False

# should return something like:
# {"MON":[0800,2000], "TUE":[0700,1400]}
def parse_cal(cal_name):
    ret = {}
    if cal_name in config.sections():
        for item in config.items(cal_name):
            time = [int(t.replace(":","")) for t in item[1].split("-")]
            ret[item[0]] = time
    #print ret
    return ret;
        
if __name__ == "__main__":
    monday_morning = datetime.datetime(2016,1,18,10,0,0,0)
    assert is_time_in_cal("workdays",monday_morning)
    assert not is_time_in_cal("weekends",monday_morning)
    assert not is_time_in_cal("never",monday_morning)
    assert is_time_in_cal("always",monday_morning)
    assert not is_time_in_cal("wrong",monday_morning)
