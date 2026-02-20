-- Recommender function: ranks games using a weighted, normalized score
-- Inputs:
--   p_platform: 'Any' or exact platform value (e.g., 'PS4')
--   p_new_old:  'Any' | 'New' | 'Old' (cutoff = 2015)
--   p_care_critic: 1 = prioritize critic score, 0 = ignore critic requirement
--   p_sales_matter: 1 = include sales signal strongly, 0 = weak sales signal
--   p_genre: 'Any' or exact genre value (e.g., 'Action')

CREATE OR REPLACE FUNCTION recommend_games(
  p_platform text,
  p_new_old text,
  p_care_critic int,
  p_sales_matter int,
  p_genre text,
  p_limit int DEFAULT 20
)
RETURNS TABLE (
  name text,
  platform text,
  genre text,
  year_of_release int,
  critic_score numeric,
  global_sales numeric,
  relevance_score numeric
)
LANGUAGE sql
AS $$
WITH bounds AS (
  SELECT
    MIN(critic_score) AS min_critic,
    MAX(critic_score) AS max_critic,
    MIN(global_sales) AS min_sales,
    MAX(global_sales) AS max_sales,
    AVG(critic_score) AS avg_critic
  FROM video_games
),
scored AS (
  SELECT
    vg.name, vg.platform, vg.genre, vg.year_of_release, vg.critic_score, vg.global_sales,

    -- Normalize critic to 0..1 (use avg if null)
    CASE
      WHEN b.max_critic = b.min_critic THEN 0
      ELSE (COALESCE(vg.critic_score, b.avg_critic) - b.min_critic) * 1.0 / (b.max_critic - b.min_critic)
    END AS critic_norm,

    -- Normalize sales to 0..1
    CASE
      WHEN vg.global_sales IS NULL OR b.max_sales = b.min_sales THEN 0
      ELSE (vg.global_sales - b.min_sales) * 1.0 / (b.max_sales - b.min_sales)
    END AS sales_norm,

    -- Match flags (0/1)
    CASE WHEN p_platform = 'Any' THEN 1 WHEN vg.platform = p_platform THEN 1 ELSE 0 END AS platform_match,
    CASE WHEN p_genre    = 'Any' THEN 1 WHEN vg.genre    = p_genre    THEN 1 ELSE 0 END AS genre_match,
    CASE
      WHEN p_new_old = 'Any' THEN 1
      WHEN p_new_old = 'New' AND vg.year_of_release >= 2015 THEN 1
      WHEN p_new_old = 'Old' AND vg.year_of_release < 2015 THEN 1
      ELSE 0
    END AS year_match,

    -- Dynamic weights
    (CASE WHEN p_care_critic  = 1 THEN 0.45 ELSE 0.15 END) AS w_critic,
    (CASE WHEN p_sales_matter = 1 THEN 0.25 ELSE 0.10 END) AS w_sales,
    0.15 AS w_platform,
    0.10 AS w_genre,
    0.05 AS w_year

  FROM video_games vg
  CROSS JOIN bounds b
  WHERE (p_care_critic = 0 OR vg.critic_score IS NOT NULL)
),
ranked AS (
  SELECT
    *,
    (
      platform_match * w_platform +
      genre_match    * w_genre +
      year_match     * w_year +
      critic_norm    * w_critic +
      sales_norm     * w_sales
    ) AS relevance_score,

    -- Deduplicate titles: keep best scoring row per game name
    ROW_NUMBER() OVER (
      PARTITION BY name
      ORDER BY
        (
          platform_match * w_platform +
          genre_match    * w_genre +
          year_match     * w_year +
          critic_norm    * w_critic +
          sales_norm     * w_sales
        ) DESC,
        critic_score DESC NULLS LAST,
        global_sales DESC NULLS LAST
    ) AS rn
  FROM scored
)
SELECT
  name, platform, genre, year_of_release,
  critic_score::numeric, global_sales::numeric,
  ROUND(relevance_score::numeric, 4) AS relevance_score
FROM ranked
WHERE rn = 1
ORDER BY relevance_score DESC NULLS LAST
LIMIT p_limit;
$$;

-- Examples
SELECT * FROM recommend_games('PS4','New',1,1,'Action',20);
SELECT * FROM recommend_games('Any','Any',1,1,'Any',10);
