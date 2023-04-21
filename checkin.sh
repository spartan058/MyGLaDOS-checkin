echo '------------------sign------------------'
curl -H "cookie:${COOKIE}" -H 'content-type:application/json;charset=UTF-8' -d '{"token": "glados.network"}' -X POST 'https://glados.rocks/api/user/checkin' | grep -Eo '"message":"[^"]*"'
echo '-----------------status-----------------'
leftDays=`curl -H "cookie:${COOKIE}" -X GET 'https://glados.rocks/api/user/status' | grep -Eo '"leftDays":"[^"]*"' |awk -F '"' '{print $4}' | awk -F '.' '{print $1}'`
echo '-----------------Notify-----------------'
curl https://sctapi.ftqq.com/${SCKEY}.send?title=leftDays:${leftDays}
