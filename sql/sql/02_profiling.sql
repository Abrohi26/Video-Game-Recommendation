-- Row count
SELECT COUNT(*) AS total_rows FROM video_games;

-- Null count per column
SELECT
  COUNT(*) AS total_rows,
  COUNT(*) - COUNT(name)            AS name_nulls,
  COUNT(*) - COUNT(platform)        AS platform_nulls,
  COUNT(*) - COUNT(year_of_release) AS year_nulls,
  COUNT(*) - COUNT(genre)           AS genre_nulls,
  COUNT(*) - COUNT(global_sales)    AS global_sales_nulls,
  COUNT(*) - COUNT(critic_score)    AS critic_score_nulls
FROM video_games;

-- Ranges
SELECT
  MIN(year_of_release) AS min_year,
  MAX(year_of_release) AS max_year,
  MAX(global_sales)    AS max_global_sales,
  MAX(critic_score)    AS max_critic_score
FROM video_games;
