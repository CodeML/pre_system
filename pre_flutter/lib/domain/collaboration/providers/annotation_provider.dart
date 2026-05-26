import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../repository/annotation_repository.dart';
import '../../../core/annotation_engine/annotation_model.dart';
import '../../../core/network/api_client.dart';

final annotationRepositoryProvider = Provider((ref) {
  final dio = ref.watch(apiClientProvider);
  return AnnotationRepository(dio);
});

// 1. 基础数据拉取
final annotationListProvider = FutureProvider.family<List<AnnotationEntity>, String>((ref, targetId) async {
  final repo = ref.watch(annotationRepositoryProvider);
  return repo.getAnnotations("file", targetId);
});

// 2. 状态变更控制器 (处理业务逻辑)
class AnnotationController {
  final Ref ref;
  final String targetId;

  AnnotationController(this.ref, this.targetId);

  Future<void> addAnnotation(AnnotationEntity item) async {
    final repo = ref.read(annotationRepositoryProvider);
    try {
      await repo.createAnnotation(item);
      ref.invalidate(annotationListProvider(targetId));
    } catch (e) {
      rethrow;
    }
  }

  Future<void> resolve(String id) async {
    final repo = ref.read(annotationRepositoryProvider);
    try {
      await repo.updateStatus(id, AnnotationStatus.resolved);
      ref.invalidate(annotationListProvider(targetId));
    } catch (e) {
      rethrow;
    }
  }
}

final annotationControllerProvider = Provider.family<AnnotationController, String>((ref, targetId) {
  return AnnotationController(ref, targetId);
});
