import 'package:flutter/material.dart';
import 'annotation_model.dart';

class AnnotationPainter extends CustomPainter {
  final List<AnnotationEntity> annotations;
  final String? selectedId;
  final double scale;

  AnnotationPainter({required this.annotations, this.selectedId, required this.scale});

  @override
  void paint(Canvas canvas, Size size) {
    for (final item in annotations) {
      if (item.status == AnnotationStatus.ignored) continue;

      final isSelected = item.id == selectedId;
      final isResolved = item.status == AnnotationStatus.resolved;
      
      final baseOpacity = isResolved ? 0.3 : 1.0;
      final color = _getStatusColor(item.status);

      // 使用 withValues 适配新版本
      final paint = Paint()
        ..color = color.withValues(alpha: isSelected ? 1.0 : baseOpacity * 0.7)
        ..style = PaintingStyle.stroke
        ..strokeWidth = (isSelected ? 3.0 : 2.0) / scale;

      final fillPaint = Paint()
        ..color = color.withValues(alpha: isSelected ? 0.4 : baseOpacity * 0.2)
        ..style = PaintingStyle.fill;

      final pos = Offset(item.x * size.width, item.y * size.height);

      if (item.type == AnnotationType.point) {
        _drawPoint(canvas, pos, paint, isSelected, scale, isResolved);
      } else if (item.type == AnnotationType.rect) {
        final rect = Rect.fromLTWH(
          pos.dx, pos.dy, 
          item.normalizedRect.width * size.width, 
          item.normalizedRect.height * size.height
        );
        canvas.drawRect(rect, fillPaint);
        canvas.drawRect(rect, paint);
      }
    }
  }

  void _drawPoint(Canvas canvas, Offset pos, Paint paint, bool isSelected, double scale, bool isResolved) {
    final radius = (isSelected ? 10.0 : 8.0) / scale;
    canvas.drawCircle(pos, radius, paint..style = PaintingStyle.fill);
    canvas.drawCircle(pos, radius + 2/scale, paint..style = PaintingStyle.stroke);
    
    if (isResolved) {
      final checkPaint = Paint()
        ..color = Colors.white.withValues(alpha: 0.8)
        ..style = PaintingStyle.stroke
        ..strokeWidth = 1.5 / scale;
      canvas.drawLine(pos + Offset(-3/scale, 0), pos + Offset(-1/scale, 3/scale), checkPaint);
      canvas.drawLine(pos + Offset(-1/scale, 3/scale), pos + Offset(4/scale, -3/scale), checkPaint);
    }
  }

  Color _getStatusColor(AnnotationStatus status) {
    switch (status) {
      case AnnotationStatus.open: return Colors.red;
      case AnnotationStatus.resolved: return Colors.green;
      case AnnotationStatus.ignored: return Colors.grey;
      case AnnotationStatus.reopened: return Colors.orange;
    }
  }

  @override
  bool shouldRepaint(covariant AnnotationPainter oldDelegate) => true; 
}
