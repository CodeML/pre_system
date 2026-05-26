import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../auth/auth_manager.dart';

final apiClientProvider = Provider((ref) {
  final dio = Dio(BaseOptions(
    baseUrl: const String.fromEnvironment('API_BASE_URL', defaultValue: 'http://127.0.0.1:8000/api'),
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
    contentType: 'application/json',
  ));

  dio.interceptors.add(InterceptorsWrapper(
    onRequest: (options, handler) async {
      final auth = ref.read(authProvider);
      if (auth.token != null) {
        options.headers['Authorization'] = 'Bearer ${auth.token}';
      }
      return handler.next(options);
    },
    onResponse: (response, handler) {
      final data = response.data;
      if (data is Map<String, dynamic>) {
        if (data.containsKey('code') && data['code'] != 200) {
           throw DioException(
             requestOptions: response.requestOptions,
             response: response,
             message: data['message'] ?? '业务异常',
           );
        }
        response.data = data['data'] ?? data;
      }
      return handler.next(response);
    },
    onError: (DioException e, handler) {
      if (e.response?.statusCode == 401) {
        ref.read(authProvider.notifier).logout();
      }
      return handler.next(e);
    },
  ));
  
  if (kDebugMode) {
    dio.interceptors.add(LogInterceptor(responseBody: true, requestBody: true));
  }

  return dio;
});
