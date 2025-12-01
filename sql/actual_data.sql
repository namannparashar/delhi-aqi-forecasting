SELECT DATE(timestamp) AS date, ROUND(PM2_5,0) as PM2_5
FROM `delhi-weather-app-479422.weather_data.delhi_daily`
WHERE DATE(timestamp) <= CURRENT_DATE()
ORDER BY 1 DESC 
LIMIT 1000;