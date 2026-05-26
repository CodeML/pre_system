import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class AuthState {
  final String? token;
  final List<String> permissions;
  final List<String> roles;
  final int? orgId;
  final String? currentRole;

  AuthState({
    this.token,
    this.permissions = const [],
    this.roles = const [],
    this.orgId,
    this.currentRole,
  });

  AuthState copyWith({
    String? token,
    List<String>? permissions,
    List<String>? roles,
    int? orgId,
    String? currentRole,
  }) {
    return AuthState(
      token: token ?? this.token,
      permissions: permissions ?? this.permissions,
      roles: roles ?? this.roles,
      orgId: orgId ?? this.orgId,
      currentRole: currentRole ?? this.currentRole,
    );
  }
}

class AuthNotifier extends Notifier<AuthState> {
  static late SharedPreferences _prefs;

  static Future<void> init() async {
    _prefs = await SharedPreferences.getInstance();
  }

  @override
  AuthState build() {
    final token = _prefs.getString('token');
    final perms = _prefs.getStringList('permissions') ?? [];
    final roles = _prefs.getStringList('roles') ?? [];
    final orgId = _prefs.getInt('orgId');
    final currentRole = _prefs.getString('currentRole');

    return AuthState(
      token: token,
      permissions: perms,
      roles: roles,
      orgId: orgId,
      currentRole: currentRole,
    );
  }

  Future<void> login(String newToken, List<String> perms, List<String> roles, int orgId) async {
    await _prefs.setString('token', newToken);
    await _prefs.setStringList('permissions', perms);
    await _prefs.setStringList('roles', roles);
    await _prefs.setInt('orgId', orgId);
    
    String? role;
    if (roles.isNotEmpty) {
      role = roles.first;
      await _prefs.setString('currentRole', role);
    }

    state = state.copyWith(
      token: newToken,
      permissions: perms,
      roles: roles,
      orgId: orgId,
      currentRole: role,
    );
  }

  Future<void> logout() async {
    await _prefs.remove('token');
    await _prefs.remove('permissions');
    await _prefs.remove('roles');
    await _prefs.remove('orgId');
    await _prefs.remove('currentRole');
    
    state = AuthState();
  }

  bool hasPermission(String code) {
    if (state.permissions.contains('system:admin')) return true;
    return state.permissions.contains(code);
  }
}

final authProvider = NotifierProvider<AuthNotifier, AuthState>(() {
  return AuthNotifier();
});
