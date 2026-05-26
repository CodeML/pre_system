import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/state/workspace_state.dart';
import '../../domain/task_flow/providers/task_provider.dart';
import 'file_review_page.dart';
import '../widgets/logout_button.dart';

class DesignerWorkspace extends ConsumerWidget {
  const DesignerWorkspace({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final workspace = ref.watch(workspaceProvider);
    final taskQueueAsync = ref.watch(taskQueueProvider);

    return Scaffold(
      backgroundColor: const Color(0xFFF0F2F5),
      body: Row(
        children: [
          // 1. 左侧任务队列 (Work Queue)
          if (workspace.isTaskQueueOpen)
            _buildTaskQueue(ref, taskQueueAsync, workspace.currentTaskId),
          
          // 2. 中间主工作区
          Expanded(
            child: workspace.currentTaskId == null 
              ? Scaffold(
                  appBar: AppBar(
                    title: const Text("请选择任务"),
                    actions: const [LogoutButton(), SizedBox(width: 16)],
                  ),
                  body: const Center(child: Text("请从左侧选择一个任务开始生产")),
                )
              : FileReviewPage(fileId: workspace.currentFileId ?? "1"),
          ),
        ],
      ),
    );
  }

  Widget _buildTaskQueue(WidgetRef ref, AsyncValue<List<Map<String, dynamic>>> tasksAsync, String? selectedId) {
    return Container(
      width: 300,
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(right: BorderSide(color: Color(0xFFE0E0E0))),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.all(20),
            child: Row(
              children: [
                const Icon(Icons.list_alt, color: Colors.blue),
                const SizedBox(width: 8),
                const Text("我的生产队列", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                const Spacer(),
                if (selectedId != null) const LogoutButton(),
              ],
            ),
          ),
          Expanded(
            child: tasksAsync.when(
              data: (tasks) => ListView.builder(
                itemCount: tasks.length,
                itemBuilder: (context, index) {
                  final task = tasks[index];
                  final isSelected = task['id'].toString() == selectedId;
                  return _buildTaskItem(ref, task, isSelected);
                },
              ),
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (e, _) => Center(child: Text("加载失败: $e")),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTaskItem(WidgetRef ref, Map<String, dynamic> task, bool isSelected) {
    return ListTile(
      selected: isSelected,
      selectedTileColor: Colors.blue.withValues(alpha: 0.05),
      leading: _getStatusIcon(task['status']),
      title: Text(task['name'] ?? "未命名任务", style: const TextStyle(fontWeight: FontWeight.w600)),
      subtitle: Text("项目: ${task['project_name'] ?? '未知'}"),
      onTap: () {
        final taskId = task['id'].toString();
        ref.read(workspaceProvider.notifier).selectTask(taskId);
        ref.read(workspaceProvider.notifier).selectFile("101");
      },
    );
  }

  Widget _getStatusIcon(String? status) {
    switch (status) {
      case '设计中': return const Icon(Icons.edit_note, color: Colors.orange, size: 20);
      case '内审中': return const Icon(Icons.fact_check, color: Colors.blue, size: 20);
      case '已完成': return const Icon(Icons.check_circle, color: Colors.green, size: 20);
      default: return const Icon(Icons.circle_outlined, color: Colors.grey, size: 20);
    }
  }
}
