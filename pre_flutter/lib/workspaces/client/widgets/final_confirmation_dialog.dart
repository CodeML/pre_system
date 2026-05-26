import 'package:flutter/material.dart';

class FinalConfirmationDialog extends StatelessWidget {
  const FinalConfirmationDialog({super.key});

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Row(
        children: [
          Icon(Icons.gavel, color: Colors.orange),
          SizedBox(width: 8),
          Text("确认终稿并锁定"),
        ],
      ),
      content: const SizedBox(
        width: 400,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("确认后，该设计稿将进入【最终交付】状态。", style: TextStyle(fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            Text("• 系统将自动生成不可篡改的交付快照。"),
            Text("• 锁定后将无法再发起任何修改意见。"),
            Text("• 此操作将作为项目阶段结算的法律依据。"),
            SizedBox(height: 16),
            Text("请输入您的姓名（电子签名）：", style: TextStyle(color: Colors.grey)),
            SizedBox(height: 8),
            TextField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                hintText: "如：张三",
                isDense: true,
              ),
            ),
          ],
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text("再看看", style: TextStyle(color: Colors.grey)),
        ),
        ElevatedButton(
          onPressed: () {
            // TODO: 调用后端 Lock 接口
            Navigator.of(context).pop();
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text("已确认终稿，文件已锁定。")),
            );
          },
          style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF10B981), foregroundColor: Colors.white),
          child: const Text("我已确认无误，签名并锁定"),
        ),
      ],
    );
  }
}
