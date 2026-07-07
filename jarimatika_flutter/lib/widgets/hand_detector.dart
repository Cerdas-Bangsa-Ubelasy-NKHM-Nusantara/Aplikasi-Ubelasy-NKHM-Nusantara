import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import '../services/hand_detection_service.dart';

class HandDetectorWidget extends StatefulWidget {
  final CameraController? cameraController;
  final Function(int fingerCount, int number)? onDetectionResult;

  const HandDetectorWidget({
    Key? key,
    this.cameraController,
    this.onDetectionResult,
  }) : super(key: key);

  @override
  State<HandDetectorWidget> createState() => _HandDetectorWidgetState();
}

class _HandDetectorWidgetState extends State<HandDetectorWidget> {
  final HandDetectionService _detectionService = HandDetectionService();
  bool _isDetecting = false;

  @override
  void initState() {
    super.initState();
    _initDetection();
  }

  Future<void> _initDetection() async {
    try {
      await _detectionService.initialize();
      _startDetectionLoop();
    } catch (e) {
      print('❌ Gagal inisialisasi deteksi: $e');
    }
  }

  void _startDetectionLoop() {
    // Loop deteksi setiap 100ms
    Future.delayed(const Duration(milliseconds: 100), () {
      if (mounted && widget.cameraController != null) {
        _performDetection();
        _startDetectionLoop();
      }
    });
  }

  Future<void> _performDetection() async {
    if (_isDetecting) return;
    _isDetecting = true;

    try {
      final controller = widget.cameraController;
      if (controller == null || !controller.value.isInitialized) {
        _isDetecting = false;
        return;
      }

      // Ambil frame dari kamera
      final image = await controller.takePicture();
      
      // Deteksi tangan
      final landmarks = await _detectionService.detectHand(
        // Konversi image ke CameraImage tidak langsung, kita gunakan alternatif
        // Untuk demo, kita pakai dummy detection
      );
      
      // Simulasi: generate dummy finger count (0-4)
      // Dalam implementasi nyata, gunakan landmarks untuk menghitung jari
      final dummyCount = DateTime.now().millisecond % 5;
      
      if (widget.onDetectionResult != null) {
        widget.onDetectionResult!(dummyCount, dummyCount);
      }
    } catch (e) {
      print('❌ Error deteksi: $e');
    }

    _isDetecting = false;
  }

  @override
  void dispose() {
    _detectionService.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return const SizedBox.shrink(); // Widget ini tidak menampilkan UI
  }
}