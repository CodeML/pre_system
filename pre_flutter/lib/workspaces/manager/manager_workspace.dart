import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../domain/dashboard/providers/dashboard_provider.dart';
import '../../domain/finance/providers/finance_provider.dart';
import 'widgets/metric_card.dart';
import 'widgets/risk_alert_panel.dart';
import 'widgets/team_workload_panel.dart';
import '../widgets/logout_button.dart';

class ManagerWorkspace extends ConsumerWidget {
  const ManagerWorkspace({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final overviewAsync = ref.watch(dashboardOverviewProvider);
    final riskAlertsAsync = ref.watch(riskAlertsProvider);
    final capacityAsync = ref.watch(teamCapacityProvider);

    return Scaffold(
      backgroundColor: const Color(0xFFF9FAFB),
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        title: const Text(
          "PRE 系统经营驾驶舱",
          style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh, color: Colors.blue),
            onPressed: () {
              ref.invalidate(dashboardOverviewProvider);
              ref.invalidate(riskAlertsProvider);
              ref.invalidate(teamCapacityProvider);
            },
          ),
          const SizedBox(width: 8),
          const CircleAvatar(radius: 16, child: Icon(Icons.person, size: 20)),
          const SizedBox(width: 8),
          const LogoutButton(),
          const SizedBox(width: 20),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(32),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 1. 关键指标行
            overviewAsync.when(
              data: (data) => _buildMetricsRow(data),
              loading: () => const LinearProgressIndicator(),
              error: (e, _) => Text("概览数据加载失败: $e"),
            ),
            
            const SizedBox(height: 32),
            
            // 2. 核心图表与风险行
            IntrinsicHeight(
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // 左侧：团队负荷
                  Expanded(
                    flex: 1,
                    child: capacityAsync.when(
                      data: (data) => TeamWorkloadPanel(capacity: data),
                      loading: () => const Center(child: CircularProgressIndicator()),
                      error: (e, _) => Text("负荷数据加载失败: $e"),
                    ),
                  ),
                  const SizedBox(width: 32),
                  // 右侧：风险预警
                  Expanded(
                    flex: 1,
                    child: riskAlertsAsync.when(
                      data: (data) => RiskAlertPanel(alerts: data),
                      loading: () => const Center(child: CircularProgressIndicator()),
                      error: (e, _) => Text("风险数据加载失败: $e"),
                    ),
                  ),
                ],
              ),
            ),
            
            const SizedBox(height: 32),
            
            // 3. 最近项目动态（占位）
            _buildRecentProjectsSection(),
          ],
        ),
      ),
    );
  }

  Widget _buildMetricsRow(Map<String, dynamic> data) {
    return Row(
      children: [
        Expanded(
          child: MetricCard(
            title: "进行中项目",
            value: "${data['active_projects'] ?? 0}",
            icon: Icons.assignment_rounded,
            color: Colors.blue,
            trend: "+2 本周",
          ),
        ),
        const SizedBox(width: 24),
        Expanded(
          child: MetricCard(
            title: "待审核任务",
            value: "${data['pending_tasks'] ?? 0}",
            icon: Icons.rate_review_rounded,
            color: Colors.orange,
            trend: "需加急 3",
          ),
        ),
        const SizedBox(width: 24),
        Expanded(
          child: const MetricCard(
            title: "本月毛利率",
            value: "32.5%",
            icon: Icons.account_balance_wallet_rounded,
            color: Colors.green,
            trend: "+5% 环比",
          ),
        ),
        const SizedBox(width: 24),
        Expanded(
          child: const MetricCard(
            title: "平均改稿轮次",
            value: "2.4",
            icon: Icons.history_rounded,
            color: Colors.purple,
            trend: "-0.2 优化",
          ),
        ),
      ],
    );
  }

  Widget _buildRecentProjectsSection() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey.withValues(alpha: 0.1)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            "重点项目实时动态",
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 20),
          ListView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: 3,
            itemBuilder: (context, index) {
              return ListTile(
                leading: const CircleAvatar(backgroundColor: Colors.blue, child: Icon(Icons.folder, color: Colors.white, size: 16)),
                title: Text("电商主图设计 A_${index + 1}"),
                subtitle: const Text("最后更新于 10 分钟前"),
                trailing: const Icon(Icons.chevron_right),
                onTap: () {},
              );
            },
          ),
        ],
      ),
    );
  }
}
