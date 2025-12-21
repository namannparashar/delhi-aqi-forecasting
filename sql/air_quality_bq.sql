WITH max_dt AS (
  SELECT MAX(DATE(timestamp)) AS last_date, ROUND(MAX(PM2_5),0) AS last_aqi 
  FROM `delhi-weather-app-479422.weather_data.delhi_daily`
),

future_dates AS (
  SELECT
    DATE_ADD(last_date, INTERVAL day_num DAY) AS timestamp
  FROM max_dt,
  UNNEST(GENERATE_ARRAY(1, 30)) AS day_num
)

SELECT DISTINCT date, PM2_5, Wind_Speed, Wind_Direction, Humidity, Temperature, Diwali_Flag
FROM 
(
SELECT DATE(timestamp) AS date, ROUND(PM2_5,0) AS PM2_5, Wind_Speed, Wind_Direction, Humidity, Temperature,
CASE WHEN DATE(timestamp) IN ("2022-10-22","2023-11-10","2024-10-29","2025-10-18") THEN 1 ELSE 0 END AS Diwali_Flag 
FROM `delhi-weather-app-479422.weather_data.delhi_daily`
WHERE DATE(timestamp) > '2022-08-03'

UNION ALL

-- mdt.PM2_5 is just a placeholder for future values of PM2_5 that are to be forecasted
-- wind speed, wind direction, humidity, temperature values are taken assuming yearly seasonality, for simplicity
SELECT fd.timestamp as date, mdt.last_aqi AS PM2_5, a.Wind_Speed, a.Wind_Direction, a.Humidity, a.Temperature,
CASE WHEN DATE(fd.timestamp) IN ("2022-10-22","2023-11-10","2024-10-29","2025-10-18") THEN 1 ELSE 0 END AS Diwali_Flag
FROM future_dates fd 
JOIN max_dt mdt 
ON fd.timestamp >= mdt.last_date 
LEFT JOIN `delhi-weather-app-479422.weather_data.delhi_daily` a 
ON DATE(a.timestamp) = DATE_SUB(DATE(fd.timestamp), INTERVAL 1 YEAR)
)
ORDER BY date;
