-- ============================================================================
-- 数据库索引回滚脚本
-- ============================================================================
-- 文件: 001_add_indexes_rollback.sql
-- 版本: 1.0
-- 创建日期: 2025-10-14
-- 关联: 001_add_indexes.sql (Phase 3.5.4 Day 1)
-- 
-- 用途:
--   回滚性能优化索引，恢复到原始数据库状态
--
-- 使用场景:
--   1. 索引导致意外性能问题
--   2. 降级到旧版本
--   3. 测试环境清理
--
-- 执行方式:
--   psql -U postgres -d langgraph_db -f backend/migrations/001_add_indexes_rollback.sql
--
-- 安全性:
--   - 使用 IF EXISTS 防止错误
--   - 不影响数据完整性
--   - 可重复执行（幂等性）
-- ============================================================================

\echo '================================================'
\echo '开始回滚数据库索引...'
\echo '================================================'

-- ============================================================================
-- Papers 表索引回滚
-- ============================================================================

\echo ''
\echo '📄 Papers 表索引回滚...'

-- 删除 session_id 索引
DROP INDEX IF EXISTS idx_papers_session_id;
\echo '  ✓ 已删除 idx_papers_session_id'

-- 删除 doi 条件索引
DROP INDEX IF EXISTS idx_papers_doi;
\echo '  ✓ 已删除 idx_papers_doi'

-- 删除 created_at 索引
DROP INDEX IF EXISTS idx_papers_created_at;
\echo '  ✓ 已删除 idx_papers_created_at'

-- ============================================================================
-- Reports 表索引回滚
-- ============================================================================

\echo ''
\echo '📊 Reports 表索引回滚...'

-- 删除 session_id 索引
DROP INDEX IF EXISTS idx_reports_session_id;
\echo '  ✓ 已删除 idx_reports_session_id'

-- 删除组合索引 (session_id, version)
DROP INDEX IF EXISTS idx_reports_session_version;
\echo '  ✓ 已删除 idx_reports_session_version'

-- ============================================================================
-- Session Events 表索引回滚
-- ============================================================================

\echo ''
\echo '📅 Session Events 表索引回滚...'

-- 删除 session_id 索引
DROP INDEX IF EXISTS idx_session_events_session_id;
\echo '  ✓ 已删除 idx_session_events_session_id'

-- 删除 event_type 索引
DROP INDEX IF EXISTS idx_session_events_event_type;
\echo '  ✓ 已删除 idx_session_events_event_type'

-- 删除 created_at 索引
DROP INDEX IF EXISTS idx_session_events_created_at;
\echo '  ✓ 已删除 idx_session_events_created_at'

-- 删除组合索引 (session_id, created_at)
DROP INDEX IF EXISTS idx_session_events_session_created;
\echo '  ✓ 已删除 idx_session_events_session_created'

-- ============================================================================
-- Sessions 表索引回滚
-- ============================================================================

\echo ''
\echo '🗂️ Sessions 表索引回滚...'

-- 删除 thread_id 索引
DROP INDEX IF EXISTS idx_sessions_thread_id;
\echo '  ✓ 已删除 idx_sessions_thread_id'

-- 删除 created_at 索引
DROP INDEX IF EXISTS idx_sessions_created_at;
\echo '  ✓ 已删除 idx_sessions_created_at'

-- 删除 status 索引
DROP INDEX IF EXISTS idx_sessions_status;
\echo '  ✓ 已删除 idx_sessions_status'

-- ============================================================================
-- 验证回滚结果
-- ============================================================================

\echo ''
\echo '================================================'
\echo '验证回滚结果...'
\echo '================================================'

-- 统计剩余索引数量
SELECT 
    schemaname,
    tablename,
    COUNT(*) as remaining_indexes
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename IN ('papers', 'reports', 'session_events', 'sessions')
GROUP BY schemaname, tablename
ORDER BY tablename;

\echo ''
\echo '预期结果:'
\echo '  - Papers: 基础索引（主键、外键）'
\echo '  - Reports: 基础索引（主键、外键）'
\echo '  - Session Events: 基础索引（主键、外键）'
\echo '  - Sessions: 基础索引（主键）'
\echo ''

-- 详细列出剩余索引
\echo '剩余索引详情:'
SELECT 
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename IN ('papers', 'reports', 'session_events', 'sessions')
ORDER BY tablename, indexname;

-- ============================================================================
-- 性能影响评估
-- ============================================================================

\echo ''
\echo '================================================'
\echo '⚠️ 性能影响评估'
\echo '================================================'
\echo ''
\echo '回滚后预期性能变化:'
\echo '  - 查询速度: 降低 30-40%'
\echo '  - Papers查询: 无session_id索引，全表扫描'
\echo '  - Reports查询: 无version索引，排序变慢'
\echo '  - Events查询: 无时间索引，时间线生成变慢'
\echo '  - Session列表: 无status索引，过滤变慢'
\echo ''
\echo '适用场景:'
\echo '  ✓ 索引导致写入性能下降'
\echo '  ✓ 存储空间不足'
\echo '  ✓ 降级到旧版本'
\echo '  ✗ 生产环境（不推荐）'
\echo ''

-- ============================================================================
-- 完成消息
-- ============================================================================

\echo '================================================'
\echo '✅ 索引回滚完成！'
\echo '================================================'
\echo ''
\echo '已删除索引:'
\echo '  - Papers: 3 个索引'
\echo '  - Reports: 2 个索引'
\echo '  - Session Events: 4 个索引'
\echo '  - Sessions: 3 个索引'
\echo '  总计: 12 个性能优化索引'
\echo ''
\echo '后续操作:'
\echo '  1. 重启应用服务: docker-compose restart langgraph-api'
\echo '  2. 监控查询性能: 观察慢查询日志'
\echo '  3. 如需恢复: 执行 001_add_indexes.sql'
\echo ''
\echo '文档参考:'
\echo '  - backend/migrations/001_add_indexes.sql'
\echo '  - .ai-sessions/development/PHASE_3.5.4_COMPLETION_SUMMARY.md'
\echo ''

-- ============================================================================
-- 回滚历史记录（可选）
-- ============================================================================

-- 如果有migration_history表，记录回滚操作
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'migration_history') THEN
        INSERT INTO migration_history (migration_name, applied_at, rollback_at, notes)
        VALUES (
            '001_add_indexes',
            (SELECT applied_at FROM migration_history WHERE migration_name = '001_add_indexes' ORDER BY applied_at DESC LIMIT 1),
            NOW(),
            'Rollback executed: removed 12 performance indexes'
        );
        \echo '已记录回滚历史到 migration_history 表'
    END IF;
END $$;

\echo ''
\echo '🔚 脚本执行完毕'
\echo ''
