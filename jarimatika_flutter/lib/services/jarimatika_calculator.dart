class JarimatikaCalculator {
  /// Menghitung perkalian dengan metode Jarimatika PMD (6-10)
  /// @param num1 angka pertama (6-10)
  /// @param num2 angka kedua (6-10)
  /// @return Map berisi hasil dan langkah-langkah perhitungan
  static Map<String, dynamic> calculateMultiplication(int num1, int num2) {
    if (num1 < 6 || num1 > 10 || num2 < 6 || num2 > 10) {
      return {
        'error': 'Gunakan angka antara 6-10',
        'result': null,
        'steps': [],
      };
    }

    // Indeks jari (0=Kelingking, 1=Manis, 2=Tengah, 3=Telunjuk, 4=Jempol)
    final idx1 = num1 - 6;
    final idx2 = num2 - 6;
    
    const fingerNames = ['Kelingking', 'Manis', 'Tengah', 'Telunjuk', 'Jempol'];
    final rightFinger = fingerNames[idx1];
    final leftFinger = fingerNames[idx2];

    // Jari bawah (dari pertemuan ke bawah)
    final bawahKanan = idx1 + 1;
    final bawahKiri = idx2 + 1;
    
    // Jari atas (dari pertemuan ke atas)
    final atasKanan = 5 - bawahKanan;
    final atasKiri = 5 - bawahKiri;
    
    final totalBawah = bawahKanan + bawahKiri;
    final totalAtas = atasKanan * atasKiri;
    final hasil = totalBawah * 10 + totalAtas;

    final steps = [
      '📌 ${num1} × ${num2}',
      '👉 ${rightFinger} kanan + ${leftFinger} kiri',
      '🔽 Jari bawah: ${bawahKanan} + ${bawahKiri} = ${totalBawah} (puluhan)',
      '🔼 Jari atas: ${atasKanan} × ${atasKiri} = ${totalAtas} (satuan)',
      '✅ Hasil: ${totalBawah}${totalAtas} = ${hasil}',
    ];

    return {
      'result': hasil,
      'steps': steps,
      'rightFinger': rightFinger,
      'leftFinger': leftFinger,
      'bawahKanan': bawahKanan,
      'bawahKiri': bawahKiri,
      'atasKanan': atasKanan,
      'atasKiri': atasKiri,
      'totalBawah': totalBawah,
      'totalAtas': totalAtas,
    };
  }

  /// Konversi jumlah jari ke angka (untuk deteksi real-time)
  static int getNumberFromFingers(int fingerCount) {
    return fingerCount.clamp(0, 4);
  }
}