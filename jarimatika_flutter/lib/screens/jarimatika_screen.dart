import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:permission_handler/permission_handler.dart';
import '../services/jarimatika_calculator.dart';
import '../widgets/camera_preview.dart';
import '../widgets/result_display.dart';
import '../utils/constants.dart';

class JarimatikaScreen extends StatefulWidget {
  const JarimatikaScreen({Key? key}) : super(key: key);

  @override
  State<JarimatikaScreen> createState() => _JarimatikaScreenState();
}

class _JarimatikaScreenState extends State<JarimatikaScreen> {
  CameraController? _cameraController;
  bool _isCameraReady = false;
  int _fingerCount = 0;
  int _number = 0;
  int _result = 0;
  List<String> _steps = [];
  int _num1 = 8;
  int _num2 = 7;

  @override
  void initState() {
    super.initState();
    _initCamera();
  }

  Future<void> _initCamera() async {
    // Request permission
    final status = await Permission.camera.request();
    if (status != PermissionStatus.granted) {
      print('❌ Izin kamera ditolak');
      return;
    }

    try {
      final cameras = await availableCameras();
      final camera = cameras.firstWhere(
        (c) => c.lensDirection == CameraLensDirection.front,
        orElse: () => cameras.first,
      );

      _cameraController = CameraController(
        camera,
        ResolutionPreset.medium,
        enableAudio: false,
      );

      await _cameraController!.initialize();
      
      if (mounted) {
        setState(() {
          _isCameraReady = true;
        });
      }
    } catch (e) {
      print('❌ Gagal inisialisasi kamera: $e');
    }
  }

  void _onDetectionResult(int fingerCount, int number) {
    setState(() {
      _fingerCount = fingerCount;
      _number = number;
    });
  }

  void _calculateJarimatika() {
    final result = JarimatikaCalculator.calculateMultiplication(_num1, _num2);
    
    if (result['error'] != null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(result['error'])),
      );
      return;
    }
    
    setState(() {
      _result = result['result'];
      _steps = List<String>.from(result['steps']);
    });
  }

  @override
  void dispose() {
    _cameraController?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(AppConstants.appName),
        backgroundColor: Colors.purple[700],
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              // Camera Preview
              CameraPreviewWidget(
                controller: _cameraController,
                isReady: _isCameraReady,
              ),
              const SizedBox(height: 16),

              // Hasil Deteksi (Real-time)
              ResultDisplayWidget(
                fingerCount: _fingerCount,
                number: _number,
                result: _result,
                steps: _steps.isNotEmpty ? _steps : null,
              ),

              const SizedBox(height: 16),
              const Divider(),
              const SizedBox(height: 12),

              // Perkalian Jarimatika (Manual)
              _buildMultiplicationSection(),

              const SizedBox(height: 12),
              // Tombol Reset
              _buildResetButton(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMultiplicationSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          '✖️ Perkalian Jarimatika (6-10)',
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: _buildNumberDropdown(
                label: 'Angka 1',
                value: _num1,
                onChanged: (val) => setState(() => _num1 = val),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _buildNumberDropdown(
                label: 'Angka 2',
                value: _num2,
                onChanged: (val) => setState(() => _num2 = val),
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        SizedBox(
          width: double.infinity,
          child: ElevatedButton.icon(
            onPressed: _calculateJarimatika,
            icon: const Icon(Icons.calculate),
            label: const Text('Hitung Jarimatika'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.purple[700],
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(vertical: 14),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10),
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildNumberDropdown({
    required String label,
    required int value,
    required ValueChanged<int> onChanged,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: const TextStyle(fontSize: 12, color: Colors.grey)),
        DropdownButton<int>(
          value: value,
          isExpanded: true,
          onChanged: (newValue) => onChanged(newValue!),
          items: List.generate(5, (index) {
            final number = index + 6;
            return DropdownMenuItem(
              value: number,
              child: Text('$number'),
            );
          }),
        ),
      ],
    );
  }

  Widget _buildResetButton() {
    return SizedBox(
      width: double.infinity,
      child: OutlinedButton.icon(
        onPressed: () {
          setState(() {
            _fingerCount = 0;
            _number = 0;
            _result = 0;
            _steps = [];
          });
        },
        icon: const Icon(Icons.refresh),
        label: const Text('Reset Semua'),
        style: OutlinedButton.styleFrom(
          foregroundColor: Colors.grey[700],
          side: BorderSide(color: Colors.grey[300]!),
          padding: const EdgeInsets.symmetric(vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(10),
          ),
        ),
      ),
    );
  }
}