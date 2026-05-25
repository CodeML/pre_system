import "package:flutter/material.dart";
import "package:flutter_easyloading/flutter_easyloading.dart";
import 'routes/app_routes.dart';
import 'routes/route_generator.dart';
import 'core/constants/color_constants.dart';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '设计工作室PRE系统',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: ColorConstants.primaryColor),
        visualDensity: VisualDensity.adaptivePlatformDensity,
        useMaterial3: true,
      ),
      initialRoute: AppRoutes.login,
      onGenerateRoute: RouteGenerator.generateRoute,
      builder: EasyLoading.init(),
      debugShowCheckedModeBanner: false,
    );
  }
}
