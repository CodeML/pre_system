import 'package:flutter/material.dart';

class RiskAlertPanel extends StatelessWidget {
  final List<dynamic> alerts;

  const RiskAlertPanel({super.key, required this.alerts});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey.withValues(alpha: 0.1)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.warning_amber_rounded, color: Colors.red),
              SizedBox(width: 8),
              Text(
                "异常与风险预警",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
            ],
          ),
          const SizedBox(height: 20),
          if (alerts.isEmpty)
            const Expanded(
              child: Center(child: Text("暂无风险项", style: TextStyle(color: Colors.grey))),
            )
          else
            Expanded(
              child: ListView.separated(
                itemCount: alerts.length,
                separatorBuilder: (context, index) => const Divider(),
                itemBuilder: (context, index) {
                  final alert = alerts[index];
                  return ListTile(
                    contentPadding: EdgeInsets.zero,
                    title: Text(alert['project_name'] ?? "未知项目", style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Text(alert['reason'] ?? "预算超出警戒线"),
                    trailing: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: Colors.red[50],
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: Text(
                        "高风险",
                        style: TextStyle(color: Colors.red[700], fontSize: 12, fontWeight: FontWeight.bold),
                      ),
                    ),
                  );
                },
              ),
            ),
        ],
      ),
    );
  }
}
