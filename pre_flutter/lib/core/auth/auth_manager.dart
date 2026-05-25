import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AuthManager extends ChangeNotifier {
  static late SharedPreferences _prefs;
  bool _isLoggedIn = false;
  String? _token;
  String? _userId;

  bool get isLoggedIn => _isLoggedIn;
  String? get token => _token;
  String? get userId => _userId;

  // 初始化本地存储
  static Future<void> init() async {
    _prefs = await SharedPreferences.getInstance();
  }

  // 登录
  Future<void> login(String token, String userId) async {
    _token = token;
    _userId = userId;
    _isLoggedIn = true;

    await _prefs.setString('token', token);
    await _prefs.setString('userId', userId);
    await _prefs.setBool('isLoggedIn', true);

    notifyListeners();
  }

  // 登出
  Future<void> logout() async {
    _token = null;
    _userId = null;
    _isLoggedIn = false;

    await _prefs.remove('token');
    await _prefs.remove('userId');
    await _prefs.remove('isLoggedIn');

    notifyListeners();
  }

  // 恢复登录状态
  Future<void> restoreLoginState() async {
    _isLoggedIn = _prefs.getBool('isLoggedIn') ?? false;
    _token = _prefs.getString('token');
    _userId = _prefs.getString('userId');
    notifyListeners();
  }
}
