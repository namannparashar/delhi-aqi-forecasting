WITH max_dt AS (
  SELECT MAX(DATE(timestamp)) AS last_date, MAX(PM2_5) AS last_aqi 
  FROM `delhi-weather-app-479422.weather_data.delhi_daily`
),

future_dates AS (
  SELECT
    DATE_ADD(last_date, INTERVAL day_num DAY) AS timestamp
  FROM max_dt,
  UNNEST(GENERATE_ARRAY(1, 30)) AS day_num
)
SELECT DATE(timestamp) AS timestamp, PM2_5, Wind_Speed, Wind_Direction, Humidity, Temperature
FROM `delhi-weather-app-479422.weather_data.delhi_daily`
WHERE DATE(timestamp) > '2022-08-03'

UNION ALL

-- mdt.PM2_5 is just a placeholder for future values of PM2_5 that are to be forecasted
-- wind speed, wind direction, humidity, temperature values are taken assuming yearly seasonality, for simplicity
SELECT fd.timestamp, mdt.last_aqi AS PM2_5, a.Wind_Speed, a.Wind_Direction, a.Humidity, a.Temperature
FROM future_dates fd 
JOIN max_dt mdt 
ON fd.timestamp >= mdt.last_date 
LEFT JOIN `delhi-weather-app-479422.weather_data.delhi_daily` a 
ON DATE(a.timestamp) = DATE_SUB(DATE(fd.timestamp), INTERVAL 1 YEAR)
ORDER BY timestamp;
