import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_easyloading/flutter_easyloading.dart';
import '../../core/auth/auth_manager.dart';
import '../../domain/auth/repository/auth_repository.dart';

class LoginPage extends ConsumerStatefulWidget {
  const LoginPage({super.key});

  @override
  ConsumerState<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends ConsumerState<LoginPage> {
  final _usernameController = TextEditingController(text: "admin");
  final _passwordController = TextEditingController(text: "123456");

  Future<void> _handleLogin() async {
    EasyLoading.show(status: '正在登录...');
    try {
      final authRepo = ref.read(authRepositoryProvider);
      final res = await authRepo.login(
        _usernameController.text,
        _passwordController.text,
      );
      
      final token = res['access_token'];
      final perms = List<String>.from(res['permissions'] ?? []);
      final roles = List<String>.from(res['roles'] ?? []);
      final orgId = res['org_id'] as int;

      await ref.read(authProvider.notifier).login(token, perms, roles, orgId);
      EasyLoading.showSuccess('欢迎回来');
    } catch (e) {
      EasyLoading.showError('登录失败: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          width: 400,
          padding: const EdgeInsets.all(32),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
            boxShadow: [
              BoxShadow(color: Colors.black.withValues(alpha: 0.05), blurRadius: 20, spreadRadius: 5)
            ],
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.architecture, size: 64, color: Colors.blue),
              const SizedBox(height: 16),
              const Text(
                "Design Production OS",
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 32),
              TextField(
                controller: _usernameController,
                decoration: const InputDecoration(
                  labelText: "用户名",
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.person),
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _passwordController,
                obscureText: true,
                decoration: const InputDecoration(
                  labelText: "密码",
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.lock),
                ),
              ),
              const SizedBox(height: 32),
              SizedBox(
                width: double.infinity,
                height: 48,
                child: ElevatedButton(
                  onPressed: _handleLogin,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                    foregroundColor: Colors.white,
                  ),
                  child: const Text("立即进入系统"),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
