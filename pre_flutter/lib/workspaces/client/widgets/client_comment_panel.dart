import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/annotation_engine/annotation_model.dart';

class ClientCommentPanel extends ConsumerWidget {
  final String fileId;
  final List<AnnotationEntity> annotations;
  final String? selectedId;

  const ClientCommentPanel({
    super.key,
    required this.fileId,
    required this.annotations,
    this.selectedId,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Container(
      width: 350,
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(left: BorderSide(color: Color(0xFFE5E7EB))),
      ),
      child: Column(
        children: [
          const Padding(
            padding: EdgeInsets.all(16),
            child: Row(
              children: [
                Icon(Icons.forum_outlined, color: Colors.blue),
                SizedBox(width: 8),
                Text("修改意见", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              ],
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: annotations.length,
              itemBuilder: (context, index) {
                final ann = annotations[index];
                return _buildSimpleCommentCard(ann, ann.id == selectedId);
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSimpleCommentCard(AnnotationEntity ann, bool isSelected) {
    final isResolved = ann.status == AnnotationStatus.resolved;
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      elevation: 0,
      color: isSelected ? Colors.blue[50] : Colors.white,
      shape: RoundedRectangleBorder(
        side: BorderSide(color: isSelected ? Colors.blue : const Color(0xFFE5E7EB)),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                CircleAvatar(
                  radius: 12,
                  backgroundColor: ann.createdBy == 'me' ? Colors.blue : Colors.grey[200],
                  child: Text(
                    ann.createdBy.isNotEmpty ? ann.createdBy[0].toUpperCase() : 'U', 
                    style: TextStyle(fontSize: 10, color: ann.createdBy == 'me' ? Colors.white : Colors.black)
                  ),
                ),
                const SizedBox(width: 8),
                Text(ann.createdBy == 'me' ? "我" : "设计师", style: const TextStyle(fontWeight: FontWeight.bold)),
                const Spacer(),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: isResolved ? Colors.green[50] : Colors.orange[50],
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    isResolved ? "已处理" : "待处理",
                    style: TextStyle(
                      color: isResolved ? Colors.green[700] : Colors.orange[700],
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text(ann.content, style: const TextStyle(fontSize: 14, height: 1.5)),
            // 极简设计：客户不需要看到复杂的内部工程状态按钮
          ],
        ),
      ),
    );
  }
}
