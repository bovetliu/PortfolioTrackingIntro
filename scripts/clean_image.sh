#!/usr/bin/env bash

# TODO(Bowei) use aws shell to automate following steps
# this file is used to prepare cleaned-up image
# 0. make sure master is in desired state
# 1. create snapshot, then stop ec2_running_ibgateways
# 2. create a new volume based on snapshot created in step1
# 3. detach ec2_running_ibgateways_vol from ec2_running_ibgateways
# 4. attach volume created in step 2 to ec2_running_ibgateways
# 5. start ec2_running_ibgateways
# 6. run this clean_image.sh
# 7. created snapshot of volume created in step2

stock_app_path=~/workrepo/InteractiveBroker/IBJts/person_stock_app
if [ -d "${stock_app_path}/src" ]; then
  cd ${stock_app_path}
  git checkout master
  git pull origin master
  git checkout ec2_config
  git rebase master
  mvn clean package -Dmaven.test.skip=true
  cp ${stock_app_path}/target/stockapp.jar /tmp
  rm -rf ~/workrepo/InteractiveBroker
  cd ~
  mkdir -p ${stock_app_path}/target
  mv /tmp/stockapp.jar ${stock_app_path}/target
else
  echo "no src folder in ${stock_app_path}, skip rebuilding stockapp jar."
fi

# replacing password in ibc configuration for Live and Paper configuration
sed -i 's/IbLoginId=..*/IbLoginId=edemog/' ~/JtsPaper/paper-ibc-config.ini
sed -i 's/IbPassword=..*/IbPassword=demouser/' ~/JtsPaper/paper-ibc-config.ini
sed -i 's/IbLoginId=..*/IbLoginId=edemog/' ~/JtsLive/live-ibc-config.ini
sed -i 's/IbPassword=..*/IbPassword=demouser/' ~/JtsLive/live-ibc-config.ini

printf "" > ~/JtsPaper/cronjob.log
rm -f ~/JtsPaper/launcher*log
find ~/JtsPaper/IBControllerLogs ! -name 'README.txt' -type f -exec rm -f {} +

printf "" > ~/JtsLive/cronjob.log
rm -f ~/JtsLive/launcher*log
find ~/JtsLive/IBControllerLogs ! -name 'README.txt' -type f -exec rm -f {} +

# clean stock app logs and state file
printf "" > ~/.local/share/opentechfin/livestate.txt
printf "" > ~/.local/share/opentechfin/paperstate.txt
rm -f  ~/.local/share/opentechfin/livelogs/*.log
rm -f ~/.local/share/opentechfin/paperlogs/*.log
