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

  HandDetector? _handDetector;
  bool _isInitialized = false;
  
  // Landmark yang terdeteksi
  List<HandLandmark>? _currentLandmarks;
  
  /// Inisialisasi detektor tangan dengan model TFLite
  Future<void> initialize() async {
    if (_isInitialized) return;
    
    try {
      // Opsi 1: Load model dari assets
      try {
        _handDetector = await HandDetector.fromAsset(
          'assets/models/hand_landmark.tflite',
        );
        print('✅ Hand detector loaded from assets');
      } catch (e) {
        print('⚠️ Gagal load dari assets, mencoba create default: $e');
        // Opsi 2: Gunakan model default dari package
        _handDetector = await HandDetector.create();
        print('✅ Hand detector created with default model');
      }
      
      if (_handDetector != null) {
        _isInitialized = true;
      } else {
        throw Exception('Tidak dapat inisialisasi hand detector');
      }
    } catch (e) {
      print('❌ Gagal inisialisasi hand detector: $e');
      // Fallback: inisialisasi dengan google_ml_kit (jika diperlukan)
      try {
        // Contoh fallback dengan pose detector (hanya placeholder)
        // final options = PoseDetectorOptions();
        // _poseDetector = PoseDetector(options: options);
        // _isInitialized = true;
        throw Exception('Tidak dapat inisialisasi detektor tangan');
      } catch (e2) {
        print('❌ Gagal inisialisasi fallback: $e2');
        throw Exception('Tidak dapat inisialisasi detektor tangan');
      }
    }
  }

  /// Deteksi tangan dari frame kamera
  Future<List<HandLandmark>?> detectHand(CameraImage image) async {
    if (!_isInitialized || _handDetector == null) return null;
    
    try {
      // Deteksi menggunakan hand_detection
      final landmarks = await _handDetector!.detect(image);
      _currentLandmarks = landmarks;
      return landmarks;
    } catch (e) {
      print('❌ Error deteksi tangan: $e');
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
    _handDetector?.dispose();
    _handDetector = null;
    _isInitialized = false;
  }
}