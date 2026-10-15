-- Step 3: Business questions answered with SQL

-- 1. On-time delivery % by hub
SELECT hub,
       COUNT(*) AS total_orders,
       ROUND(100.0 * SUM(on_time) / COUNT(*), 1) AS on_time_pct
FROM deliveries
GROUP BY hub
ORDER BY on_time_pct DESC;

-- 2. Top 10 riders by on-time deliveries (min 50 orders)
SELECT rider_id, COUNT(*) AS orders, SUM(on_time) AS on_time_orders,
       ROUND(100.0 * SUM(on_time) / COUNT(*), 1) AS on_time_pct
FROM deliveries
WHERE rider_id <> 'UNKNOWN'
GROUP BY rider_id
HAVING COUNT(*) >= 50
ORDER BY on_time_pct DESC
LIMIT 10;

-- 3. Peak pickup hours
SELECT strftime('%H', pickup_time) AS hour_of_day, COUNT(*) AS orders
FROM deliveries
GROUP BY hour_of_day
ORDER BY orders DESC;

-- 4. Failed delivery reasons
SELECT fail_reason, COUNT(*) AS cases
FROM deliveries
WHERE status <> 'Delivered'
GROUP BY fail_reason
ORDER BY cases DESC;

-- 5. Rank hubs within each city (window function)
SELECT city, hub, on_time_pct,
       RANK() OVER (PARTITION BY city ORDER BY on_time_pct DESC) AS rank_in_city
FROM (
  SELECT city, hub, ROUND(100.0 * SUM(on_time) / COUNT(*), 1) AS on_time_pct
  FROM deliveries GROUP BY city, hub
);

-- 6. Weekly trend of on-time %
SELECT strftime('%Y-%W', pickup_time) AS week,
       ROUND(100.0 * SUM(on_time) / COUNT(*), 1) AS on_time_pct
FROM deliveries
GROUP BY week
ORDER BY week;
