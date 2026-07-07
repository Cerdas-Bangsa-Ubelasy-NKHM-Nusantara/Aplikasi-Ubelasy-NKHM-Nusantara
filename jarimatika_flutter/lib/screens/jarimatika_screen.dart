import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:hand_detection/hand_detection.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'dart:convert';

class JarimatikaScreen extends StatefulWidget {
  @override
  _JarimatikaScreenState createState() => _JarimatikaScreenState();
}

class _JarimatikaScreenState extends State<JarimatikaScreen> {
  CameraController? _controller;
  HandDetector? _handDetector;
  int _fingerCount = 0;
  int _result = 0;
  bool _isCameraReady = false;

  @override
  void initState() {
    super.initState();
    _initCamera();
    _initHandDetector();
  }

  // Inisialisasi kamera
  Future<void> _initCamera() async {
    final cameras = await availableCameras();
    _controller = CameraController(cameras[0], ResolutionPreset.medium);
    await _controller!.initialize();
    setState(() => _isCameraReady = true);
  }

  // Inisialisasi detektor tangan (MediaPipe/TFLite)
  Future<void> _initHandDetector() async {
    _handDetector = HandDetector();
    await _handDetector!.loadModel();
  }

  // Kirim hasil ke Streamlit (via postMessage)
  void _sendResultToStreamlit(int fingerCount, int result) {
    if (WebView.platform != null) {
      final message = jsonEncode({
        'fingerCount': fingerCount,
        'result': result,
      });
      // Kirim ke parent (Streamlit iframe)
      // window.parent.postMessage(message, '*');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('🖐️ Jarimatika')),
      body: Column(
        children: [
          // Preview Kamera
          Expanded(
            flex: 2,
            child: _isCameraReady
                ? CameraPreview(_controller!)
                : Center(child: CircularProgressIndicator()),
          ),
          // Hasil Deteksi
          Container(
            padding: EdgeInsets.all(16),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildResultCard('Jari', _fingerCount),
                _buildResultCard('Angka', _fingerCount),
                _buildResultCard('Hasil', _result),
              ],
            ),
          ),
          // Tombol Hitung (Manual)
          ElevatedButton(
            onPressed: () {
              // Logika perhitungan Jarimatika
              setState(() {
                _result = _fingerCount * 10 + _fingerCount;
              });
            },
            child: Text('Hitung Jarimatika'),
          ),
        ],
      ),
    );
  }

  Widget _buildResultCard(String label, int value) {
    return Card(
      child: Padding(
        padding: EdgeInsets.all(12),
        child: Column(
          children: [
            Text(label, style: TextStyle(fontSize: 12, color: Colors.grey)),
            Text(value.toString(), style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _controller?.dispose();
    _handDetector?.dispose();
    super.dispose();
  }
}