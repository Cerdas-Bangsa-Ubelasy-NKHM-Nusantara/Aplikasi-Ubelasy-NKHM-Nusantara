class AppConstants {
  static const String appName = '🖐️ Jarimatika';
  static const String modelPath = 'assets/models/hand_landmark.tflite';
  
  // Mapping jari ke angka (Jarimatika PMD)
  static const List<String> fingerNames = [
    'Kelingking', // 6
    'Manis',      // 7
    'Tengah',     // 8
    'Telunjuk',   // 9
    'Jempol',     // 10
  ];
  
  static const int minNumber = 6;
  static const int maxNumber = 10;
  static const int totalFingers = 5;
}