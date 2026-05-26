import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:vector_math/vector_math_64.dart' as v64;
import '../../core/annotation_engine/annotation_model.dart';
import '../../core/annotation_engine/annotation_painter.dart';
import '../../core/annotation_engine/viewport_provider.dart';
import '../../domain/collaboration/providers/annotation_provider.dart';
import 'widgets/client_comment_panel.dart';
import 'widgets/final_confirmation_dialog.dart';
import '../widgets/logout_button.dart';

class ClientWorkspace extends ConsumerStatefulWidget {
  final String fileId;
  const ClientWorkspace({super.key, this.fileId = "101"});

  @override
  ConsumerState<ClientWorkspace> createState() => _ClientWorkspaceState();
}

class _ClientWorkspaceState extends ConsumerState<ClientWorkspace> {
  final TransformationController _transformationController = TransformationController();
  AnnotationType _currentTool = AnnotationType.point;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final annotationsAsync = ref.watch(annotationListProvider(widget.fileId));
    final viewport = ref.watch(viewportProvider);
    final selectedId = ref.watch(selectedAnnotationProvider);

    return Scaffold(
      backgroundColor: const Color(0xFFF9FAFB),
      appBar: _buildClientAppBar(context),
      body: Row(
        children: [
          // 核心看稿与批注区 (无文件树，极简)
          Expanded(
            child: Column(
              children: [
                _buildSimpleToolbar(),
                Expanded(
                  child: annotationsAsync.when(
                      data: (annotations) => _buildCanvas(annotations, selectedId, viewport),
                      loading: () => const Center(child: CircularProgressIndicator()),
                      error: (e, _) => Center(child: Text("加载失败: $e")),
                  ),
                ),
              ],
            ),
          ),
          
          // 对话式评论区
          ClientCommentPanel(
            fileId: widget.fileId,
            annotations: annotationsAsync.value ?? [],
            selectedId: selectedId,
          ),
        ],
      ),
    );
  }

  PreferredSizeWidget _buildClientAppBar(BuildContext context) {
    return AppBar(
      backgroundColor: Colors.white,
      elevation: 0,
      bottom: PreferredSize(
        preferredSize: const Size.fromHeight(1.0),
        child: Container(color: const Color(0xFFE5E7EB), height: 1.0),
      ),
      title: const Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text("双11大促主视觉海报", style: TextStyle(color: Colors.black87, fontSize: 16, fontWeight: FontWeight.bold)),
          Text("第 2 轮修改 · 待客户确认", style: TextStyle(color: Colors.blue, fontSize: 12)),
        ],
      ),
      actions: [
        Padding(
          padding: const EdgeInsets.symmetric(vertical: 8),
          child: ElevatedButton.icon(
            onPressed: () => _showConfirmationDialog(context),
            icon: const Icon(Icons.verified),
            label: const Text("确认终稿", style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF10B981),
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
            ),
          ),
        ),
        const SizedBox(width: 8),
        const LogoutButton(),
        const SizedBox(width: 16),
      ],
    );
  }

  Widget _buildSimpleToolbar() {
    return Container(
      height: 48,
      padding: const EdgeInsets.symmetric(horizontal: 16),
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(bottom: BorderSide(color: Color(0xFFE5E7EB))),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text("批注工具：", style: TextStyle(color: Colors.grey)),
          _buildToolBtn(AnnotationType.point, Icons.location_on, "标记点"),
          _buildToolBtn(AnnotationType.rect, Icons.crop_din, "框选区域"),
          const VerticalDivider(width: 32),
          IconButton(icon: const Icon(Icons.zoom_in, color: Colors.black54), onPressed: () {}),
          IconButton(icon: const Icon(Icons.zoom_out, color: Colors.black54), onPressed: () {}),
        ],
      ),
    );
  }

  Widget _buildToolBtn(AnnotationType type, IconData icon, String tooltip) {
    final isSelected = _currentTool == type;
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 4),
      child: ActionChip(
        avatar: Icon(icon, size: 16, color: isSelected ? Colors.white : Colors.black54),
        label: Text(tooltip),
        backgroundColor: isSelected ? Colors.blue : Colors.grey[100],
        labelStyle: TextStyle(color: isSelected ? Colors.white : Colors.black87),
        onPressed: () => setState(() => _currentTool = type),
      ),
    );
  }

  Widget _buildCanvas(List<AnnotationEntity> annotations, String? selectedId, ViewportState viewport) {
    return ClipRect(
      child: GestureDetector(
        onTapUp: _handleCanvasTap,
        child: InteractiveViewer(
          transformationController: _transformationController,
          boundaryMargin: const EdgeInsets.all(1000),
          minScale: 0.1,
          maxScale: 10.0,
          onInteractionUpdate: (details) {
            final matrix = _transformationController.value;
            final v64.Vector3 translation = matrix.getTranslation();
            ref.read(viewportProvider.notifier).updateTransform(
              matrix.getMaxScaleOnAxis(),
              Offset(translation.x, translation.y),
            );
          },
          child: Stack(
            children: [
              Center(child: Image.network("https://via.placeholder.com/1920x1080")),
              Positioned.fill(
                child: CustomPaint(
                  painter: AnnotationPainter(
                    annotations: annotations,
                    selectedId: selectedId,
                    scale: viewport.scale,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _handleCanvasTap(TapUpDetails details) {
    final RenderBox box = context.findRenderObject() as RenderBox;
    final Offset local = box.globalToLocal(details.globalPosition);
    final nx = local.dx / box.size.width;
    final ny = (local.dy - (kToolbarHeight + 48)) / (box.size.height - (kToolbarHeight + 48));
    
    final newId = "temp_${DateTime.now().millisecondsSinceEpoch}";
    final newAnn = AnnotationEntity(
        id: newId,
        targetId: widget.fileId,
        targetType: "file",
        content: "客户意见...",
        type: _currentTool,
        normalizedRect: _currentTool == AnnotationType.rect 
            ? Rect.fromLTWH(nx, ny, 0.05, 0.05) 
            : Rect.fromLTWH(nx, ny, 0, 0),
        createdAt: DateTime.now(),
        createdBy: "client_1",
    );
    
    ref.read(annotationControllerProvider(widget.fileId)).addAnnotation(newAnn);
    ref.read(selectedAnnotationProvider.notifier).select(newId);
  }

  void _showConfirmationDialog(BuildContext context) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => const FinalConfirmationDialog(),
    );
  }
}
