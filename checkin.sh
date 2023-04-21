echo '------------------sign------------------'
curl -H "cookie:${COOKIE}" -H 'content-type:application/json;charset=UTF-8' -d '{"token": "glados.network"}' -X POST 'https://glados.rocks/api/user/checkin' | grep -Eo '"message":"[^"]*"'
echo '-----------------status-----------------'
leftDays=`curl -H "cookie:${COOKIE}" -X GET 'https://glados.rocks/api/user/status' | grep -Eo '"leftDays":"[^"]*"' |awk -F '"' '{print $4}' | awk -F '.' '{print $1}'`
echo '-----------------Notify-----------------'
curl " -X GET https://sctapi.ftqq.com/SCT206874TDXkYKVRQ15az1U0fIiQukc0u.send?title=leftDays:${leftDays}"