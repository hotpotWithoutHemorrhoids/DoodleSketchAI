-- DoodleSketchAI 数据库初始化脚本

-- 创建视频表
CREATE TABLE IF NOT EXISTS videos (
    id VARCHAR(36) PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    duration FLOAT,
    width INTEGER,
    height INTEGER,
    format VARCHAR(50),
    status ENUM('uploading', 'processing', 'ready', 'error') DEFAULT 'uploading',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- 创建断点表
CREATE TABLE IF NOT EXISTS breakpoints (
    id VARCHAR(36) PRIMARY KEY,
    video_id VARCHAR(36) NOT NULL,
    timestamp FLOAT NOT NULL,
    label VARCHAR(255),
    description TEXT,
    status ENUM('pending', 'processing', 'completed', 'error') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE,
    INDEX idx_video_id (video_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_status (status)
);

-- 创建任务表
CREATE TABLE IF NOT EXISTS tasks (
    id VARCHAR(36) PRIMARY KEY,
    video_id VARCHAR(36) NOT NULL,
    breakpoint_id VARCHAR(36),
    task_type ENUM('frame_extraction', 'sketch_generation', 'batch_processing') NOT NULL,
    status ENUM('pending', 'processing', 'completed', 'failed', 'cancelled') DEFAULT 'pending',
    progress INTEGER DEFAULT 0,
    result_data JSON,
    error_message TEXT,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE,
    FOREIGN KEY (breakpoint_id) REFERENCES breakpoints(id) ON DELETE SET NULL,
    INDEX idx_video_id (video_id),
    INDEX idx_status (status),
    INDEX idx_task_type (task_type),
    INDEX idx_created_at (created_at)
);

-- 创建生成结果表
CREATE TABLE IF NOT EXISTS generation_results (
    id VARCHAR(36) PRIMARY KEY,
    task_id VARCHAR(36) NOT NULL,
    breakpoint_id VARCHAR(36),
    original_frame_path VARCHAR(500),
    sketch_path VARCHAR(500),
    thumbnail_path VARCHAR(500),
    metadata JSON,
    file_size BIGINT,
    processing_time FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (breakpoint_id) REFERENCES breakpoints(id) ON DELETE CASCADE,
    INDEX idx_task_id (task_id),
    INDEX idx_breakpoint_id (breakpoint_id),
    INDEX idx_created_at (created_at)
);

-- 创建用户会话表 (可选，用于多用户支持)
CREATE TABLE IF NOT EXISTS user_sessions (
    id VARCHAR(36) PRIMARY KEY,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    user_data JSON,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_session_token (session_token),
    INDEX idx_expires_at (expires_at)
);

-- 创建系统配置表
CREATE TABLE IF NOT EXISTS system_config (
    id VARCHAR(36) PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_config_key (config_key)
);

-- 插入默认配置
INSERT IGNORE INTO system_config (id, config_key, config_value, description) VALUES
('config-1', 'max_file_size', '104857600', '最大文件上传大小 (字节)'),
('config-2', 'allowed_formats', 'mp4,avi,mov,wmv,flv,webm', '允许的视频格式'),
('config-3', 'max_breakpoints_per_video', '50', '每个视频最大断点数量'),
('config-4', 'sketch_quality', 'high', '简笔画质量设置'),
('config-5', 'concurrent_tasks_limit', '5', '并发任务数量限制');

-- 创建触发器：自动更新 updated_at 字段
DELIMITER //
CREATE TRIGGER videos_update_timestamp 
BEFORE UPDATE ON videos 
FOR EACH ROW 
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END//

CREATE TRIGGER breakpoints_update_timestamp 
BEFORE UPDATE ON breakpoints 
FOR EACH ROW 
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END//

CREATE TRIGGER tasks_update_timestamp 
BEFORE UPDATE ON tasks 
FOR EACH ROW 
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END//

CREATE TRIGGER system_config_update_timestamp 
BEFORE UPDATE ON system_config 
FOR EACH ROW 
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- 创建视图：视频统计信息
CREATE OR REPLACE VIEW video_stats AS
SELECT 
    v.id,
    v.filename,
    v.created_at,
    COUNT(DISTINCT bp.id) as breakpoint_count,
    COUNT(DISTINCT t.id) as task_count,
    COUNT(DISTINCT gr.id) as result_count,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) as completed_tasks,
    SUM(CASE WHEN t.status = 'failed' THEN 1 ELSE 0 END) as failed_tasks
FROM videos v
LEFT JOIN breakpoints bp ON v.id = bp.video_id
LEFT JOIN tasks t ON v.id = t.video_id
LEFT JOIN generation_results gr ON t.id = gr.task_id
GROUP BY v.id, v.filename, v.created_at;

-- 创建视图：任务进度统计
CREATE OR REPLACE VIEW task_progress_stats AS
SELECT 
    DATE(created_at) as date,
    task_type,
    status,
    COUNT(*) as count
FROM tasks
WHERE created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
GROUP BY DATE(created_at), task_type, status
ORDER BY date DESC;
