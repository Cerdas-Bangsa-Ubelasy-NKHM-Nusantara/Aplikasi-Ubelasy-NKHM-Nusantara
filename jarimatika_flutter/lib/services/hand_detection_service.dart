import 'dart:io';
import 'dart:typed_data';
import 'package:camera/camera.dart';
import 'package:hand_detection/hand_detection.dart';
import 'package:google_ml_kit/google_ml_kit.dart';
import 'package:flutter/services.dart';
import '../utils/constants.dart';

class HandDetectionService {
  static final HandDetectionService _instance = HandDetectionService._internal();
  factory HandDetectionService() => _instance;
  HandDetectionService._internal();

  late HandDetector _handDetector;
  bool _isInitialized = false;
  
  // Landmark yang terdeteksi
  List<HandLandmark>? _currentLandmarks;
  
  /// Inisialisasi detektor tangan dengan model TFLite
  Future<void> initialize() async {
    if (_isInitialized) return;
    
    try {
      // Load model dari assets
      final modelBytes = await _loadModel();
      
      // Inisialisasi detektor (menggunakan hand_detection package)
      _handDetector = await HandDetector.fromAsset(
        'assets/models/hand_landmark.tflite',
      );
      
      _isInitialized = true;
    } catch (e) {
      print('❌ Gagal inisialisasi hand detector: $e');
      // Fallback: inisialisasi dengan google_ml_kit
      try {
        final options = PoseDetectorOptions();
        // _poseDetector = PoseDetector(options: options);
        _isInitialized = true;
      } catch (e2) {
        print('❌ Gagal inisialisasi fallback: $e2');
        throw Exception('Tidak dapat inisialisasi detektor tangan');
      }
    }
  }

  /// Load model dari assets
  Future<ByteData> _loadModel() async {
    try {
      return await rootBundle.load(AppConstants.modelPath);
    } catch (e) {
      print('⚠️ Model tidak ditemukan di assets, gunakan fallback');
      // Fallback: model default dari package
      throw Exception('Model file not found');
    }
  }

  /// Deteksi tangan dari frame kamera
  Future<List<HandLandmark>?> detectHand(CameraImage image) async {
    if (!_isInitialized) return null;
    
    try {
      // Konversi CameraImage ke InputImage (untuk google_ml_kit)
      final inputImage = _convertCameraImageToInputImage(image);
      
      if (inputImage == null) return null;
      
      // Deteksi menggunakan hand_detection
      final landmarks = await _handDetector.detect(image);
      
      _currentLandmarks = landmarks;
      return landmarks;
    } catch (e) {
      print('❌ Error deteksi tangan: $e');
      return null;
    }
  }

  /// Konversi CameraImage ke InputImage
  InputImage? _convertCameraImageToInputImage(CameraImage image) {
    try {
      final format = image.format.group;
      final bytes = image.planes[0].bytes;
      final width = image.width;
      final height = image.height;
      
      final inputImageData = InputImageData(
        size: Size(width.toDouble(), height.toDouble()),
        imageRotation: InputImageRotation.rotation0deg,
        inputImageFormat: InputImageFormat.nv21,
        planeData: image.planes.map((plane) {
          return InputImagePlaneMetadata(
            bytesPerRow: plane.bytesPerRow,
            height: plane.height,
            width: plane.width,
          );
        }).toList(),
      );
      
      return InputImage.fromByteData(
        bytes: bytes as ByteData? ?? ByteData(0),
        metadata: inputImageData,
      );
    } catch (e) {
      return null;
    }
  }

  /// Menghitung jumlah jari yang terbuka dari landmark
  int countOpenFingers(List<HandLandmark> landmarks) {
    if (landmarks.isEmpty) return 0;
    
    // Urutan landmark yang umum: 4=ibu jari, 8=telunjuk, 12=tengah, 16=manis, 20=kelingking
    final tipIndices = [4, 8, 12, 16, 20];
    final baseIndices = [2, 5, 9, 13, 17];
    
    int count = 0;
    for (int i = 0; i < tipIndices.length; i++) {
      final tip = landmarks[tipIndices[i]];
      final base = landmarks[baseIndices[i]];
      
      // Cek apakah ujung jari lebih tinggi dari pangkal (untuk tangan menghadap ke atas)
      if (tip.y < base.y) {
        count++;
      }
    }
    
    return count.clamp(0, 4);
  }

  /// Ambil landmark terakhir yang terdeteksi
  List<HandLandmark>? getCurrentLandmarks() => _currentLandmarks;
  
  /// Cek apakah detektor sudah siap
  bool isInitialized() => _isInitialized;
  
  /// Bersihkan resources
  void dispose() {
    _handDetector.dispose();
    _isInitialized = false;
  }
}