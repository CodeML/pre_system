import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/auth/auth_manager.dart';

class LogoutButton extends ConsumerWidget {
  final Color? color;
  const LogoutButton({super.key, this.color});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return IconButton(
      icon: Icon(Icons.logout_rounded, color: color ?? Colors.redAccent),
      tooltip: "退出系统",
      onPressed: () async {
        final confirm = await showDialog<bool>(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text("确认退出"),
            content: const Text("是否确认退出当前账号？"),
            actions: [
              TextButton(onPressed: () => Navigator.pop(context, false), child: const Text("取消")),
              TextButton(
                onPressed: () => Navigator.pop(context, true), 
                child: const Text("确认退出", style: TextStyle(color: Colors.red)),
              ),
            ],
          ),
        );

        if (confirm == true) {
          await ref.read(authProvider.notifier).logout();
        }
      },
    );
  }
}
