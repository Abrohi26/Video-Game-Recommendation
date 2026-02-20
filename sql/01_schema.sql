CREATE TABLE IF NOT EXISTS video_games (
  name              text,
  platform          varchar(20),
  year_of_release   integer,
  genre             varchar(50),
  publisher         text,
  na_sales          numeric(6,2),
  eu_sales          numeric(6,2),
  jp_sales          numeric(6,2),
  other_sales       numeric(6,2),
  global_sales      numeric(6,2),
  critic_score      integer,
  critic_count      integer,
  user_score        text,
  user_count        integer,
  developer         text,
  rating            varchar(10)
);

-- Helpful for filtering/ranking
CREATE INDEX IF NOT EXISTS idx_vg_platform ON video_games(platform);
CREATE INDEX IF NOT EXISTS idx_vg_genre ON video_games(genre);
CREATE INDEX IF NOT EXISTS idx_vg_year ON video_games(year_of_release);
