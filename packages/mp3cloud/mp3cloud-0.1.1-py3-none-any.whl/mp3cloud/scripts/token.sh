# cURL fetches the webpage without anu issue while python `requests` lib
# returns 403 forbidden. thread on https://github.com/rtcq/freemp3cloud-downloader/issues/1

curl 'https://wwv.freemp3cloud.com/' \
  -H 'authority: wwv.freemp3cloud.com' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'accept-language: en-US,en;q=0.9,fa;q=0.8' \
  -H 'cache-control: max-age=0' \
  -H 'cookie: __ddg2_=OoNQEIynYTMJoVwU; __ddg1_=9NZlynXQBBht02meCgQe; _ym_uid=1669227862874709378; .AspNetCore.Antiforgery.2kyQ2nmXF04=CfDJ8JKPcoD1_8lEtTdrfYWqW-lcrqTxTPlY2MpWV3ii0eqR_t8QkYs-NGxFjaBu16S4r6GlnTRPRyqmtlOBwFy9kkdg7bPp5rF_J-a8zJwrwySY6lYjG2VlWnQGK6G9C5NU6cpWrIltLwN9IjQuOq_mSmk; _ym_isad=1' \
  -H 'sec-ch-ua: "Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: none' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' \
  --compressed