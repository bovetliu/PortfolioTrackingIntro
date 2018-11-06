from typing import Dict, List
import boto3
import pytz
import datetime

# only select instances having tag category:ibgateway_instance
filters = [{'Name': 'tag:category', 'Values': ['ibgateway_instance']}]

nyse_holidays = [
    "2017-01-02",
    "2017-01-16",
    "2017-02-20",
    "2017-04-14",
    "2017-05-29",
    "2017-07-04",
    "2017-09-04",
    "2017-11-23",
    "2017-12-25",

    "2018-01-01",
    "2018-01-15",
    "2018-02-19",
    "2018-03-30",
    "2018-05-28",
    "2018-07-04",
    "2018-09-03",
    "2018-11-22",
    "2018-12-25",

    "2019-01-01",
    "2019-01-21",
    "2019-02-18",
    "2019-04-19",
    "2019-05-27",
    "2019-07-04",
    "2019-09-02",
    "2019-11-28",
    "2019-12-25",

    "2020-01-01",
    "2020-01-20",
    "2020-02-17",
    "2020-04-10",
    "2020-05-25",
    "2020-07-03",
    "2020-09-07",
    "2020-11-26",
    "2020-12-25",
]


def get_utc_now() -> datetime:
    return pytz.utc.localize(datetime.datetime.utcnow(), is_dst=None)


def inside_time_range(time_range: List[Dict], time_to_test=get_utc_now()):
    if not isinstance(time_range, list):
        raise TypeError('time_range should be a list with 2 objects.')
    utc_time = get_utc_now()
    begin_time_tz = pytz.timezone(time_range[0]['tz'])
    timezoned_now = utc_time.astimezone(begin_time_tz)
    begin_time_of_day = datetime.datetime.strptime(time_range[0]['time_of_day'], "%H:%M").time()
    begin_time_timezoned = timezoned_now.replace(
        hour=begin_time_of_day.hour, minute=begin_time_of_day.minute, second=begin_time_of_day.second)

    end_time_of_day = datetime.datetime.strptime(time_range[1]['time_of_day'], "%H:%M").time()
    end_time_tz = pytz.timezone(time_range[1]['tz'])
    timezoned_now = utc_time.astimezone(end_time_tz)
    end_time_timezoned = timezoned_now.replace(
        hour=end_time_of_day.hour, minute=end_time_of_day.minute, second=end_time_of_day.second)
    return begin_time_timezoned <= time_to_test <= end_time_timezoned


def is_nyse_holiday(utc_now: datetime.datetime):
    if not isinstance(utc_now, datetime.datetime):
        raise TypeError("parameter utc_now must be an instance of datetime")
    ny_tz = pytz.timezone('America/New_York')
    return utc_now.astimezone(ny_tz).date().isoformat() in nyse_holidays


def lambda_handler(event, context):
    # check whether falls into time range
    utc_now = get_utc_now()
    if event.get('time_range') and not inside_time_range(event.get('time_range'), utc_now):
        print("not invoked inside desired time range, going to exit 0.")
        return 0
    region = event.get('region')
    ec2 = boto3.resource('ec2', region_name=region)
    if event.get("filters"):
        filters = event.get('filters')
    qualified_ec2s = ec2.instances.filter(Filters=filters)
    operation = event.get('operation')
    if operation == 'stop_instances':
        for instance in qualified_ec2s:
            print('stop instance {}'.format(instance.instance_id))
            instance.stop()
    elif operation == 'start_instances':
        if is_nyse_holiday(utc_now):
            print("will not attempt starting instance since today is nyse holidy")
            return 0
        for instance in qualified_ec2s:
            print('start instance {}'.format(instance.instance_id))
            instance.start()
    else:
        raise Exception('unable to handle operation : {}'.format(operation))
    return 0
