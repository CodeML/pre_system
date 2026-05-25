import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:flutter_easyloading/flutter_easyloading.dart';
import 'core/auth/auth_manager.dart';
import 'routes/app_routes.dart';
import 'routes/route_generator.dart';
import 'app.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // 初始化本地存储
  await AuthManager.init();

  final authManager = AuthManager();
  await authManager.restoreLoginState();

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider<AuthManager>(create: (_) => authManager),
      ],
      child: const MyApp(),
    ),
  );
  // 配置EasyLoading
  configLoading();
}

void configLoading() {
  EasyLoading.instance
    ..displayDuration = const Duration(milliseconds: 2000)
    ..indicatorType = EasyLoadingIndicatorType.fadingCircle
    ..loadingStyle = EasyLoadingStyle.dark
    ..maskType = EasyLoadingMaskType.clear;
}
