from typing import Dict, List
import boto3
import pytz
import datetime

# only select instances having tag category:ibgateway_instance
filters = [{'Name': 'tag:category', 'Values': ['ibgateway_instance']}]


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


def lambda_handler(event, context):
    # check whether falls into time range
    if event.get('time_range') and not inside_time_range(event.get('time_range'), get_utc_now()):
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
        for instance in qualified_ec2s:
            print('start instance {}'.format(instance.instance_id))
            instance.start()
    else:
        raise Exception('unable to handle operation : {}'.format(operation))
    return 0
