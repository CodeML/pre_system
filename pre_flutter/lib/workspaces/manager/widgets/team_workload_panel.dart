import 'package:flutter/material.dart';

class TeamWorkloadPanel extends StatelessWidget {
  final Map<String, dynamic> capacity;

  const TeamWorkloadPanel({super.key, required this.capacity});

  @override
  Widget build(BuildContext context) {
    final List<dynamic> details = capacity['details'] ?? [];

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
          Row(
            children: [
              const Icon(Icons.people_alt_rounded, color: Colors.blue),
              const SizedBox(width: 8),
              const Text(
                "团队生产负荷",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const Spacer(),
              Text(
                "${capacity['current_load']}%",
                style: TextStyle(
                  color: _getLoadColor(capacity['current_load'] as int? ?? 0),
                  fontWeight: FontWeight.bold,
                  fontSize: 20,
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          Expanded(
            child: ListView.builder(
              itemCount: details.length,
              itemBuilder: (context, index) {
                final item = details[index];
                final loadStr = (item['load'] as String).replaceAll('%', '');
                final loadVal = double.tryParse(loadStr) ?? 0;

                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 12),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(item['designer'] ?? "未知", style: const TextStyle(fontWeight: FontWeight.w600)),
                          Text("${item['load']}"),
                        ],
                      ),
                      const SizedBox(height: 8),
                      LinearProgressIndicator(
                        value: loadVal / 100,
                        backgroundColor: Colors.grey[100],
                        color: _getLoadColor(loadVal.toInt()),
                        minHeight: 6,
                        borderRadius: BorderRadius.circular(3),
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Color _getLoadColor(int load) {
    if (load > 90) return Colors.red;
    if (load > 70) return Colors.orange;
    return Colors.blue;
  }
}
