CREATE TABLE IF NOT EXISTS trending_videos (
    video_id TEXT,
    title TEXT,
    channel_title TEXT,
    category_id INTEGER,
    publish_time TIMESTAMP,
    tags TEXT,
    views INTEGER,
    likes INTEGER,
    dislikes INTEGER,
    comment_count INTEGER
);
