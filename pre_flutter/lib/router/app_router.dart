import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../core/auth/auth_manager.dart';
import '../workspaces/designer/designer_workspace.dart';
import '../workspaces/manager/manager_workspace.dart';
import '../workspaces/admin/login_page.dart';

// Placeholder Pages
class ClientWorkspace extends StatelessWidget { const ClientWorkspace({super.key}); @override Widget build(BuildContext context) => const Scaffold(body: Center(child: Text("Client Workspace"))); }

final routerProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authProvider);

  return GoRouter(
    initialLocation: '/workspace',
    redirect: (context, state) {
      final isLoggedIn = authState.token != null;
      final isGoingToLogin = state.matchedLocation == '/login';

      if (!isLoggedIn && !isGoingToLogin) return '/login';
      if (isLoggedIn && isGoingToLogin) return '/workspace';
      
      return null;
    },
    routes: [
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginPage(),
      ),
      GoRoute(
        path: '/workspace',
        builder: (context, state) {
          final role = authState.currentRole;
          
          switch (role) {
            case 'leader':
            case 'finance':
            case 'super_admin':
              return const ManagerWorkspace();
            case 'user':
              return const ClientWorkspace();
            case 'executor':
            default:
              return const DesignerWorkspace();
          }
        },
      ),
    ],
  );
});
