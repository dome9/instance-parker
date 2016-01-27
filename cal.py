import datetime
import ConfigParser

config = ConfigParser.ConfigParser()
config.read(['calendars.cfg'])
days = ["mon","tue","wed","thu","fri","sat","sun"]

def is_time_in_cal(cal_name,time):
    today = days[time.weekday()]
    time_int = int(time.strftime("%H%M"))
    instance_cal = parse_cal(cal_name)
    if not today in instance_cal:
        return False
    today_scheds = instance_cal[today]
    return  any([sched for sched in today_scheds if ((sched[0] <= time_int) & (time_int < sched[1])) ])

# should return something like:
# {"MON":[[0800,2000],[2100,2200]], "TUE":[[0700,1400]]}
# original config item looks like : ('mon', '08:00-11:00,21:00-22:00') 
def parse_cal(cal_name):
    if not cal_name in config.sections():
        raise ValueError('could not find calendar named %s. Check your calendars configuration file or the instance tag' % cal_name)
    
    ret = {}
    for day in config.items(cal_name):
        times = [ [int(t.replace(":","")) for t in window.split("-")] for window in day[1].split(",")]
        ret[day[0]] = times
    return ret;

        
if __name__ == "__main__":
    monday_morning = datetime.datetime(2016,1,18,10,0,0,0)
    monday_noon = datetime.datetime(2016,1,18,12,0,0,0)
    monday_evening = datetime.datetime(2016,1,18,22,0,0,0)

    assert is_time_in_cal("test1",monday_morning)
    assert not is_time_in_cal("test1",monday_noon)
    assert is_time_in_cal("test1",monday_evening)
    assert not is_time_in_cal("never",monday_morning)
    assert is_time_in_cal("always",monday_morning)
    try:
        is_time_in_cal("ERROR", monday_morning)
        raise Exception("should throw exception when calnedar not found")
    except ValueError:
        pass
    print ":) tests passed"
