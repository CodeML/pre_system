import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/network/api_client.dart';

class AuthRepository {
  final Dio _dio;
  AuthRepository(this._dio);

  Future<Map<String, dynamic>> login(String username, String password) async {
    final formData = FormData.fromMap({
      'username': username,
      'password': password,
    });
    
    final response = await _dio.post('/user/login', data: formData);
    return response.data;
  }
}

final authRepositoryProvider = Provider((ref) {
  final dio = ref.watch(apiClientProvider);
  return AuthRepository(dio);
});
