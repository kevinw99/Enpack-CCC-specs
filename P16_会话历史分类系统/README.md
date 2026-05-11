# Moved

会话历史分类系统的规格已迁移到 base 仓库：

→ **`base/specs/02_session-history-classification/`** (https://github.com/kevinw99/ai-project-base/tree/main/specs/02_session-history-classification)

源代码同步在 `base/src/session_history/`，此前 CCC 仓库的 `源代码/session_history/` 也是该工具的副本。

迁移日期：2026-05-11
原因：该工具已下沉到 base 共享仓库，所有项目（CCC / CBBO / AI-ALL / LeapBoundAI）通过 `git pull base` 复用同一份实现，规格也应跟随源码归位。
